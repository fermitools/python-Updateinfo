Name:		sample
Version:	1
Release:	1.1
Summary:	Example

License:	GPL
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	bash

%description
I'm a test


%prep


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc



%changelog

