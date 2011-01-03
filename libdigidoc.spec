# TODO
# - use ca-certificates package and drop /usr/share/libdigidoc/certs
#
# Conditional build:
%bcond_with		static_libs	# build static libraries

Summary:	XAdES digital signature standard library
Name:		libdigidoc
Version:	2.7.0
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	http://esteid.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	5c00285299b027d6671f9a9ae9bcf433
URL:		http://code.google.com/p/esteid/
BuildRequires:	cmake
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
install -d build
cd build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README doc/*.pdf doc/*.xsd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/digidoc.conf
%attr(755,root,root) %{_libdir}/%{name}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.2
%attr(755,root,root) %{_bindir}/cdigidoc
%{_datadir}/%{name}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdigidoc.a
%endif
