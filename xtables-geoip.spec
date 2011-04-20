Summary:	GeoIP database files for xt_geoip
Name:		xtables-geoip
Version:	20110404
Release:	1
License:	GPL, Open Data License
Group:		Networking/Admin
URL:		http://www.maxmind.com/
Source0:	http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
# Source0-md5:	37cf1951b9ecced2612f8ff0c0bd3eaa
Source1:	http://geolite.maxmind.com/download/geoip/database/GeoIPv6.csv.gz
# Source1-md5:	4956a5ab8ecd2dd078420faa5552f09f
Source2:	http://geolite.maxmind.com/download/geoip/database/LICENSE.txt
# Source2-md5:	a1381bd1aa0a0c91dc31b3f1e847cf4a
Source3:	http://xtables-addons.git.sourceforge.net/git/gitweb.cgi?p=xtables-addons/xtables-addons;a=blob_plain;f=geoip/xt_geoip_build
# Source3-md5:	9933235c5d9c4c7fbad965d6317f8c2f
BuildRequires:	perl-Text-CSV_XS >= 0.69
BuildRequires:	perl-base
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dbdir	/usr/share/xt_geoip

# no debuginfo to package
%define		_enable_debug_packages	0

%ifarch ppc sparc ppc64 sparc64 sparcv9
%define		byteorder	BE
%else
%define		byteorder	LE
%endif

%description
The package contains the GeoIP definition files (which IP addresses
belong to which country) that are needed for Xtables-addons's xt_geoip
module.

%prep
%setup -qc

ver=$(stat -c '%y' GeoIPCountryWhois.csv | awk '{print $1}' | tr -d -)
if [ "$ver" != %{version} ]; then
	exit 1
fi

gunzip -c %{SOURCE1} >GeoIPv6.csv
cp -a %{SOURCE2} .

%build
install -d %{byteorder}
%if "%{byteorder}" == "BE"
%{__perl} %{SOURCE3} -D %{byteorder} -b GeoIPCountryWhois.csv GeoIPv6.csv | tee ranges.txt
%else
%{__perl} %{SOURCE3} -D %{byteorder} GeoIPCountryWhois.csv GeoIPv6.csv | tee ranges.txt
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dbdir}/%{byteorder}
cp -a %{byteorder}/* $RPM_BUILD_ROOT%{dbdir}/%{byteorder}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt ranges.txt
%dir %{dbdir}
%{dbdir}/%{byteorder}
