Name:			dbgl
Summary:		DBGL - DOSBox Game Launcher
URL:			http://home.quicknet.nl/qn/prive/blankendaalr/dbgl/
Group:			Applications/Multimedia
Version:		0.78
Release:		1%{?dist}
BuildArch:		noarch
License:		GPL
BuildRequires:	eclipse-swt
BuildRequires:	hsqldb
BuildRequires:	jpackage-utils
BuildRequires:	p7zip
BuildRequires:	unzip
BuildRequires:	xerces-j2
Requires:		dosbox >= 0.70
Requires:		eclipse-swt
Requires:		hsqldb
Requires:		java >= 1.5
Requires:		jpackage-utils
Requires:		SDL_net
Requires:		SDL_sound
BuildRoot:		%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:		http://members.quicknet.nl/blankendaalr/dbgl/download/%{name}076_generic.tar.gz
Source2:		dbgl.png
Source3:		dbgl


BuildRequires:	liboil 

%description
DBGL is a Java front-end for DOSBox, based largely upon the proven
interface of D-Fend.

The front-end is by no means finished. It is a work in progress
and lacking many features, but the core is working, and I think
the product is somewhat usable as it is. Please bear in mind that
the interface is still quite rough around the edges.

Autor: Ronald Blankendaal <r.blankendaal@quicknet.nl>


%prep
%setup -c


%build


%install

# jars
%__install -dm 755 %{buildroot}%{_javadir}/%{name}/
cp -af * %{buildroot}/%{_javadir}/%{name}/


# startscript
%__install -dm 755 %{buildroot}%{_bindir}

install -m 644 %{SOURCE3} %{buildroot}%{_bindir}

# icons
%__install -dm 755 %{buildroot}%{_datadir}/pixmaps
%__install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/pixmaps/

# menu
%__install -dm 755 %{buildroot}%{_datadir}/applications
%__cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Exec=dbgl
Icon=/usr/share/pixmaps/dbgl.png
Terminal=false
Name=DOSBox Game Launcher
Comment=%{summary}
Categories=Utility;
EOF


%clean
rm -rf %{buildroot}

%files
%defattr(755, root, root)
%{_bindir}/%{name}
%{_javadir}/%{name}
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/%{name}.desktop


%changelog
* Mon Jul 29 2013 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.76-2
- Initial build rpm 
