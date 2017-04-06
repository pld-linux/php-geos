#
# Conditional build:
%bcond_without	tests		# testing

%define		php_name	php%{?php_suffix}
Summary:	PHP extension for interfacing with the GEOS library
Summary(pl.UTF-8):	Rozszerzenie PHP do współpracy z biblioteką GEOS
Name:		%{php_name}-geos
Version:	1.0.0
Release:	2
Epoch:		1
License:	LGPL v2.1 (GEOS code), MIT (PHP interfaces)
Group:		Development/Languages/PHP
# http://git.osgeo.org/gogs/geos/php-geos
Source0:	https://git.osgeo.org/gogs/geos/php-geos/archive/%{version}.tar.gz?/php-geos-%{version}.tar.gz
# Source0-md5:	5107e7062b12cccca5903b83c90c2955
URL:		http://geos.osgeo.org/
%{?with_tests:BuildRequires:    %{php_name}-cli >= 5}
BuildRequires:	%{php_name}-devel >= 5
%{?with_tests:BuildRequires:	%{php_name}-pcre >= 5}
BuildRequires:	geos-devel >= 3.5
BuildRequires:	rpmbuild(macros) >= 1.666
%{?requires_php_extension}
Provides:	php(geos) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
PHP extension for interfacing with the GEOS library.

%description -l pl.UTF-8
Rozszerzenie PHP do współpracy z biblioteką GEOS.

%prep
%setup -q -n php-geos

%build
phpize
%configure
%{__make}

%if %{with tests}
%{__make} check \
	PHP_EXECUTABLE=%{__php} \
	RUN_TESTS_SETTINGS="-q -w failed.log"

test -f failed.log -a ! -s failed.log
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<EOF > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/geos.ini
; Enable GEOS extension module
extension=geos.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc COPYING MIT-LICENSE NEWS README.md TODO
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/geos.ini
%attr(755,root,root) %{php_extensiondir}/geos.so
