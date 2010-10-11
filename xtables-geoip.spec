Summary:	GeoIP database files for xt_geoip
Name:		xtables-geoip
Version:	20101002
Release:	1
License:	GPL, Open Data License
Group:		Networking/Admin
URL:		http://www.maxmind.com/
Source0:	http://jengelh.medozas.de/files/geoip/geoip_src.tar.bz2
# Source0-md5:	bbcb1edd6ce2ece229d3e61173c7cadc
Source1:	http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
# Source1-md5:	14d2a5c6845f4e3df46c992ffca209d9
Source2:	http://geolite.maxmind.com/download/geoip/database/LICENSE.txt
# Source2-md5:	a1381bd1aa0a0c91dc31b3f1e847cf4a
BuildRequires:	perl-Text-CSV_XS >= 0.69
BuildRequires:	perl-base
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dbdir	/usr/share/xt_geoip

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
rm -f GeoIPCountryWhois.csv
%setup -qD -a1

ver=$(stat -c '%y' GeoIPCountryWhois.csv | awk '{print $1}' | tr -d -)
if [ "$ver" != %{version} ]; then
	exit 1
fi

cp -a %{SOURCE2} .

%build
install -d %{byteorder}
cd %{byteorder}
%if "%{byteorder}" == "BE"
%{__perl} ../geoip_csv_iv0.pl -b ../GeoIPCountryWhois.csv | tee ../ranges.txt
%else
%{__perl} ../geoip_csv_iv0.pl ../GeoIPCountryWhois.csv | tee ../ranges.txt
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
