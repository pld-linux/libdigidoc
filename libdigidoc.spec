#
# Conditional build:
%bcond_with		static_libs	# build static libraries

Summary:	XAdES digital signature standard library
Name:		libdigidoc
Version:	3.10.2
Release:	1
License:	LGPL v2+
Group:		Libraries
Source0:	https://github.com/open-eid/libdigidoc/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	987a21c44a8b627794b6f810bf15465f
URL:		https://github.com/open-eid/libdigidoc
BuildRequires:	cmake
BuildRequires:	libstdc++-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	ca-certificates
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DigiDoc is a generic library implementing the XAdES digital signature
standard. It allows to create, sign, verify, and modify digidoc XML
containers. Support for doing hardware cryptographic signing
operations is porivded via PKCS#11.

%package devel
Summary:	Header files and development documentation for libdigidoc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files and development documentation for libdigidoc.

%package static
Summary:	Static libdigidoc library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

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

# certs come from ca-certificates package
rm -r $RPM_BUILD_ROOT%{_datadir}/%{name}/*.crt

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md RELEASE-NOTES.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/digidoc.conf
%attr(755,root,root) %{_libdir}/%{name}.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{name}.so.2
%attr(755,root,root) %{_bindir}/cdigidoc
%{_mandir}/man1/cdigidoc.1*

%files devel
%defattr(644,root,root,755)
%doc doc/*
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/%{name}.so
%{_includedir}/%{name}
%{_pkgconfigdir}/%{name}.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libdigidoc.a
%endif
