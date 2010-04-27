# TODO
# - build from source using http://jengelh.medozas.de/files/geoip/geoip_src.tar.bz2
# - make it arch dependant and package only LE or BE dirs?
Summary:	GeoIP database files for xt_geoip
Name:		xtables-geoip
Version:	20090901
Release:	2
License:	GPL
Group:		Networking/Admin
URL:		http://www.maxmind.com/
Source0:	http://jengelh.medozas.de/files/geoip/geoip_iv0_database-%{version}.tar.bz2
# Source0-md5:	896cb23ada582ac945dcd4af305884fe
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dbdir	/usr/share/xt_geoip

%description
The package contains the GeoIP definition files (which IP addresses
belong to which country) that are needed for Xtables-addons's xt_geoip
module.

%prep
%setup -q -n var

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dbdir}/{B,L}E
cp -a geoip/BE/* $RPM_BUILD_ROOT%{dbdir}/BE
cp -a geoip/LE/* $RPM_BUILD_ROOT%{dbdir}/LE

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{dbdir}
