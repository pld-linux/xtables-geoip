Summary:	GeoIP database files for xt_geoip
Name:		xtables-geoip
Version:	20101204
Release:	1
License:	GPL, Open Data License
Group:		Networking/Admin
URL:		http://www.maxmind.com/
Source0:	http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
# Source0-md5:	2bd9c15b470fe72d6b6be2a32138cc29
Source1:	http://geolite.maxmind.com/download/geoip/database/LICENSE.txt
# Source1-md5:	a1381bd1aa0a0c91dc31b3f1e847cf4a
Source2:	http://xtables-addons.git.sf.net/git/gitweb.cgi?p=xtables-addons/xtables-addons;a=blob_plain;f=geoip/geoip_build_db.pl
# Source2-md5:	7cd5c1ab1d83a94d84ae918f0805603f
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

cp -a %{SOURCE1} .

%build
install -d %{byteorder}
%if "%{byteorder}" == "BE"
%{__perl} %{SOURCE2} -D %{byteorder} -b ../GeoIPCountryWhois.csv | tee ranges.txt
%else
%{__perl} %{SOURCE2} -D %{byteorder} GeoIPCountryWhois.csv | tee ranges.txt
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
