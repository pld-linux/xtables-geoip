Summary:	GeoIP database files for xt_geoip
Summary(pl.UTF-8):	Pliki baz danych GeoIP dla xt_geoip
Name:		xtables-geoip
Version:	20181030
Release:	1
License:	GPL, Open Data License
Group:		Networking/Admin
Source0:	http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip
# Source0-md5:	1f5524d5ac54a779831bffc57d91e2a2
Source1:	http://geolite.maxmind.com/download/geoip/database/LICENSE.txt
# Source1-md5:	a1381bd1aa0a0c91dc31b3f1e847cf4a
Source2:	http://sourceforge.net/p/xtables-addons/xtables-addons/ci/master/tree/geoip/xt_geoip_build?format=raw&/xt_geoip_build
# Source2-md5:	462ca00be38471d19dc6e0f32c098275
URL:		http://www.maxmind.com/
BuildRequires:	perl-Text-CSV_XS >= 0.69
BuildRequires:	perl-base
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dbdir	/usr/share/xt_geoip

# no debuginfo to package
%define		_enable_debug_packages	0

%description
The package contains the GeoIP definition files (which IP addresses
belong to which country) that are needed for Xtables-addons's xt_geoip
module.

%description -l pl.UTF-8
Ten pakiet zawiera pliki definicji GeoIP (określające, które adresy IP
należą do jakiego kraju), wymagane przez moduł xt_geoip z pakietu
xtables-addons.

%prep
%setup -qc

ver=$(echo GeoLite2-Country-CSV_*)
ver=${ver#GeoLite2-Country-CSV_}
if [ "$ver" != %{version} ]; then
	exit 1
fi

cp -p %{SOURCE1} .

%build
%{__mkdir} out
%{__perl} %{SOURCE2} -S GeoLite2-Country-CSV_%{version} -D out > ranges.txt

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dbdir}
cp -a out/* $RPM_BUILD_ROOT%{dbdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.txt ranges.txt
%{dbdir}
