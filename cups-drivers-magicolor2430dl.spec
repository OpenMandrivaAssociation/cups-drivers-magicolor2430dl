%define rname magicolor2430dl

Summary:	Cups Driver for KONICA MINOLTA magicolor 2430 DL
Name:		cups-drivers-%{rname}
Version:	1.6.1
Release:	%mkrel 14
License:	GPL
Group:		System/Printing
URL:		http://printer.konicaminolta.net/
Source0:	magicolor2430DL-%{version}.tar.gz
Patch0:		magicolor2430DL-shared_system_libs.diff
BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	jbig-devel
BuildRequires:	lcms-devel
Requires:	cups
Conflicts:	cups-drivers = 2007
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This package contains KONICA MINOLTA CUPS LavaFlow stream(PCL-like) filter
rastertokm2430dl and the PPD file. The filter converts CUPS raster data to
KONICA MINOLTA LavaFlow stream.

This package contains CUPS drivers (PPD) for the following printers:

 o KONICA MINOLTA magicolor 2430 DL printer

%prep

%setup -q -n magicolor2430DL-%{version}
%patch0 -p0

# Fix copy of CUPS headers in kmlf.h
perl -p -i -e 's:\bcups_strlcpy:_cups_strlcpy:g' src/kmlf.h

# Remove asterisks from group names in PPD file
gzip -dc src/km_en.ppd.gz | perl -p -e 's/(Group:\s+)\*/$1/g' | gzip > src/km_en.tmp.ppd.gz && mv -f src/km_en.tmp.ppd.gz src/km_en.ppd.gz

# Add support for the magicolor 2300 DL
gzip -dc src/km_en.ppd.gz | perl -p -e 's:2430(\s*DL):2300$1:g' | gzip > src/km2300dl.ppd.gz

# Determine the directory for the CUPS filters using the correct method
perl -p -i -e 's:(CUPS_SERVERBIN=)"\$libdir/cups":$1`cups-config --serverbin`:' configure*

%build
rm -f configure
libtoolize --force --copy; aclocal; automake --add-missing --copy --foreign; autoconf

%configure2_5x

%make

%install
rm -rf %{buildroot}

%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog
%{_prefix}/lib/cups/filter/rastertokm2430dl
%{_datadir}/KONICA_MINOLTA/mc2430DL
%attr(0644,root,root) %{_datadir}/cups/model/KONICA_MINOLTA/km2430dl.ppd*


%changelog
* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-13mdv2011.0
+ Revision: 663441
- mass rebuild

* Sun Jan 02 2011 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-12mdv2011.0
+ Revision: 627565
- don't force the usage of automake1.7

* Tue Nov 30 2010 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-11mdv2011.0
+ Revision: 603873
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-10mdv2010.1
+ Revision: 518845
- rebuild

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-9mdv2010.0
+ Revision: 413289
- rebuild

* Sat Jan 31 2009 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-8mdv2009.1
+ Revision: 335838
- rebuilt against new jbigkit major

* Tue Dec 23 2008 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-7mdv2009.1
+ Revision: 318073
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.6.1-6mdv2009.0
+ Revision: 220543
- rebuild

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 1.6.1-5mdv2008.1
+ Revision: 149151
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Thu Aug 30 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-4mdv2008.0
+ Revision: 75330
- fix deps (pixel)

* Wed Aug 22 2007 Thierry Vignaud <tv@mandriva.org> 1.6.1-3mdv2008.0
+ Revision: 69005
- fix description

* Thu Aug 16 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-2mdv2008.0
+ Revision: 64151
- use the new System/Printing RPM GROUP

* Mon Aug 13 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-1mdv2008.0
+ Revision: 62512
- Import cups-drivers-magicolor2430dl



* Mon Aug 13 2007 Oden Eriksson <oeriksson@mandriva.com> 1.6.1-1mdv2008.0
- initial Mandriva package
