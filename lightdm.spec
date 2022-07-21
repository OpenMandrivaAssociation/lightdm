%define url_ver %(echo %{version}|cut -d. -f1,2)

%define api 1
%define qtapi 3
%define major 0

%define liblightdmqt5devel %mklibname -d lightdm-qt5
%define liblightdmqt5 %mklibname lightdm-qt5_ %{qtapi} %{major}

Summary:	The Light Display Manager
Name:		lightdm
Version:	1.32.0
Release:	1
License:	GPLv3+
Group:		Graphical desktop/Other
Url:		http://www.freedesktop.org/wiki/Software/LightDM
Source0:	https://github.com/CanonicalLtd/%{name}/releases/download/%{version}/%{name}-%{version}.tar.xz
Source1:	29lightdm.conf
Source2:	Xsession
# specific settings overrides
Source3:	lightdm-settings.conf
# For autologin configuration via drakboot
Source4:	lightdm-autologin-config.conf
# Systemd related:
Source10:	lightdm-tmpfiles.conf
Source11:	lightdm.service
Source12:	lightdm.rules
Source13:	lightdm-users.conf
# PAM configs stolen from gdm
Source20:	lightdm.pam
Source21:	lightdm-autologin.pam
Source22:	lightdm-greeter.pam
# mga patches:
#Patch3:		lightdm-1.8.3-remove-bin-from-path.patch
# originally from Fedora:
Patch10:	lightdm-1.11.7-nodaemon_option.patch
BuildRequires:	intltool
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	pam-devel
BuildRequires:	yelp-tools
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(audit)
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gobject-2.0)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libxklavier)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(libgcrypt)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(vapigen)

Requires:	typelib(LightDM)
Requires:	lightdm-greeter
Requires:	accountsservice

Requires(post,postun,preun):	rpm-helper

Suggests:	light-locker

Provides:	dm

%description
An X display manager that:
  * Has a lightweight codebase
  * Is standards compliant (PAM, etc)
  * Has a well defined interface between the server and user interface
  * Fully themeable (easiest with the webkit interface)
  * Cross-desktop (greeters can be written in any toolkit)

%files -f %{name}.lang
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/%{name}.conf.d/
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf.d/50-%{_vendor}-autologin.conf
%{_sysconfdir}/%{name}/Xsession
%config(noreplace) %{_sysconfdir}/%{name}/keys.conf
%config(noreplace) %{_sysconfdir}/%{name}/lightdm.conf
%config(noreplace) %{_sysconfdir}/%{name}/users.conf
%config(noreplace) %{_sysconfdir}/pam.d/lightdm*
%dir %{_logdir}/%{name}/
%ghost %{_logdir}/%{name}/%{name}.log
%attr(-,lightdm,lightdm) %dir %{_localstatedir}/lib/%{name}/
%attr(-,lightdm,lightdm) %dir %{_localstatedir}/lib/%{name}-data/
%{_datadir}/dbus-1/system.d/org.freedesktop.DisplayManager.conf
%{_datadir}/%{name}/
%{_datadir}/X11/dm.d/29lightdm.conf
%{_datadir}/accountsservice/interfaces/org.freedesktop.DisplayManager.AccountsService.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.DisplayManager.AccountsService.xml
%{_datadir}/polkit-1/rules.d/lightdm.rules
%{_datadir}/polkit-1/actions/org.freedesktop.DisplayManager.AccountsService.policy
%{_sbindir}/%{name}
%{_bindir}/dm-tool
%{_libexecdir}/lightdm-guest-session
%{_mandir}/man1/%{name}*
%{_mandir}/man1/dm-tool.*
%{_tmpfilesdir}/lightdm.conf
%{_unitdir}/lightdm.service
%{_datadir}/bash-completion/completions/dm-tool
%{_datadir}/bash-completion/completions/lightdm

#-------------------------------------------------------------------------

%define liblightdmgobject %mklibname lightdm-gobject %{api} %{major}

%package -n %{liblightdmgobject}
Summary:	LightDM GObject client library
Group:		Graphical desktop/Other
License:	LGPLv2+

%description -n %{liblightdmgobject}
A GObject based library for LightDM clients to use to interface with LightDM.

%files -n %{liblightdmgobject}
%{_libdir}/liblightdm-gobject-%{api}.so.%{major}*

#-------------------------------------------------------------------------

%define liblightdmgir %mklibname lightdm-gir %{api}

