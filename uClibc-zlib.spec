%define _provides_exceptions libz.so.1\\|devel(libz)
%define _requires_exceptions devel(/lib/libNoVersion)

%define realname zlib

%define	major 1
%define	libname %{name}%{major}

%define basedir %{_prefix}/%{_target_cpu}-linux-uclibc
%define _sysconfdir %{basedir}/etc
%define _mandir %{basedir}/usr/share/man
%define _bindir %{basedir}/usr/bin
%define _sbindir %{basedir}/usr/sbin
%define _libdir %{basedir}/usr/lib
%define _docdir %{basedir}/usr/share/doc
%define _includedir %{basedir}/usr/include
%define _lib %{basedir}/lib

Summary:	The zlib compression and decompression library
Name:		uClibc-%{realname}
Version:	1.2.3
Release:	%mkrel 7
License:	BSD
Group:		System/Libraries
URL:		http://www.gzip.org/zlib/
Source0:	http://prdownloads.sourceforge.net/libpng/%{realname}-%{version}.tar.bz2
Patch0:		zlib-1.2.1-glibc.patch
Patch1:		zlib-1.2.1-multibuild.patch
Patch2:		zlib-1.2.2.2-build-fPIC.patch
Patch4:		zlib-1.2.1.1-deb-alt-inflate.patch
BuildRequires:	uClibc uClibc-devel uClibc-static-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.

%package -n	%{libname}
Summary:	The zlib compression and decompression library
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Requires:	uClibc

%description -n	%{libname}
The zlib compression library provides in-memory compression and
decompression functions, including integrity checks of the uncompressed
data.  This version of the library supports only one compression method
(deflation), but other algorithms may be added later, which will have
the same stream interface.  The zlib library is used by many different
system programs.

%package -n	%{libname}-devel
Summary:	Header files and libraries for developing apps which will use zlib
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	uClibc-devel uClibc-static-devel

%description -n	%{libname}-devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

Install the zlib-devel package if you want to develop applications that
will use the zlib library.

%prep

%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1 -b .multibuild
%patch2 -p1 -b .build-fPIC
%patch4 -p1 -b .deb-alt-inflate

%build

mkdir objs
pushd objs
    CFLAGS="%{optflags}" uclibc ../configure --shared --prefix=%{basedir}/usr
    uclibc make
    uclibc make test
    ln -s ../zlib.3 .
popd

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_prefix}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_lib}

uclibc make install -C objs prefix=%{buildroot}%{basedir}%{_prefix} \
    includedir=%{buildroot}%{_includedir} libdir=%{buildroot}%{_libdir}

mv %{buildroot}%{_libdir}/*.so.* %{buildroot}/%{_lib}/

ln -s ../../lib/libz.so.%{version} %{buildroot}%{_libdir}/

%post -n %{libname} -p %{basedir}/sbin/ldconfig

%postun -n %{libname} -p %{basedir}/sbin/ldconfig

%clean
rm -fr %{buildroot}

%files -n %{libname}
%defattr(-, root, root)
%doc README
/%{_lib}/libz.so.*
%{_libdir}/libz.so.*

%files -n %{libname}-devel
%defattr(-, root, root)
%doc README ChangeLog algorithm.txt
%{_libdir}/*.a
%{_libdir}/*.so
%{_includedir}/*
%{_mandir}/*/*


