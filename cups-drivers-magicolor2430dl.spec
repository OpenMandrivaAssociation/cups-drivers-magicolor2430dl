%define rname magicolor2430dl

Summary:	Cups Driver for KONICA MINOLTA magicolor 2430 DL
Name:		cups-drivers-%{rname}
Version:	1.6.1
Release:	14
License:	GPLv2
Group:		System/Printing
URL:		http://printer.konicaminolta.net/
Source0:	magicolor2430DL-%{version}.tar.gz
Patch0:		magicolor2430DL-shared_system_libs.diff
Patch1:		magicolor-automake-1.13.patch

BuildRequires:	cups-devel
BuildRequires:	jbig-devel
BuildRequires:	pkgconfig(lcms)
Requires:	cups

%description
This package contains KONICA MINOLTA CUPS LavaFlow stream(PCL-like) filter
rastertokm2430dl and the PPD file. The filter converts CUPS raster data to
KONICA MINOLTA LavaFlow stream.

This package contains CUPS drivers (PPD) for the following printers:

 o KONICA MINOLTA magicolor 2430 DL printer

%prep

%setup -q -n magicolor2430DL-%{version}
%patch0 -p0
%patch1 -p1 -b .am113~

# Fix copy of CUPS headers in kmlf.h
perl -pi -e 's:\bcups_strlcpy:_cups_strlcpy:g' src/kmlf.h

# Remove asterisks from group names in PPD file
gzip -dc src/km_en.ppd.gz | perl -p -e 's/(Group:\s+)\*/$1/g' | gzip > src/km_en.tmp.ppd.gz && mv -f src/km_en.tmp.ppd.gz src/km_en.ppd.gz

# Add support for the magicolor 2300 DL
gzip -dc src/km_en.ppd.gz | perl -p -e 's:2430(\s*DL):2300$1:g' | gzip > src/km2300dl.ppd.gz

# Determine the directory for the CUPS filters using the correct method
perl -pi -e 's:(CUPS_SERVERBIN)="\$libdir/cups":$1`cups-config --serverbin`:' configure*

rm -f configure
autoreconf -fi

%build
%configure2_5x

%make

%install

%makeinstall_std

%files
%doc AUTHORS COPYING ChangeLog
%{_prefix}/lib/cups/filter/rastertokm2430dl
%{_datadir}/KONICA_MINOLTA/mc2430DL
%{_datadir}/cups/model/KONICA_MINOLTA/km2430dl.ppd*

