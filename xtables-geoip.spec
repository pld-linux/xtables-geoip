Summary:	GeoIP database files for xt_geoip
Summary(pl.UTF-8):	Pliki baz danych GeoIP dla xt_geoip
Name:		xtables-geoip
Version:	20181023
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

%ifarch ppc ppc64 s390 s390x sparc sparc64 sparcv9
%define		byteorder	BE
%else
%define		byteorder	LE
%endif

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

ver=$(ls -d GeoLite2-Country-CSV_* | head -1 | %{__sed} 's/^GeoLite2-Country-CSV_//')
if [ "$ver" != %{version} ]; then
	exit 1
fi

cp -p %{SOURCE1} .

%build
%{__mkdir} %{byteorder}
%{__perl} %{SOURCE2} -S GeoLite2-Country-CSV_%{version} -D %{byteorder} > ranges.txt

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
# kernel-net-xtables-addons-1.18-8@2.6.27.45_1.i686  searches from /var/lib:
# Could not open /var/lib/geoip/LE/EE.iv0: No such file or directory
install -d $RPM_BUILD_ROOT/var/lib
ln -s %{_datadir}/xt_geoip $RPM_BUILD_ROOT/var/lib/geoip
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if "%{pld_release}" == "ac"
%pretrans
# this needs to be a symlink
if [ -d /var/lib/geoip -a ! -L /var/lib/geoip ]; then
	mv -f /var/lib/geoip{,.rpmsave}
	install -d %{dbdir}
	ln -s %{dbdir} /var/lib/geoip
fi
%endif

%files
%defattr(644,root,root,755)
%doc LICENSE.txt ranges.txt
%dir %{dbdir}
%{dbdir}/%{byteorder}

%if "%{pld_release}" == "ac"
/var/lib/geoip
%endif
