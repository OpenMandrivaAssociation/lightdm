%define greeter_session lightdm-greeter
%define libapi		1
%define libqtapi	3
%define libmajor	0
%bcond_with 	qt5


Summary:	The Light Display Manager
Name:		lightdm
Version:	1.9.6
Release:	1
License:	GPLv3+
Group:		Graphical desktop/Other
Source0:	https://launchpad.net/lightdm/1.9/%{version}/+download/%{name}-%{version}.tar.xz
Source1:	29lightdm.conf
Source2:	Xsession
#Systemd related:
Source10:	lightdm-tmpfiles.conf
Source11:	lightdm.service
Source12:	lightdm.rules
# omv/mdv patches:
Patch1:		lightdm-1.7.4-omv-config.patch
Patch2:		lightdm-1.7.9-pam-modules.patch
Patch3:		lightdm-1.7.0-remove-bin-from-path.patch
# originally from Fedora:
Patch10:	lightdm-1.7.0-nodaemon_option.patch
Patch11:	lightdm-1.7.0-lock-screen-before-switch.patch
URL:		http://www.freedesktop.org/wiki/Software/LightDM
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	gettext-devel
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	pam-devel
BuildRequires:	yelp-tools
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(QtCore) < 5.0.0
BuildRequires:	pkgconfig(QtDBus) < 5.0.0
BuildRequires:	pkgconfig(QtGui) < 5.0.0

%if %{with qt5}
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
%endif

BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(x11)
BuildRequires:	libgcrypt-devel
Requires:	lightdm-greeter
Requires:	accountsservice
Requires(pre,postun):   rpm-helper
Requires:	distro-theme-OpenMandriva
Provides:	dm


%description
An X display manager that:
  * Has a lightweight codebase
  * Is standards compliant (PAM, etc)
  * Has a well defined interface between the server and user interface
  * Fully themeable (easiest with the webkit interface)
  * Cross-desktop (greeters can be written in any toolkit)

#-------------------------------------------------------------------------

%define liblightdmgobject %mklibname lightdm-gobject %{libapi} %{libmajor}

%package -n %{liblightdmgobject}
Summary:	LightDM GObject client library
Group:		Graphical desktop/Other
License:	LGPLv2+

%description -n %{liblightdmgobject}
A GObject based library for LightDM clients to use to interface with LightDM.

%files -n %{liblightdmgobject}
%{_libdir}/liblightdm-gobject-%{libapi}.so.%{libmajor}
%{_libdir}/liblightdm-gobject-%{libapi}.so.%{libmajor}.*

#-------------------------------------------------------------------------

%define liblightdmgir %mklibname lightdm-gir %{libapi}

%package -n %{liblightdmgir}
Summary:	Typelib file for liblightdm-1
Group:		Graphical desktop/Other
License:	LGPLv2+
Requires:	%{liblightdmgobject} = %{version}-%{release}

%description -n %{liblightdmgir}
A GObject based library for LightDM clients to use to interface with LightDM.

%files -n %{liblightdmgir}
%{_libdir}/girepository-1.0/LightDM-%{libapi}.typelib

#-------------------------------------------------------------------------

%define liblightdmgobjectdevel %mklibname -d lightdm-gobject

%package -n %{liblightdmgobjectdevel}
Summary:	LightDM client library (development files)
Group:		Graphical desktop/Other
License:	LGPLv2+
Requires:	%{liblightdmgobject} = %{version}-%{release}
Provides:	lightdm-gobject-devel = %{version}-%{release}

%description -n %{liblightdmgobjectdevel}
A GObject based library for LightDM clients to use to interface with LightDM.

This package contains header files and development information, which
is useful for building LightDM greeters and user switchers.

%files -n %{liblightdmgobjectdevel}
%doc %{_datadir}/gtk-doc/html/lightdm-gobject-%{libapi}
%{_includedir}/lightdm-gobject-%{libapi}/
%{_libdir}/liblightdm-gobject-%{libapi}.so
%{_libdir}/pkgconfig/liblightdm-gobject-%{libapi}.pc
%{_datadir}/gir-1.0/LightDM-%{libapi}.gir
%{_datadir}/vala/vapi/liblightdm-gobject-%{libapi}.vapi

#-------------------------------------------------------------------------
%if %{with qt5}
%define liblightdmqt5 %mklibname lightdm-qt5_ %{libqtapi} %{libmajor}

%package -n %{liblightdmqt5}
Summary:	LightDM Qt5 client library
Group:		Graphical desktop/Other
License:	LGPLv2+

%description -n %{liblightdmqt5}
A Qt5 based library for LightDM clients to use to interface with LightDM.

%files -n %{liblightdmqt5}
%{_libdir}/liblightdm-qt5-%{libqtapi}.so.%{libmajor}
%{_libdir}/liblightdm-qt5-%{libqtapi}.so.%{libmajor}.*

#-------------------------------------------------------------------------

%define liblightdmqt5devel %mklibname -d lightdm-qt5

%package -n %{liblightdmqt5devel}
Summary:	LightDM client library (development files)
Group:		Graphical desktop/Other
License:	LGPLv2+
Requires:	%{liblightdmqt5} = %{version}-%{release}
Provides:	lightdm-qt5-devel = %{version}-%{release}

%description -n %{liblightdmqt5devel}
A Qt5 based library for LightDM clients to use to interface with LightDM.

This package contains header files and development information, which
is useful for building LightDM greeters and user switchers.

