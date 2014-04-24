import os
import logging
import zc.buildout.easy_install
import shutil
import sys

logger=zc.buildout.easy_install.logger


def enable_eggscleaner(old_get_dist):
    """Patching method so we can go keep track of all the used eggs"""
    def get_dist(self, *kargs, **kwargs):
        dists = old_get_dist(self, *kargs, **kwargs)
        for dist in dists:
            egg_name = dist.egg_name()
            path = os.path.normpath(dist.location)
            if sys.platform == 'win32':
                path = path.lower()
            if egg_name not in self.__used_eggs:
                self.__used_eggs[egg_name] = path
        return dists
    return get_dist


def eggs_cleaner(old_logging_shutdown, eggs_directory, old_eggs_directory, extensions):
    """Patching method so we can report and/or move eggs when buildout shuts down"""

    def logging_shutdown():
        #Set some easy to use variables
        used_eggs = set(zc.buildout.easy_install.Installer.__used_eggs.values())
        eggsdirectory = os.listdir(eggs_directory)
        move_eggs = []

        #Loop through the contents of the eggs directory
        #Determine which eggs aren't used..
        #ignore any which seem to be buildout  extensions
        for eggname in eggsdirectory:
            fullpath = os.path.normpath(os.path.join(eggs_directory, eggname))
            if sys.platform == 'win32':
                fullpath = fullpath.lower()
            if not fullpath in used_eggs:
                is_extensions = False
                for ext in extensions:
                    if ext in eggname:
                        is_extensions = True
                        break
                if not is_extensions:
                    move_eggs.append(eggname)


        print("*************** BUILDOUT EGGSCLEANER ****************")

        #Move or not?
        if old_eggs_directory:
            if not os.path.exists(old_eggs_directory):
                #Create if needed
                os.mkdir(old_eggs_directory)
            for eggname in move_eggs:
                oldpath = os.path.join(eggs_directory, eggname)
                newpath= os.path.join(old_eggs_directory, eggname)
                if not os.path.exists(newpath):
                    shutil.move(oldpath, newpath)
                else:
                    try:
                        if os.path.isfile(oldpath) or os.path.islink(oldpath):
                           os.remove(oldpath)
                        else:
                           shutil.rmtree(oldpath)
                    except (OSError, IOError) as e:
                        print "Can't remove path %s: %s" % (path, e)
                print("Moved unused egg: %s " % eggname)
        else: #Only report
            print("Don't have a 'old-eggs-directory' set, only reporting")
            print("Can add it by adding 'old-eggs-directory = ${buildout:directory}/old-eggs' to your [buildout]")
            for eggname in move_eggs:
                print("Found unused egg: %s " % eggname)

        #Nothing to do?
        if not move_eggs:
            print "No unused eggs in eggs directory"
        print("*************** /BUILDOUT EGGSCLEANER ****************")

        old_logging_shutdown()
    return logging_shutdown

def install(buildout):

    # See if the eggs-directory is local or not.
    buildout_directory = buildout['buildout'].get('directory', None)


    #Fetch the eggs-directory from the buildout
    eggs_directory = 'eggs-directory' in buildout['buildout'] and buildout['buildout']['eggs-directory'].strip() or None

    #Fetch our old-eggs-directory
    old_eggs_directory = 'old-eggs-directory' in buildout['buildout'] and \
                    buildout['buildout']['old-eggs-directory'].strip() or \
                                    None
    # Very basic check to see if the local directory also contains the eggs directory
    # If not, we don't do anything because the user_default possibly contains 1000's of eggs
    # Many of which might not be used here, resulting in a cleanup of your local egg repo.
    # Which is undesired at best ;)
    if buildout_directory and buildout_directory in eggs_directory:
        #Get a list of extensions. There is no fancier way to ensure they don't get included.
        extensions = buildout['buildout'].get('extensions', '').split()

        #Patch methods
        zc.buildout.easy_install.Installer.__used_eggs= {}
        zc.buildout.easy_install.Installer._get_dist = enable_eggscleaner(
                                      zc.buildout.easy_install.Installer._get_dist)
        logging.shutdown = eggs_cleaner(logging.shutdown, eggs_directory, old_eggs_directory, extensions)
    else:
        print("*************** BUILDOUT EGGSCLEANER ****************")
        print("None-local eggs-directory found, skipping. ")
        print("buildout-directory: {0} ".format(buildout_directory))
        print("eggs-directory: {0} ".format(eggs_directory))
        print("*************** /BUILDOUT EGGSCLEANER ****************")


    pass
