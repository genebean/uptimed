Summary:	A daemon to record and keep track of system uptimes
Name:		uptimed
Version:	0.3.17
Release:	0.3
License:	GPLv2
Group:		System Environment/Daemons
Source:		https://github.com/downloads/genebean/uptimed/%{name}-%{version}-%{release}.tar.gz
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	m4
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:	chkconfig >= 0.9

%description
Uptimed is an uptime record daemon keeping track of the highest 
uptimes the system ever had. Instead of using a pid file to 
keep sessions apart from each other, it uses the system boot 
time. 

Uptimed has the ability to inform you of records and milestones 
though syslog and e-mail, and comes with a console front end to 
parse the records, which can also easily be used to show your 
records on your Web page

%prep
%setup -q -n %{name}-%{version}-%{release}
autoreconf -ivf

%build
%configure
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
install -m 755 -d %{buildroot}/%_docdir/%{name}-%{version}/sample-cgi
install -m 644 sample-cgi/uprecords.* %{buildroot}/%_docdir/%{name}-%{version}/sample-cgi
install -m 755 -d %{buildroot}/etc/rc.d/init.d
install -m 755 etc/rc.uptimed %{buildroot}/etc/rc.d/init.d/uptimed
mv %{buildroot}/etc/uptimed.conf-dist $RPM_BUILD_ROOT/etc/uptimed.conf

%post
/sbin/ldconfig
install -m 755 -d /var/spool/uptimed
/sbin/chkconfig --add uptimed

if [ -f /etc/rc.d/rc.sysinit ]
then
	if [ ! `grep "/sbin/service uptimed createbootid" /etc/rc.d/rc.sysinit > /dev/null` ]
	then
		echo "/sbin/service uptimed createbootid" >> /etc/rc.d/rc.sysinit
	fi
else
echo
echo "Please add the following line to your rc.sysinit script"
echo "/sbin/service uptimed createbootid"
echo
fi

%postun
/sbin/ldconfig

%preun
/sbin/chkconfig --del uptimed

if [ -f /etc/rc.d/rc.sysinit ]
then
	grep -v "/sbin/service uptimed createbootid" /etc/rc.d/rc.sysinit > /tmp/rc.sysinit.$$ && mv /tmp/rc.sysinit.$$ /etc/rc.d/rc.sysinit
	chmod 755 /etc/rc.d/rc.sysinit
else
echo
echo "Please remove the following line to your rc.sysinit script"
echo "/sbin/service uptimed createbootid"
echo
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING CREDITS ChangeLog INSTALL INSTALL.cgi INSTALL.upgrade README README.unsupported TODO sample-cgi/
%config(noreplace) /etc/uptimed.conf
%config /etc/rc.d/init.d/uptimed
%{_sbindir}/uptimed
%{_bindir}/uprecords
%{_mandir}/*/*
%{_libdir}/libuptimed.*

%changelog
* Tue Mar 27 2012 Gene Liverman <gliverman@gmail.com> - 0.3.17-0.3
- Replaced uptime.spec.in with uptime.spec
- Replaced $RPM_BUILD_ROOT with %{buildroot} throughout uptime.spec
- Fixed prep section so that it knows how the tarball unpacks.

* Tue Mar 27 2012 Gene Liverman <gliverman@gmail.com>
- Based on output from autoreconf -ivf I made the following changes:
- Added BuildRequire m4 to uptime.spec.in
- Created directory m4
- Added `AC_CONFIG_MACRO_DIR([m4])' to configure.ac
- Added `-I m4' to ACLOCAL_AMFLAGS in Makefile.am
- Changed src/Makefile.am:17: `CFLAGS' to `AM_CFLAGS'

* Sat Sep 17 2011 Gene Liverman <gliverman@gmail.com>
- Changed source location
- Changed license to match what is actually in the source
- Changed version and release to 0.3.17-0.1

* Tue May 14 2002 Brett Pemberton <generica@email.com>
- Reset release to 0 for uptimed-2.0
- Change source location

* Sat Mar 16 2002 Brett Pemberton <generica@email.com>
- Add /etc/rc.d/init.d/uptimed
- Use chkconfig

* Wed Mar 13 2002 Brett Pemberton <generica@email.com>
- Automate rc.{sysinit,local} add/remove
- Warn if rc.{sysinit,local} not found

* Fri Dec 21 2001 Brett Pemberton <generica@email.com>
- Handle sample-cgi dir properly
- Install uptimed.conf properly
- Install /var/spool/uptimed
- Warn user to finish configuring

* Thu Dec 20 2001 Brett Pemberton <generica@email.com>
- Initial spec-file