%files -n %{liblightdmqt5devel}
%{_includedir}/lightdm-qt5-%{libqtapi}
%{_libdir}/liblightdm-qt5-%{libqtapi}.so
%{_libdir}/pkgconfig/liblightdm-qt5-%{libqtapi}.pc

%endif
#-------------------------------------------------------------------------

%define liblightdmqt %mklibname lightdm-qt %{libqtapi} %{libmajor}

%package -n %{liblightdmqt}
Summary:        LightDM Qt client library
Group:          Graphical desktop/Other
License:        LGPLv2+

%description -n %{liblightdmqt}
A Qt based library for LightDM clients to use to interface with LightDM.

%files -n %{liblightdmqt}
%{_libdir}/liblightdm-qt-%{libqtapi}.so.%{libmajor}
%{_libdir}/liblightdm-qt-%{libqtapi}.so.%{libmajor}.*

#-------------------------------------------------------------------------

%define liblightdmqtdevel %mklibname -d lightdm-qt

%package -n %{liblightdmqtdevel}
Summary:        LightDM client library (development files)
Group:          Graphical desktop/Other
License:        LGPLv2+
Requires:	%{liblightdmqt} = %{version}-%{release}
Provides:	lightdm-qt-devel = %{version}-%{release}

%description -n %{liblightdmqtdevel}
A Qt based library for LightDM clients to use to interface with LightDM.

This package contains header files and development information, which
is useful for building LightDM greeters and user switchers.

%files -n %{liblightdmqtdevel}
%{_includedir}/lightdm-qt-%{libqtapi}
%{_libdir}/liblightdm-qt-%{libqtapi}.so
%{_libdir}/pkgconfig/liblightdm-qt-%{libqtapi}.pc

#-------------------------------------------------------------------------

%prep
%setup -q
%patch1 -p1 -b .omv
%patch2 -p1 -b .pamfix
%patch3 -p1 -b .path
%patch10 -p1 -b .nodaemon

# for autoreconf (to make it happy)
sed -i '1iACLOCAL_AMFLAGS=-I m4' Makefile.am

%build
autoreconf -vfi

export PATH=$PATH:%{qt4bin}
%configure2_5x \
	--disable-static \
	--disable-tests \
	--enable-introspection \
	--with-greeter-user=%{name} \
	--with-greeter-session=%{greeter_session} \
	--enable-liblightdm-gobject \
	--enable-liblightdm-qt \

%make

%install
%makeinstall_std

# make lightdm user home
mkdir -p %{buildroot}%{_var}/run/%{name}

# dm config
install -Dpm644 %{SOURCE1} %{buildroot}/%{_datadir}/X11/dm.d/29lightdm.conf

# session wrapper script to source /etc/profile and ~/.profile if they exists
install -Dpm755 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}/Xsession

# will be created when lightdm starts
install -d %{buildroot}%{_localstatedir}/log/%{name}
touch %{buildroot}%{_localstatedir}/log/%{name}/%{name}.log

# directory for remote sessions
mkdir -p %{buildroot}%{_datadir}/%{name}/remote-sessions

# for config overrides
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf.d

# for systemd
install -Dpm 644 %{SOURCE10} %{buildroot}%{_tmpfilesdir}/lightdm.conf
install -Dpm 644 %{SOURCE11} %{buildroot}%{_unitdir}/lightdm.service
install -Dpm 644 %{SOURCE12} %{buildroot}%{_datadir}/polkit-1/rules.d/lightdm.rules

#home dir for lightdm user
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

#we don't want these
find %{buildroot} -name "*.la" -delete
rm -rf %{buildroot}%{_sysconfdir}/{init,apparmor.d}/

%find_lang %{name}

%pre
%_pre_useradd %{name} %{_var}/run/%{name} /bin/false
%_pre_groupadd xgrp %{name}

%preun
%_preun_service %{name}

%post
%create_ghostfile %{_localstatedir}/log/%{name}/%{name}.log %{name} %{name} 0644
%tmpfiles_create %{name}
%_post_service %{name}

%postun
%_postun_userdel %{name}
%_postun_groupdel xgrp %{name}

%files -f %{name}.lang
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/%{name}.conf.d
%{_sysconfdir}/%{name}/Xsession
%config(noreplace) %{_sysconfdir}/%{name}/keys.conf
%config(noreplace) %{_sysconfdir}/%{name}/lightdm.conf
%config(noreplace) %{_sysconfdir}/%{name}/users.conf
%config(noreplace) %{_sysconfdir}/pam.d/lightdm*
%attr(770, %{name}, %{name}) %dir %{_var}/run/%{name}
%attr(-,lightdm,lightdm) %dir %{_localstatedir}/log/%{name}/
%ghost %{_localstatedir}/log/%{name}/%{name}.log
%attr(-,lightdm,lightdm) %dir %{_localstatedir}/lib/%{name}/
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_datadir}/X11/dm.d/29lightdm.conf
%{_datadir}/polkit-1/rules.d/lightdm.rules
%{_datadir}/%{name}/
%{_datadir}/help/C/%{name}/*
%{_sbindir}/%{name}
%{_bindir}/dm-tool
%{_libexecdir}/%{name}-guest-session
%{_mandir}/man1/%{name}*
%{_mandir}/man1/dm-*
%{_tmpfilesdir}/lightdm.conf
%{_unitdir}/lightdm.service
