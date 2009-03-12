Summary:	XAdES digital signature standard library
Name:		libdigidoc
Version:	2.2.5
Release:	1
License:	GPL
Group:		Libraries
Source0:	http://www.openxades.org/files/%{name}-release-%{version}.tar.gz
# Source0-md5:	cc07cb0b6fa378ed85d12d0c9a7df07f
URL:		http://www.openxades.org/
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir		/sbin

%description
DigiDoc is a generic library implementing the XAdES digital signature
standard. It allows to create, sign, verify, and modify digidoc XML
containers. Support for doing hardware cryptographic signing
operations is porivded via PKCS#11.

%package devel
Summary:	Header files and development documentation for libdigidoc
Group:		Development/Libraries

%description devel
Header files and development documentation for libdigidoc.

%package static
Summary:	Static libdigidoc library
Group:		Development/Libraries
Requires:	%{name}-devel = %{epoch}:%{version}-%{release}

%description static
Static libdigidoc library.

%prep
%setup -q

%build
%configure

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/*.pdf doc/*.xsd
%attr(755,root,root) %{_bindir}/cdigidoc
%attr(755,root,root) %{_libdir}/libdigidoc.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libdigidoc.so.2
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/digidoc.conf
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdigidoc.so
%{_libdir}/libdigidoc.la
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libdigidoc.a
