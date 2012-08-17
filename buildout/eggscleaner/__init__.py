import os
import logging
import zc.buildout.easy_install
import shutil

logger=zc.buildout.easy_install.logger


def enable_eggscleaner(old_get_dist):
    """Patching method so we can go keep track of all the used eggs"""
    def get_dist(self, requirement, ws, always_unzip):
        dists = old_get_dist(self, requirement, ws, always_unzip)
        for dist in dists:
            self.__used_eggs[dist.egg_name()] = dist.location
        return dists
    return get_dist


def eggs_cleaner(old_logging_shutdown, eggs_directory, old_eggs_directory, extensions):
    """Patching method so we can report and/or move eggs when buildout shuts down"""

    def logging_shutdown():

        #Set some easy to use variables
        used_eggs = zc.buildout.easy_install.Installer.__used_eggs
        eggsdirectory = os.listdir(eggs_directory)
        move_eggs = []

        #Loop through the contents of the eggs directory
        #Determine which eggs aren't used..
        #ignore any which seem to be buildout  extensions
        for eggname in eggsdirectory:
            fullpath = "%s/%s" % (eggs_directory, eggname)
            if not fullpath in used_eggs.values():
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
                oldpath = "%s/%s" % (eggs_directory, eggname)
                newpath= "%s/%s" %(old_eggs_directory, eggname)
                if not os.path.exists(newpath):
                    shutil.move(oldpath, newpath)
                else:
                    shutil.rmtree(oldpath)
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

    #Fetch the eggs-directory from the buildout
    eggs_directory = 'eggs-directory' in buildout['buildout'] and buildout['buildout']['eggs-directory'].strip() or None

    #Fetch our old-eggs-directory
    old_eggs_directory = 'old-eggs-directory' in buildout['buildout'] and \
                    buildout['buildout']['old-eggs-directory'].strip() or \
                                    None

    #Get a list of extensions. There is no fancier way to ensure they don't get included.
    extensions = buildout['buildout'].get('extensions', '').split()

    #Patch methods
    zc.buildout.easy_install.Installer.__used_eggs= {}
    zc.buildout.easy_install.Installer._get_dist = enable_eggscleaner(
                                  zc.buildout.easy_install.Installer._get_dist)
    logging.shutdown = eggs_cleaner(logging.shutdown, eggs_directory, old_eggs_directory, extensions)


    pass
