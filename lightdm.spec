%define	dm_user	lightdm
%define greeter_session	lightdm-gtk-greeter

%define	api 1
%define	qt_api 2
%define	major 0
%define	libgobject		%mklibname %{name}-gobject %{api} %{major}
%define	develgobject	%mklibname %{name}-gobject -d
%define	libqt 			%mklibname %{name}-qt %{qt_api} %{major}
%define	develqt 		%mklibname %{name}-qt -d

Name:		lightdm
Version:	1.1.9
Release:	1
Summary:	A lightweight display manager
Group:		System/X11
License:	GPLv3
URL:		https://launchpad.net/lightdm
Source0:	https://launchpad.net/lightdm/+download/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
Source2:	35%{name}.conf

BuildRequires: gnome-common
BuildRequires: gtk-doc
BuildRequires: intltool >= 0.35.0
BuildRequires: vala-tools
BuildRequires: gettext-devel
BuildRequires: pam-devel
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: pkgconfig(gio-2.0) >= 2.26
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gmodule-export-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: pkgconfig(gobject-introspection-1.0) >= 0.9.5
BuildRequires: pkgconfig(libxklavier)
BuildRequires: pkgconfig(QtCore)
BuildRequires: pkgconfig(QtDBus)
BuildRequires: pkgconfig(QtGui)
BuildRequires: pkgconfig(QtNetwork)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xcb)
BuildRequires: pkgconfig(xdmcp)

Suggests: lightdm-greeter
Requires(pre,postun): rpm-helper

%description
LightDM is an X display manager that:
* Has a lightweight codebase
* Is standards compliant (PAM, ConsoleKit, etc)
* Has a well defined interface between the server and user interface
* Fully themeable (easiest with the webkit interface)
* Cross-desktop (greeters can be written in any toolkit)
  
%package -n %{libgobject}
Summary:	LightDM GObject client library
Group:		System/Libraries
Obsoletes:	%{_lib}ldmgreeter0

%description -n %{libgobject}
A GObject based library for LightDM clients to use to interface with LightDM.

%package -n %{develgobject}
Summary:	The GObject development files for %{name}
Group:		Development/C
Requires:	%{libgobject} = %{version}
Obsoletes:	%{_lib}ldmgreeter-devel

%description -n %{develgobject}
The GObject development files and headers for %{name}.

%package -n %{libqt}
Summary:	LightDM Qt client library
Group:		System/Libraries

%description -n %{libqt}
A Qt based library for LightDM clients to use to interface with LightDM.

%package -n %{develqt}
Summary:	The QT development files for %{name}
Group:		Development/C++
Requires:	%{libqt} = %{version}

%description -n %{develqt}
The QT development files and headers for %{name}.

%prep
%setup -q

%build
NOCONFIGURE=yes gnome-autogen.sh

%configure2_5x \
	--disable-static \
	--with-greeter-user=%{dm_user} \
	--with-greeter-session=%{greeter_session}

%make LIBS='-lgmodule-2.0 -lglib-2.0'

%install
rm -rf %{buildroot}
%makeinstall_std

# make lightdm user home
mkdir -p %{buildroot}%{_var}/lib/%{name}

install -D -m0755 utils/gdmflexiserver %{buildroot}%{_libexecdir}/%{name}/gdmflexiserver

# remove apparmor stuff
rm -f %{buildroot}%{_sysconfdir}/apparmor.d/lightdm-guest-session

# pam needed for authentication
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}

# dm.d conf so lightdm with start if no other dm is present
mkdir -p %{buildroot}%{_datadir}/X11/dm.d
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/X11/dm.d/35%{name}.conf

%find_lang %{name} %{name}.lang

%pre
%_pre_useradd %{dm_user} %{_var}/lib/%{name} /bin/false
%_pre_groupadd xgrp %{dm_user}

%postun
%_postun_userdel %{dm_user}
%_postun_groupdel xgrp %{dm_user}

%files -f %{name}.lang
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/keys.conf
%config(noreplace) %{_sysconfdir}/%{name}/lightdm.conf
%config(noreplace) %{_sysconfdir}/%{name}/users.conf
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_datadir}/X11/dm.d/35%{name}.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_sysconfdir}/init/%{name}.conf
%{_bindir}/dm-tool
%{_sbindir}/%{name}
%{_libexecdir}/lightdm/*
%{_mandir}/man1/%{name}.1*
%attr(770, %{dm_user}, %{dm_user}) %dir %{_var}/lib/%{name}

%files -n %{libgobject}
%{_libdir}/liblightdm-gobject-%{api}.so.%{major}*
%{_libdir}/girepository-1.0/LightDM-%{api}.typelib

%files -n %{develgobject}
%{_includedir}/%{name}-gobject-1/
%{_libdir}/pkgconfig/liblightdm-gobject-%{api}.pc
%{_libdir}/liblightdm-gobject-%{api}.so
%{_datadir}/gtk-doc/html/%{name}-gobject-%{api}/*
%{_datadir}/gir-1.0/LightDM-%{api}.gir
%{_datadir}/vala/vapi/liblightdm-gobject-%{api}.vapi

%files -n %{libqt}
%{_libdir}/liblightdm-qt-%{qt_api}.so.%{major}*

%files -n %{develqt}
%{_includedir}/lightdm-qt-%{qt_api}
%{_libdir}/liblightdm-qt-%{qt_api}.so
%{_libdir}/pkgconfig/liblightdm-qt-%{qt_api}.pc
