%define major 0
%define libname %mklibname ldmgreeter %{major}
%define develname %mklibname ldmgreeter -d

Summary:	A lightweight display manager
Name:		lightdm
Version:	0.1.1
Release:	%mkrel 2
License:	GPLv3
Group:		System/X11
Url:		https://launchpad.net/lightdm
Source0:	http://people.ubuntu.com/~robert-ancell/lightdm/releases/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Source2:	35%{name}.conf
Patch0:		lightdm-0.1.1-fix-undefined-reference.patch
BuildRequires:	perl(XML::Parser)
BuildRequires:	consolekit-devel
BuildRequires:	pam-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	libxcb-devel
BuildRequires:	libxklavier-devel
BuildRequires:	glib2-devel
BuildRequires:	gtk2-devel
BuildRequires:	webkitgtk-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool
Requires:	%{libname} = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
An X display manager that:
* Has a lightweight codebase
* Is standards compliant (PAM, ConsoleKit, etc)
* Has a well defined interface between the server and user interface
* Fully themeable (easiest with the webkit interface)
* Cross-desktop (greeters can be written in any toolkit)

%package -n %{libname}
Summary:	Main library for %{name}
Group:		System/Libraries

%description -n %{libname}
Greeter library for %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Provides:	%{name}-devel
Requires:	%{libname} = %{version}-%{release}

%description -n %{develname}
Development files and headers for %{name}.

%prep
%setup -q
%patch0 -p1

%build
%configure2_5x \
	--enable-console-kit=yes \
	--without-default-session \
	--enable-introspection=yes \
	--with-xsession-dir="%{_sysconfdir}/X11/wmsession.d" \
	--disable-gtk-doc \
	--disable-static

%make

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
%makeinstall_std

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

mkdir -p %{buildroot}%{_datadir}/X11/dm.d
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/X11/dm.d/35%{name}.conf

#(tpg) wtf is this
rm -rf %{buildroot}%{_libdir}/girepository-1.0/LightDMGreeter-1.typelib
rm -rf %{buildroot}%{_datadir}/gir-1.0/LightDMGreeter-1.gir

#(tpg) get rid of these
rm -rf %{buildroot}%{_libdir}/lib*.*a

%find_lang %{name}

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog NEWS
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/themes
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_datadir}/X11/dm.d/35%{name}.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.LightDisplayManager.conf
%{_bindir}/%{name}
%{_libdir}/ldm-gtk-greeter
%{_libdir}/ldm-webkit-greeter
#%{_datadir}/gir-1.0/LightDMGreeter-1.gir
%{_datadir}/%{name}/themes/gnome*
%{_datadir}/%{name}/themes/webkit*
%{_mandir}/man1/lightdm.1.*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%dir %{_includedir}/%{name}-1.0
%dir %{_includedir}/%{name}-1.0/%{name}
%dir %{_datadir}/gtk-doc/html/ldmgreeter
%{_libdir}/lib*.so
%{_includedir}/%{name}-1.0/%{name}/*.h
%{_datadir}/gtk-doc/html/ldmgreeter/*
%{_libdir}/pkgconfig/libldmgreeter-1.pc
