%global debug_package %{nil}

Name:           dbgl
Summary:        DOSBox Game Launcher
URL:            http://home.quicknet.nl/qn/prive/blankendaalr/dbgl/
Version:        0.90
%global         uversion  %(foo=%{version}; echo ${foo//./})
Release:        1%{?dist}
License:        GPLv2
BuildRequires:  ant
BuildRequires:  eclipse-swt
BuildRequires:  hsqldb1
BuildRequires:  desktop-file-utils
BuildRequires:  java-devel
BuildRequires:  apache-commons-lang3
BuildRequires:  apache-commons-io
BuildRequires:  libappstream-glib
#BuildRequires:  jersey
#BuildRequires:  glassfish-jax-rs-api
#BuildRequires:  glassfish-hk2-utils
#BuildRequires:  glassfish-hk2-configuration
#BuildRequires:  glassfish-hk2-metadata-generator
#BuildRequires:  glassfish-hk2-hk2
Requires:       dosbox >= 0.70
Requires:       eclipse-swt
Requires:       hsqldb1
Requires:       java >= 1:1.8.0
Requires:       java-headless >= 1:1.8.0
Requires:       jpackage-utils
Requires:       SDL_net
Requires:       SDL_sound
Source0:        http://members.quicknet.nl/blankendaalr/dbgl/download/src%{uversion}.zip
Source1:        dbgl.desktop
Source2:        dbgl.appdata.xml

%description
DBGL is a Java front-end for DOSBox, based largely upon the proven
interface of D-Fend.
The front-end is by no means finished. It is a work in progress
and lacking many features, but the core is working, and I think
the product is somewhat usable as it is. Please bear in mind that
the interface is still quite rough around the edges.

%prep
%setup -qc
# remove bundles
# swt
rm -r ./src/dist/linuxshared/lib
rm -r ./src/dist/macshared
rm -r ./src/dist/winshared
rm -r ./src/dist/shared/lib/hsqldb.jar
rm -r ./src/dist/shared/lib/commons-lang3-*.jar
rm -r ./src/dist/shared/lib/commons-io-*.jar
# not easy unbundle jersey-2.13.jar fedora have jersey-2.18 and 2.23 seems that
# haven't org.glassfish.jersey.core.jersey-server
#rm -r ./src/dist/shared/lib/jersey-2.13.jar
#rm -r ./src/dist/shared/lib/jersey-2.27.0.jar


%build
mkdir -p lib
build-jar-repository -s -p lib commons-io commons-lang3 hsqldb1-1 swt
#    glassfish-jax-rs-api jersey glassfish-hk2-utils \
#    glassfish-hk2-configuration glassfish-hk2/hk2-metadata-generator \
#    glassfish-hk2-hk2

# fix build.xml clean all swt.*64.jar
sed -i '/swt.*64.jar/d' build.xml

ant distlinux

%install
install -dm 755 %{buildroot}%{_javadir}/%{name}/
tar xvf dist/dbgl%{uversion}.tar.gz -C %{buildroot}%{_javadir}/%{name}/

# use symbol links to system libraries
build-jar-repository -s -p %{buildroot}/%{_javadir}/%{name}/lib commons-io \
    commons-lang3 hsqldb1-1 swt

# startscript
mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_bindir}
ln -s %{_javadir}/%{name}/dbgl
popd

# icons
mkdir %{buildroot}%{_datadir}/pixmaps
mv %{buildroot}%{_javadir}/%{name}/dbgl.png %{buildroot}%{_datadir}/pixmaps/

# menu
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install                               \
--dir=%{buildroot}%{_datadir}/applications         \
%{SOURCE1}

install -D -p -m 0644 %{SOURCE2} \
    %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%check
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%files
%{_bindir}/%{name}
%{_javadir}/%{name}
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Wed Dec 25 2019 Sérgio Basto <sergio@serjux.com> - 0.90-1
- Update to 0.90

* Sun Nov 05 2017 Sérgio Basto <sergio@serjux.com> - 0.82-1
- Updated to 0.82

* Thu Mar 09 2017 Sérgio Basto <sergio@serjux.com> - 0.81-1
- Update to 0.81

* Fri Dec 23 2016 Sérgio Basto <sergio@serjux.com> - 0.80-3
- set jar classpath with (unbundle) system libraries (instead use symbol links)
- gnatenkobrain review:
  - btw, you can remove / between %{buildroot} and others.
  - probably you meant %{ix86}
  - to %check please

* Mon Dec 19 2016 Sérgio Basto <sergio@serjux.com> - 0.80-2
- Bump release
- Use external .desktop file easier to send to upstream
- Add Packaging:AppData

* Fri Jun 17 2016 Oleg Kishinskiy <legunt@yandex.ru> - 0.80-1
- Update for new vertion

* Fri Mar 20 2015 Oleg Kishinskiy <legunt@yandex.ru> - 0.79-3
- add ant for BuildRequires

* Fri Mar 20 2015 Oleg Kishinskiy <legunt@yandex.ru> - 0.79-2
- FIX change category

* Fri Mar 20 2015 Oleg Kishinskiy <legunt@yandex.ru> - 0.79-1
- update for new vertion
- change category

* Tue Dec 23 2014 Oleg Kishinskiy <legunt@yandex.ru> - 0.78-3
- fix spec to install from source

* Wed Dec 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.78-2
- spec cleanup

* Wed Dec 10 2014 Oleg Kishinskiy <legunt@yandex.ru> - 0.78-1
- Update for new vertion

* Mon Jul 29 2013 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.76-2
- Initial build rpm 
