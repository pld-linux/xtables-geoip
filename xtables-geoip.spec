Summary:	GeoIP database files for xt_geoip
Name:		xtables-geoip
Version:	20120104
Release:	1
License:	GPL, Open Data License
Group:		Networking/Admin
URL:		http://www.maxmind.com/
Source0:	http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
# Source0-md5:	469b827f3064eafe4a47b9318e933345
Source1:	http://geolite.maxmind.com/download/geoip/database/GeoIPv6.csv.gz
# Source1-md5:	6cab8b7818ce94826a01f9a6e9254fd3
Source2:	http://geolite.maxmind.com/download/geoip/database/LICENSE.txt
# Source2-md5:	a1381bd1aa0a0c91dc31b3f1e847cf4a
Source3:	http://xtables-addons.git.sourceforge.net/git/gitweb.cgi?p=xtables-addons/xtables-addons;a=blob_plain;f=geoip/xt_geoip_build
# Source3-md5:	9933235c5d9c4c7fbad965d6317f8c2f
BuildRequires:	perl-Text-CSV_XS >= 0.69
BuildRequires:	perl-base
BuildRequires:	rpm >= 4.4.9-56
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

%if "%{pld_release}" == "ac"
# handle older xtables in ac:
# kernel-net-xtables-addons-1.18-15@2.6.27.53_1.amd64
# still having old .iv0 names requirement
# http://xtables-addons.git.sourceforge.net/git/gitweb.cgi?p=xtables-addons/xtables-addons;a=commitdiff;h=25bf680ead80e505d5073308f151b4007cb5683f
# create hardlink, to be most compatible
for a in $RPM_BUILD_ROOT%{dbdir}/%{byteorder}/*.iv4; do
	ln $a ${a%.iv4}.iv0
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt ranges.txt
%dir %{dbdir}
%{dbdir}/%{byteorder}
