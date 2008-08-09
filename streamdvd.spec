%{!?perl_vendorarch: %define perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}
Name:           streamdvd
Version:        0.4
Release:        7%{?dist}
Summary:        A fast tool to backup Video DVDs

Group:          Applications/Multimedia 
License:        GPL
URL:            http://www.badabum.de/streamdvd.html 
Source0:        http://www.badabum.de/down/streamdvd-0.4.tar.gz
Patch0:         streamdvd-makefile.patch
Patch1:         streamdvd-streamdvd.patch
Patch2:         streamdvd-lsdvd.patch
Patch3:         streamdvd-gui.patch
Patch4:         streamdvd-gcc41.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  libdvdread-devel >= 0.9.2
BuildRequires:  perl

%package streamanalyze
Summary: Factor-Calculator for streamdvd
Group: Applications/Multimedia 
Requires: %{name} = %{version}-%{release}

%package gui
Summary: Graphical user interface for streamdvd
Group: User Interface/X
Requires: %{name} = %{version}-%{release}
Requires: %{name}-streamanalyze = %{version}-%{release}
Requires: dvdauthor >= 0.6.5
Requires: mkisofs >= 1.15
Requires: dvd+rw-tools >= 5.13.4.7.4
Requires: perl(Tk) perl(Tk::BrowseEntry) perl(Tk::Photo) perl(Tk::JPEG)

%description
StreamDVD is a fast tool to backup Video DVDs 'on the fly', there
will be no ripping, demultiplexing, recoding, remultiplexing ....
You can select the wanted title, chapters, video, audio and subpicture streams
and also a resize factor and StreamDVD will write a 'ready to author' vob file
to stdout. 

%description streamanalyze
StreamAnalyze is a little helper for people using StreamDVD to backup movies.
Giving the video/audio/subpicture tracks you want to save StreamAnalyze will
calculate if the backup would fit on a dvd-r and, if not, prints a shrink factor
to reduce the video size.

%description gui
Graphical user interface for streamdvd

%prep
%setup -q -n StreamDVD-%{version}
%patch0
%patch1
%patch2
%patch3
%patch4 -p1

%{__perl} -pi -e 's/(Tk::JPEG)::Lite/$1/' \
%{_builddir}/StreamDVD-%{version}/Gui/StreamDVD/Gui.pm

%build
make gui CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_bindir}
%{__mkdir_p} $RPM_BUILD_ROOT%{perl_vendorarch}/StreamDVD

#install streamdvd, streamanalyze and lsdvd
make install INSTALLDIR=$RPM_BUILD_ROOT%{_bindir}

#install modules for gui
%{__install} %{_builddir}/StreamDVD-%{version}/Gui/StreamDVD/*.pm \
$RPM_BUILD_ROOT%{perl_vendorarch}/StreamDVD/

#install gui
%{__install} %{_builddir}/StreamDVD-%{version}/Gui/StreamDVD.pl \
$RPM_BUILD_ROOT%{_bindir}/StreamDVD


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README COPYING
%{_bindir}/streamdvd

%files streamanalyze
%defattr(-,root,root,-)
%doc contrib/StreamAnalyze/README contrib/StreamAnalyze/COPYING
%doc contrib/lsdvd/AUTHORS contrib/lsdvd/COPYING contrib/lsdvd/README
%{_bindir}/streamanalyze
%{_bindir}/lsdvd

%files gui
%defattr(-,root,root,-)
%doc Gui/README
%{_bindir}/StreamDVD
%{perl_vendorarch}/StreamDVD

%changelog
* Sat Aug 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 0.4-7
- rebuild for RPM Fusion

* Sat Mar 18 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.4-6
- remove -dl workaround

* Thu Mar 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.4-5
- fix #802 (devel build)

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Jan 23 2006 Adrian Reber <adrian@lisas.de> - 0.4-0.lvn.4
- added gcc 4.1 compile patch

* Mon Jul 11 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.4.0.lvn.3
- install StreamDVD gui without .pl suffix

* Sun Jun 26 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.4.0.lvn.2
- fix some perl related stuff
- get rid of Tk::JPEG::Lite

* Tue Jun 14 2005 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.4-0.lvn.1
- Initial Release
