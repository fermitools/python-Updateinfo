===========
UpdateInfo
===========

UpdateInfo provides useful objects for creating the updateinfo.xml
for use with yum's security plugin.

This isn't really fancy, but I've included the xsd this validates against.
The xsd should also validate against Fedora or Suse.

Quick start
-----------

1. import updateinfo
2. u = updateinfo.Updateinfo()
3. fd = open('/path/to/sample/in/doc/dir/example.xml', 'r')
4. u.xml = fd.read()
5. print(u.xml)

The resulting xml file should be added to the yum repo metadata.

    modifyrepo updateinfo.xml /path/to/repodata/

I've included an example program that should help get you started.

If you are curious the objects log intersting actions at logger.DEBUG

There are a lot of options and ways of using these objects, so make sure
to read the help that comes with each module.

There is also a helper directory you can use which will allow you to very
simply build and update your updateinfo.xml if you wish.

Odds are you will need to build your own helper object for your data store,
but these should at least get you started with the basics.

Testing
-----------

If you wish to run the provided unit tests, simply run:

    python updateinfo/tests/

For coverage.py try:

    coverage run --include=updateinfo* --branch updateinfo/tests/__main__.py
    coverage html

