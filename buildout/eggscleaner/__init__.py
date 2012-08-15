import os
import sys
import logging
import zc.buildout.easy_install
import pkg_resources
import shutil

logger=zc.buildout.easy_install.logger


def enable_eggscleaner(old_get_dist):
    def get_dist(self, requirement, ws, always_unzip):
        dists = old_get_dist(self, requirement, ws, always_unzip)
        for dist in dists:
            self.__used_eggs[dist.egg_name()] = dist.location
        return dists
    return get_dist


def eggs_cleaner(old_logging_shutdown, eggs_directory, old_eggs_directory, extensions):

    def logging_shutdown():
        used_eggs = zc.buildout.easy_install.Installer.__used_eggs
        eggsdirectory = os.listdir(eggs_directory)
        move_eggs = []

        for eggname in eggsdirectory:
            fullpath = "{0}/{1}".format(eggs_directory, eggname)
            if not fullpath in used_eggs.values():
                is_extensions = False
                for ext in extensions:
                    if ext in eggname:
                        is_extensions = True
                        break
                if not is_extensions:
                    move_eggs.append(eggname)

        if not os.path.exists(old_eggs_directory):
            os.mkdir(old_eggs_directory)

        print("*************** BUILDOUT EGGSCLEANER ****************")

        if old_eggs_directory:
            for eggname in move_eggs:
                oldpath = "{0}/{1}".format(eggs_directory, eggname)
                newpath= "{0}/{1}".format(old_eggs_directory, eggname)
                if not os.path.exists(newpath):
                    shutil.move(oldpath, newpath)
                else:
                    shutil.rmtree(oldpath)
                print("Moved unused egg: {0} ".format(eggname))
        else:
            print("Don't have a 'old-eggs-directory' set, only reporting")
            for eggname in move_eggs:
                print("Found unused egg: {0} ".format(eggname))


        if not move_eggs:
            print "No unused eggs in eggs directory"
        print("*************** /BUILDOUT EGGSCLEANER ****************")

        old_logging_shutdown()
    return logging_shutdown

def install(buildout):

    eggs_directory = 'eggs-directory' in buildout['buildout'] and buildout['buildout']['eggs-directory'].strip() or None

    old_eggs_directory = 'old-eggs-directory' in buildout['buildout'] and \
                    buildout['buildout']['old-eggs-directory'].strip() or \
                                    None


    extensions = buildout['buildout'].get('extensions', '').split()

    zc.buildout.easy_install.Installer.__used_eggs= {}
    zc.buildout.easy_install.Installer._get_dist = enable_eggscleaner(
                                  zc.buildout.easy_install.Installer._get_dist)
    logging.shutdown = eggs_cleaner(logging.shutdown, eggs_directory, old_eggs_directory, extensions)


    pass
