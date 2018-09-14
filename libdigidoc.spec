Summary:	XAdES digital signature standard library
Summary(pl.UTF-8):	Biblioteka obsługująca standard podpisów cyfrowych XAdES
Name:		libdigidoc
Version:	3.10.4
Release:	1
License:	LGPL v2.1+
Group:		Libraries
#Source0Download: https://github.com/open-eid/libdigidoc/releases
Source0:	https://github.com/open-eid/libdigidoc/releases/download/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	050c73fe991dae0ffe3afec616e20851
Patch0:		%{name}-cmake.patch
URL:		https://github.com/open-eid/libdigidoc
BuildRequires:	cmake >= 2.8
BuildRequires:	libxml2-devel >= 2
BuildRequires:	openssl-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires:	ca-certificates
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DigiDoc is a generic library implementing the XAdES digital signature
standard. It allows to create, sign, verify, and modify digidoc XML
containers. Support for doing hardware cryptographic signing
operations is provided via PKCS#11.

%description -l pl.UTF-8
DigiDoc to ogólna biblioteka implementująca standard podpisów
cyfrowych XAdES. Pozwala na tworzenie, podpisywanie, sprawdzanie i
modyfikowanie kontenerów XML digidoc. Obsługa podpisywania przy użyciu
kryptografii sprzętowej jest zapewniana poprzez PKCS#11.

%package devel
Summary:	Header files for libdigidoc library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libdigidoc
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	openssl-devel
Requires:	libxml2-devel >= 2
Obsoletes:	libdigidoc-static

%description devel
Header files for libdigidoc library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libdigidoc.

%package apidocs
Summary:	Development documentation for libdigidoc
Summary(pl.UTF-8):	Dokumentacja programistyczna biblioteki libdigidoc
Group:		Documentation

%description apidocs
Development documentation for libdigidoc.

%description apidocs -l pl.UTF-8
Dokumentacja programistyczna biblioteki libdigidoc.

%prep
%setup -q
%patch0 -p1

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
%{__rm} $RPM_BUILD_ROOT%{_datadir}/%{name}/*.crt

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md RELEASE-NOTES.md
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/digidoc.conf
%attr(755,root,root) %{_libdir}/libdigidoc.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libdigidoc.so.2
%attr(755,root,root) %{_bindir}/cdigidoc
%{_mandir}/man1/cdigidoc.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdigidoc.so
%{_includedir}/libdigidoc
%{_pkgconfigdir}/libdigidoc.pc

%files apidocs
%defattr(644,root,root,755)
%doc doc/{SK-CDD-PRG-GUIDE.pdf,SK-COM-PRG-GUIDE.pdf,sample_files_CDD.zip}
