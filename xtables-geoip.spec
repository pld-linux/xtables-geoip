Summary:	GeoIP database files for xt_geoip
Name:		xtables-geoip
Version:	20090401
Release:	1
License:	GPL
Group:		Networking/Admin
URL:		http://maxmind.com/
Source0:	http://jengelh.medozas.de/files/geoip/geoip_iv0_database-%{version}.tar.bz2
# Source0-md5:	0cd65043c6165ed49a611c2cd4bc2fb4
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The package contains the GeoIP definition files (which IP addresses
belong to which country) that are needed for Xtables-addons's xt_geoip
module.

%prep
%setup -q -n var

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/lib/geoip/{B,L}E
install geoip/BE/* $RPM_BUILD_ROOT/var/lib/geoip/BE
install geoip/LE/* $RPM_BUILD_ROOT/var/lib/geoip/LE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
/var/lib/geoip
