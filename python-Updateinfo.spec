%{?scl:%scl_package python-Updateinfo}
%{!?scl:%global pkg_name %{name}}

Summary: Classes for making the yum updateinfo.xml.
Name: %{?scl_prefix}python-Updateinfo
Provides: %{?scl_prefix}python2-Updateinfo
Version: 0.2.0
Release: 9.sl%{rhel}
Source0: %{pkg_name}.tar.gz
License: GPL
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{pkg_name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Url: http://www.scientificlinux.org/

Requires: %{?scl_prefix}python %{?scl_prefix}python-hashlib %{?scl_prefix}python-argparse
Requires: %{?scl_prefix}PyYAML %{?scl_prefix}python-lxml

# for the concurrent.futures.ThreadPoolExecutor
Requires: %{?scl_prefix}python-futures

# creatrepo provides modifyrepo which is what we really need
Requires: createrepo

BuildRequires: %{?scl_prefix}python %{?scl_prefix}python-setuptools

# All these are for the testing....
BuildRequires: %{?scl_prefix}python-hashlib %{?scl_prefix}python-argparse
BuildRequires: %{?scl_prefix}python-futures
BuildRequires: %{?scl_prefix}PyYAML %{?scl_prefix}python-lxml
BuildRequires: createrepo

%if 0%{?rhel} == 7
# for SL7 Context
Provides:	example-util_%{name}
%endif

%description
python-Updateinfo provides useful objects for creating the updateinfo.xml
for use with yum and PackageKit.

This includes the xsd the xml should validate against to work correctly.
The xsd should also validate against EPEL, Fedora, and Suse

This includes an xsl template for transforming the xml into a functional
webpage.

%prep
%setup -n %{pkg_name}

%build
%{?scl:scl enable %{scl} "}
%py_build
%{?scl:"}

%install
%{?scl:scl enable %{scl} "}
%py_install
%{?scl:"}
mkdir -p $RPM_BUILD_ROOT/usr/share/doc/python-Updateinfo/
cp -pr docs/* $RPM_BUILD_ROOT/usr/share/doc/python-Updateinfo/

%check
%{?scl:scl enable %{scl} "}
PYTHONPATH=.
export PYTHONPATH
%{__python} updateinfo/tests/
%{?scl:"}


%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%doc /usr/share/doc/python-Updateinfo/

%changelog
* Wed Mar 7 2018 Pat Riehecky <riehecky@fnal.gov> 0.2.0-9.sl
- Quietly ignore null xml imports

* Tue Aug 23 2016 Pat Riehecky <riehecky@fnal.gov> 0.2.0-8.sl
- Finally fixed the repomd.xml age thingy again (I think)

* Fri Nov 13 2015 Pat Riehecky <riehecky@fnal.gov> 0.2.0-7.sl
- Added quick ref tool for parsing update ages

* Thu Aug 20 2015 Pat Riehecky <riehecky@fnal.gov> 0.2.0-5.sl
- Numerous new entry points have been added
- now uses futures for more parallel behavior

* Thu Jan 22 2015 Pat Riehecky <riehecky@fnal.gov> 0.2.0-1.sl
- Basically a complete re-write and API change
- Should work fine with python3 now
- Broke into lots of pieces for MVC like structure
- Now features over 2600 unit tests covering the behavior

* Tue Sep 9 2014 Pat Riehecky <riehecky@fnal.gov> 0.1.5-11.sl6
- Now with unit tests

* Thu Feb 6 2014 Pat Riehecky <riehecky@fnal.gov> 0.1.5-10.sl6
- pylint fixes
- added merge_with_xmlstring to updateinfo object

* Thu Feb 6 2014 Pat Riehecky <riehecky@fnal.gov> 0.1.5-9.sl6
- Added extra settings to modifyrepo
- the formatting script can now also merge updateinfo files

* Fri Oct 18 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-8.sl6
- Now easy to build for a software collection
- More efficient use of lists and list merging
- Added missing <br> to .xsl
- Smarter use of YAML documents in SL_contrib_to_updateinfo.py

* Thu Aug 15 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-7.sl6
- You can now easily check for the presence of files with os.path.basename
  under certian conditions.  The default is not to use this new feature
  everywhere except in updateinfohelper.py

* Fri Jul 5 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-6.6.sl6
- Fixed up a minor logic bug in updateinfohelper.py's import of old updateinfo

* Fri Jul 5 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-6.5.sl6
- Fixed missing Build-Requires

* Fri Jul 5 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-6.4.sl6
- added quick script to clean up the 1970 dates
- Fixed another bug in removing old updateinfo.xml files in updateinfohelper.py
- Added Makefile for use with koji's SCM integration

* Tue Apr 23 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-6.3.1.sl6
- switched to __name__ rather than __package__ for detecting if we are using
  lxml or if it is the native lib

* Fri Apr 19 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-6.3.sl6
- Added unique constraint on update ids
- The XSL transform now has lots of extra features and data strutures

* Fri Apr 12 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-6.2.sl6
- Fix minor bug in remove

* Mon Apr 8 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-6.1.sl6
- added support for xsl transforms and a sample updateinfo.xsl

* Thu Mar 28 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-6.sl6
- Added in the SL_contrib_to_updateinfo.py used for parsing the
  sl-addons YAML files
- Now recognizes bz2 updateinfo files for import

* Thu Mar 14 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-5.1.sl6
- Output is now in a stable order, should make find changes easier

* Fri Mar 1 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-5.sl6
- Added an extra script to simply check if a document is valid

* Mon Jan 28 2013 Pat Riehecky <riehecky@fnal.gov> 0.1.5-4.sl6
- Added an extra check to avoid bad behavior when not using lxml

* Thu Nov 15 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.5-3.sl6
- the example scripts can now be run with much more limited knowledge
- there are some sample updateinfo.xml files included for review
- a more feature rich example is provided
- 'prerelease' has been added to the updateinfo.xsd for package status
- the Package object can now review remote packages

* Thu Nov 15 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.5-2.1.sl6
- Entry.set_update_date now responds correctly to values of 'None'

* Wed Nov 7 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.5-2.sl6
- More documentation now avalible for how these objects interact
- You can now remove a reference from an entry
- the issued_date and update_date are now datetime objects

* Thu Nov 1 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.5-1.sl6
- The Updateinfo class can now easily ask about reference urls for all
   loaded entries.

* Thu Oct 11 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.5-0.sl6
- Added entry merge capibilities for merging entries with common
   data, such as an ID that applies to two different collections

* Wed Oct 3 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.4-2.sl6
- Added more 'convenience' functions for asking about object status
- Comments are now handled correctly

* Fri Sep 28 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.4-1.sl6
- misc bug fixes and typos
- You can now simply append to an unparsed updateinfo.xml if you want
- You can now skip the import of updateinfo.xml in updateinfohelper
- Requires are now more complete, I'm forcing lxml as it is much faster
   and has validate but this should continue to work in a pure python
   deployment if you just extract the source.

* Fri Sep 28 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.4-0.sl6
- You can now do much more complex things with updateinfohelper.py
   such as track unused packages or have a distinction between TUV
   and non-TUV ids

* Fri Sep 21 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.3-0.sl6
- Input can now be UTF-8
- updateinfohelper.py now has easy ways of dealing with unlisted
   packages.  You can return 'None' if you want to ignore them
   or 'raise' it is up to you.
- PrettyPrint now prints in a way that will actually still work
   with the validator functions
- another update to the xsd

* Wed Sep 19 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.2-0.sl6
- misc bug fixes
- now includes a helper class for abstracting away some of the
   messy details.  See helper_example.py in %doc

* Mon Sep 17 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.1-0.sl6
- now includes 'summary', 'solution', and 'rights' as valid for setting
- the xsd is now more fully documented
- the xml can now be pretty printed
- you can now force settings down the stack to make stuff consistant
- you can now load metadata from the repo itself to help with things
- some objects can be utilized like a dict now
- All xml output is now UTF-8

* Fri Sep 7 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.0-2.sl6
- now uses lxml for performance and validation

* Fri Aug 31 2012 Pat Riehecky <riehecky@fnal.gov> 0.1.0-1.sl6
- xsd can now validate lots more in the wild (EPEL, OpenSUSE).
- the xsd is now actually installed into %doc along with the example script
- The import functions can now import all sorts of things

* Mon Aug 20 2012 Pat Riehecky <riehecky@fnal.gov> 0.0.1
- initial build
