Buildout Eggscleaner
======================

Introduction
------------
The buildout.eggscleaner extensions can be used to ensure your egg directory only contains 'used' eggs.
The extension can report, but also move unused eggs to a specified directory.


Installation
------------
Eggscleaner is a buildout extensions, can add it like so ::

    [buildout]
    extensions =
            buildout.eggscleaner


Options
----------
old-eggs-directory
        The directory you want buildout.eggscleaner to move your unused eggs to.
        Should an excact egg already exist, we remove the one in the ''used'' eggs directory


Example ::    

        [buildout]                                                                 
        extensions =                                                               
                buildout.eggscleaner  
        old-eggs-directory = ${buildout:directory}/old-eggs/

Tested under
-----------
zc.buildout 1.5.1 and 1.5.2

Working with other extensions
-----------
I looked at how buildout.dumppickedversions works and made this extension work in a similar manner.
This extension will run alongside that one perfectly well.


Example outputs
-----------

Nothing do ::

    *************** BUILDOUT EGGSCLEANER ****************
    No unused eggs in eggs directory
    *************** /BUILDOUT EGGSCLEANER ****************


Moving eggs ::

    *************** BUILDOUT EGGSCLEANER ****************
    Moved unused egg: webcouturier.dropdownmenu-2.3-py2.6.egg 
    Moved unused egg: collective.uploadify-1.0-py2.6.egg 
    Moved unused egg: collective.simplesocial-1.6-py2.6.egg 
    Moved unused egg: collective.autopermission-1.0b2-py2.6.egg 
    *************** /BUILDOUT EGGSCLEANER ****************

Reporting ::

    *************** BUILDOUT EGGSCLEANER ****************
    Don't have a 'old-eggs-directory' set, only reporting
    Can add it by adding 'old-eggs-directory = ${buildout:directory}/old-eggs' to your [buildout]
    Found unused egg: webcouturier.dropdownmenu-2.3-py2.6.egg 
    Found unused egg: plone.recipe.command-1.1-py2.6.egg 
    Found unused egg: collective.uploadify-1.0-py2.6.egg 
    Found unused egg: Products.DocFinderTab-1.0.5-py2.6.egg 
    Found unused egg: collective.simplesocial-1.6-py2.6.egg 
    Found unused egg: collective.autopermission-1.0b2-py2.6.egg 
    Found unused egg: Products.Clouseau-1.0-py2.6.egg 
    *************** /BUILDOUT EGGSCLEANER ****************

TODO
-----------
Write tests!!