%package -n %{liblightdmgir}
Summary:	Typelib file for liblightdm-1
Group:		Graphical desktop/Other
License:	LGPLv2+
Requires:	%{liblightdmgobject} = %{version}-%{release}

%description -n %{liblightdmgir}
A GObject based library for LightDM clients to use to interface with LightDM.

%files -n %{liblightdmgir}
%{_libdir}/girepository-1.0/LightDM-%{api}.typelib

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
%doc %{_datadir}/gtk-doc/html/lightdm-gobject-%{api}
%{_includedir}/lightdm-gobject-%{api}/
%{_libdir}/liblightdm-gobject-%{api}.so
%{_libdir}/pkgconfig/liblightdm-gobject-%{api}.pc
%{_datadir}/gir-1.0/LightDM-%{api}.gir
%{_datadir}/vala/vapi/liblightdm-gobject-1.deps
%{_datadir}/vala/vapi/liblightdm-gobject-1.vapi
#-------------------------------------------------------------------------

%package -n %{liblightdmqt5}
Summary:	LightDM Qt5 client library
Group:		Graphical desktop/Other
License:	LGPLv2+

%description -n %{liblightdmqt5}
A Qt5 based library for LightDM clients to use to interface with LightDM.

%files -n %{liblightdmqt5}
%{_libdir}/liblightdm-qt5-%{qtapi}.so.%{major}*

#-------------------------------------------------------------------------

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
%{_includedir}/lightdm-qt5-%{qtapi}
%{_libdir}/liblightdm-qt5-%{qtapi}.so
%{_libdir}/pkgconfig/liblightdm-qt5-%{qtapi}.pc

#-------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

# for autoreconf (to make it happy)
sed -i '1iACLOCAL_AMFLAGS=-I m4' Makefile.am
autoreconf -vfi

%build
export PATH=%{_qt5_bindir}:$PATH
%configure \
	--disable-static \
	--disable-tests \
	--enable-introspection \
	--enable-liblightdm-gobject \
	--enable-liblightdm-qt5 \
	--disable-liblightdm-qt \
	--with-greeter-session=lightdm-greeter \
	--enable-vala

%make_build

%install
%make_install

# dm config
install -Dpm644 %{SOURCE1} %{buildroot}/%{_datadir}/X11/dm.d/29lightdm.conf

# session wrapper script to source /etc/profile and ~/.profile if they exists
install -Dpm755 %{SOURCE2} %{buildroot}/%{_sysconfdir}/%{name}/Xsession

# will be created when lightdm starts
install -d %{buildroot}%{_logdir}/%{name}
touch %{buildroot}%{_logdir}/%{name}/%{name}.log

# directory for remote sessions
mkdir -p %{buildroot}%{_datadir}/%{name}/remote-sessions

# distro specific config overrides
rm -rf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
rm -rf %{buildroot}%{_sysconfdir}/%{name}/users.conf
install -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -m644 %{SOURCE13} %{buildroot}%{_sysconfdir}/%{name}/users.conf

# autologin config file for drakboot
install -Dpm644 %{SOURCE4} %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf.d/50-%{_vendor}-autologin.conf

# for systemd
install -Dpm 644 %{SOURCE10} %{buildroot}%{_tmpfilesdir}/lightdm.conf
install -Dpm 644 %{SOURCE11} %{buildroot}%{_unitdir}/lightdm.service
install -Dpm 644 %{SOURCE12} %{buildroot}%{_datadir}/polkit-1/rules.d/lightdm.rules

# pam configs stolen from gdm
rm -rf %{buildroot}%{_sysconfdir}/pam.d/
install -Dpm 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -Dpm 644 %{SOURCE21} %{buildroot}%{_sysconfdir}/pam.d/%{name}-autologin
install -Dpm 644 %{SOURCE22} %{buildroot}%{_sysconfdir}/pam.d/%{name}-greeter

#home dir for lightdm user
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}

#for user data dir
mkdir -p %{buildroot}%{_localstatedir}/lib/%{name}-data

#we don't want these
rm -rf %{buildroot}%{_sysconfdir}/{init,apparmor.d}/

# locales
%find_lang %{name} --with-gnome --all-name

%pre
%_pre_useradd %{name} %{_localstatedir}/lib/%{name} /bin/nologin

%post
%create_ghostfile %{_logdir}/%{name}/%{name}.log root root 0600
