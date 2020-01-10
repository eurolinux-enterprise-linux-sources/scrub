Name:		scrub
Version:	2.2
Release:	2%{?dist}
Summary:	Disk scrubbing program
License:	GPLv2+
Group:		System Environment/Base
URL:		http://code.google.com/p/diskscrub/
Source0:	http://diskscrub.googlecode.com/files/scrub-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: automake autoconf
# 907173 - [RFE] Add option for "scrub" utility to only scrub used blocks of a sparse file
Patch0: scrub-2.2-extentonly.patch
# 903890 - scrub-freespace didn't remove the scrub file, cause the file system 100% full
Patch1: scrub-2.2-scrubfreespacefix.patch

%description
Scrub writes patterns on files or disk devices to make
retrieving the data more difficult.  It operates in one of three
modes: 1) the special file corresponding to an entire disk is scrubbed
and all data on it is destroyed;  2) a regular file is scrubbed and
only the data in the file (and optionally its name in the directory
entry) is destroyed; or 3) a regular file is created, expanded until
the file system is full, then scrubbed as in 2).

%prep
%setup -q
%patch0 -p1 -b .extentonly
%patch1 -p1 -b .scrubfreespacefix

%build
./autogen.sh
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc NEWS ChangeLog DISCLAIMER COPYING
%{_bindir}/scrub
%{_mandir}/man1/scrub.1*

%changelog
* Mon Mar 17 2014 Daniel Kopecek <dkopecek@redhat.com> 2.2-2
- added support for scrubing only allocated file extents (option -E)
- added patch to fix scrub-freespace
  Resolves: rhbz#907173
  Resolves: rhbz#903890

* Wed Jan 13 2010 Steve Grubb <sgrubb@redhat.com> 2.2-1
- initial package for RHEL 
