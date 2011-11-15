Summary:	GeoIP database files for xt_geoip
Name:		xtables-geoip
Version:	20111102
Release:	1
License:	GPL, Open Data License
Group:		Networking/Admin
URL:		http://www.maxmind.com/
Source0:	http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
# Source0-md5:	8eccf4ece22fe4b238a73ee14a6af4f7
Source1:	http://geolite.maxmind.com/download/geoip/database/GeoIPv6.csv.gz
# Source1-md5:	cfd5f62998468def232b5ec7b1f53950
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
cp -p %{SOURCE2} .

%build
%{__perl} %{SOURCE3} GeoIPCountryWhois.csv GeoIPv6.csv | tee ranges.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dbdir}
cp -a %{byteorder} $RPM_BUILD_ROOT%{dbdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt ranges.txt
%dir %{dbdir}
%{dbdir}/%{byteorder}
