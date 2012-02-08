# build against xz?
%bcond_without xz
# sqlite backend is pretty useless
%bcond_with sqlite
# just for giggles, option to build with internal Berkeley DB
%bcond_with int_bdb
# run internal testsuite?
%bcond_without check

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define rpmhome /usr/lib/rpm

%define rpmver 4.8.0
%define snapver %{nil}
%define srcver %{rpmver}

%define bdbver 4.8.24
%define dbprefix db

Summary: The RPM package management system
Name: rpm
Version: %{rpmver}
Release: 19%{?dist}.R
Group: System Environment/Base
Url: http://www.rpm.org/
Source0: http://rpm.org/releases/rpm-4.8.x/%{name}-%{version}.tar.bz2
%if %{with int_bdb}
Source1: db-%{bdbver}.tar.gz
%endif

Patch0: rpm-4.7.90-devel-autodep.patch
Patch1: rpm-4.5.90-pkgconfig-path.patch
Patch2: rpm-4.5.90-gstreamer-provides.patch
# Fedora specspo is setup differently than what rpm expects, considering
# this as Fedora-specific patch for now
Patch3: rpm-4.7.90-fedora-specspo.patch
# In current RHEL, filesystem pkg owns all the localized man directories
Patch4: rpm-4.8.0-no-man-dirs.patch

# Patches already in upstream
Patch200: rpm-4.8.0-url-segfault.patch
Patch201: rpm-4.8.0-verify-exitcode.patch
Patch202: rpm-4.8.0-pythondeps-parallel.patch
Patch203: rpm-4.8.0-python-bytecompile.patch
Patch204: rpm-4.8.0-lazy-statfs.patch
Patch205: rpm-4.8.0-erasure-dsi.patch
Patch206: rpm-4.8.0-prep-keep-empty.patch
Patch207: rpm-4.8.0-python-nocontexts.patch
Patch208: rpm-4.8.0-python-mibool.patch
Patch209: rpm-4.8.0-fix-nosrc.patch
Patch210: rpm-4.8.0-debugedit-lazy-buildid.patch
Patch211: rpm-4.8.0-chroot-verify.patch
Patch212: rpm-4.8.0-python-emptyds.patch
Patch213: rpm-4.8.0-pubkey-crlf.patch
Patch214: rpm-4.8.0-curl-empty-reply.patch
Patch215: rpm-4.8.0-remove-sbits.patch
Patch216: rpm-4.8.0-multiple-pubkeys.patch
Patch217: rpm-4.8.0-freshen-arch.patch
Patch218: rpm-4.8.0-sigsanity.patch
Patch219: rpm-4.8.0-getoutputfrom.patch
Patch220: rpm-4.8.0-debuginfo-hardlinks.patch
Patch221: rpm-4.8.0-debuginfo-index.patch
Patch222: rpm-4.8.0-verifyscript-status.patch
Patch223: rpm-4.8.0-sigcompare.patch
Patch224: rpm-4.8.0-pwcheck-errors.patch
Patch225: rpm-4.8.0-umask.patch
Patch226: rpm-4.8.0-prefcolor-erase.patch

Patch227: rpm-4.8.0-selfconflict.patch
Patch228: rpm-4.8.0-rpm2cpio.sh-xz.patch
Patch229: rpm-4.8.0-import-GPG.patch
Patch230: rpm-4.8.0-fileconflicts-1.patch
Patch231: rpm-4.8.0-fileconflicts-2.patch
Patch232: rpm-4.8.0-fileattrs.patch
Patch233: rpm-4.8.0-sigcompare-fix.patch
Patch234: rpm-4.8.0-sigcheck.patch

Patch235: rpm-4.8.0-header-sanity.patch
Patch236: rpm-4.8.x-pgpsubtype.patch

# These are not yet upstream
Patch301: rpm-4.6.0-niagara.patch
Patch302: rpm-4.7.1-geode-i686.patch
Patch303: rpm-4.8.0-em64t.patch

# Temporary Patch to provide support for updates
Patch400: rpm-4.8.0-rpmlib-filesystem-check.patch

# Partially GPL/LGPL dual-licensed and some bits with BSD
# SourceLicense: (GPLv2+ and LGPLv2+ with exceptions) and BSD 
License: GPLv2+

Requires: coreutils
%if %{without int_bdb}
# db recovery tools, rpmdb_util symlinks
Requires: db4-utils
%endif
Requires: popt >= 1.10.2.1
Requires: curl

%if %{without int_bdb}
BuildRequires: db4-devel%{_isa}
%endif

%if %{with check}
BuildRequires: fakechroot
%endif

# XXX generally assumed to be installed but make it explicit as rpm
# is a bit special...
BuildRequires: redhat-rpm-config
BuildRequires: gawk
BuildRequires: elfutils-devel%{_isa} >= 0.112
BuildRequires: elfutils-libelf-devel%{_isa}
BuildRequires: readline-devel%{_isa} zlib-devel%{_isa}
BuildRequires: nss-devel%{_isa}
# The popt version here just documents an older known-good version
BuildRequires: popt-devel%{_isa} >= 1.10.2
BuildRequires: file-devel%{_isa}
BuildRequires: gettext-devel%{_isa}
BuildRequires: libselinux-devel%{_isa}
BuildRequires: ncurses-devel%{_isa}
BuildRequires: bzip2-devel%{_isa} >= 0.9.0c-2
BuildRequires: python-devel%{_isa} >= 2.6
BuildRequires: lua-devel%{_isa} >= 5.1
BuildRequires: libcap-devel%{_isa}
BuildRequires: libacl-devel%{_isa}
# Needed for fix-nosrc patch touching testsuite
BuildRequires: autoconf
%if ! %{without xz}
BuildRequires: xz-devel%{_isa} >= 4.999.8
%endif
%if %{with sqlite}
BuildRequires: sqlite-devel%{_isa}
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The RPM Package Manager (RPM) is a powerful command line driven
package management system capable of installing, uninstalling,
verifying, querying, and updating software packages. Each software
package consists of an archive of files along with information about
the package like its version, a description, etc.

%package libs
Summary:  Libraries for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}
# librpm uses cap_compare, introduced sometimes between libcap 2.10 and 2.16.
# A manual require is needed, see #505596
Requires: libcap%{_isa} >= 2.16

%description libs
This package contains the RPM shared libraries.

%package devel
Summary:  Development files for manipulating RPM packages
Group: Development/Libraries
License: GPLv2+ and LGPLv2+ with exceptions
Requires: rpm = %{version}-%{release}
Requires: popt-devel%{_isa}
Requires: file-devel%{_isa}

%description devel
This package contains the RPM C library and header files. These
development files will simplify the process of writing programs that
manipulate RPM packages and databases. These files are intended to
simplify the process of creating graphical package managers or any
other tools that need an intimate knowledge of RPM packages in order
to function.

This package should be installed if you want to develop programs that
will manipulate RPM packages and databases.

%package build
Summary: Scripts and executable programs used to build packages
Group: Development/Tools
Requires: rpm = %{version}-%{release}
Requires: elfutils >= 0.128 binutils
Requires: findutils sed grep gawk diffutils file patch >= 2.5
Requires: unzip gzip bzip2 cpio lzma xz
Requires: pkgconfig
Requires: /usr/bin/gdb-add-index
Conflicts: ocaml-runtime < 3.11.1-7

%description build
The rpm-build package contains the scripts and executable programs
that are used to build packages using the RPM Package Manager.

%package python
Summary: Python bindings for apps which will manipulate RPM packages
Group: Development/Libraries
Requires: rpm = %{version}-%{release}

%description python
The rpm-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by RPM Package Manager libraries.

This package should be installed if you want to develop Python
programs that will manipulate RPM packages and databases.

%package apidocs
Summary: API documentation for RPM libraries
Group: Documentation
BuildArch: noarch

%description apidocs
This package contains API documentation for developing applications
that will manipulate RPM packages and databases.

%package cron
Summary: Create daily logs of installed packages.
Group: System Environment/Base
BuildArch: noarch
Requires: crontabs logrotate rpm = %{version}-%{release}

%description cron
This package contains a cron job which creates daily logs of installed
packages on a system.

%prep
%setup -q -n %{name}-%{srcver} %{?with_int_bdb:-a 1}
%patch0 -p1 -b .devel-autodep
%patch1 -p1 -b .pkgconfig-path
%patch2 -p1 -b .gstreamer-prov
%patch3 -p1 -b .fedora-specspo
%patch4 -p1 -b .no-man-dirs

%patch200 -p1 -b .url-segfault
%patch201 -p1 -b .verify-exitcode
%patch202 -p1 -b .pythondeps-parallel
%patch203 -p1 -b .python-bytecompile
%patch204 -p1 -b .lazy-statfs
%patch205 -p1 -b .erasure-dsi
%patch206 -p1 -b .prep-keep-empty
%patch207 -p1 -b .python-nocontexts
%patch208 -p1 -b .python-mibool
%patch209 -p1 -b .fix-nosrc
%patch210 -p1 -b .debugedit-lazy-buildid
%patch211 -p1 -b .chroot-verify
%patch212 -p1 -b .python-emptyds
%patch213 -p1 -b .pubkey-crlf
%patch214 -p1 -b .curl-empty-reply
%patch215 -p1 -b .remove-sbits
%patch216 -p1 -b .multiple-pubkeys
%patch217 -p1 -b .freshen-arch
%patch218 -p1 -b .sigsanity
%patch219 -p1 -b .getoutputfrom
%patch220 -p1 -b .debuginfo-hardlinks
%patch221 -p1 -b .debuginfo-index
%patch222 -p1 -b .verifyscript-status
%patch223 -p1 -b .sigcompare
%patch224 -p1 -b .pwcheck-errors
%patch225 -p1 -b .umask
%patch226 -p1 -b .prefcolor-erase

%patch227 -p1 -b .selfconflict
%patch228 -p1 -b .rpm2cpio.sh-xz
%patch229 -p1 -b .import-GPG
%patch230 -p1 -b .fileconflicts-1
%patch231 -p1 -b .fileconflicts-2
%patch232 -p1 -b .fileattrs
%patch233 -p1 -b .sigcompare-fix
%patch234 -p1 -b .sigcheck
%patch235 -p1 -b .header-sanity
%patch236 -p1 -b .pgpsubtype

%patch301 -p1 -b .niagara
%patch302 -p1 -b .geode
%patch303 -p1 -b .em64t

%patch400 -p1 -b .rpmlib-filesystem-check

%if %{with int_bdb}
ln -s db-%{bdbver} db
%endif

%build
%if %{without int_bdb}
#CPPFLAGS=-I%{_includedir}/db%{bdbver} 
#LDFLAGS=-L%{_libdir}/db%{bdbver}
%endif
CPPFLAGS="$CPPFLAGS `pkg-config --cflags nss`"
CFLAGS="$RPM_OPT_FLAGS"
export CPPFLAGS CFLAGS LDFLAGS

# Using configure macro has some unwanted side-effects on rpm platform
# setup, use the old-fashioned way for now only defining minimal paths.
./configure \
    --prefix=%{_usr} \
    --sysconfdir=%{_sysconfdir} \
    --localstatedir=%{_var} \
    --sharedstatedir=%{_var}/lib \
    --libdir=%{_libdir} \
    %{!?with_int_bdb: --with-external-db} \
    %{?with_sqlite: --enable-sqlite3} \
    --with-lua \
    --with-selinux \
    --with-cap \
    --with-acl \
    --enable-python

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

# Save list of packages through cron
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily
install -m 755 scripts/rpm.daily ${RPM_BUILD_ROOT}%{_sysconfdir}/cron.daily/rpm

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d
install -m 644 scripts/rpm.log ${RPM_BUILD_ROOT}%{_sysconfdir}/logrotate.d/rpm

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm

mkdir -p $RPM_BUILD_ROOT/var/lib/rpm
for dbi in \
    Basenames Conflictname Dirnames Group Installtid Name Packages \
    Providename Provideversion Requirename Requireversion Triggername \
    Filedigests Pubkeys Sha1header Sigmd5 Obsoletename \
    __db.001 __db.002 __db.003 __db.004 __db.005 __db.006 __db.007 \
    __db.008 __db.009
do
    touch $RPM_BUILD_ROOT/var/lib/rpm/$dbi
done

# plant links to db utils as rpmdb_foo so existing documantion is usable
%if %{without int_bdb}
for dbutil in \
    archive deadlock dump load printlog \
    recover stat upgrade verify
do
    ln -s ../../bin/%{dbprefix}_${dbutil} $RPM_BUILD_ROOT/%{rpmhome}/rpmdb_${dbutil}
done
%endif

%find_lang %{name}

find $RPM_BUILD_ROOT -name "*.la"|xargs rm -f

# avoid dragging in tonne of perl libs for an unused script
chmod 0644 $RPM_BUILD_ROOT/%{rpmhome}/perldeps.pl

# compress our ChangeLog, it's fairly big...
bzip2 -9 ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with check}
%check
make check
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%posttrans
# XXX this is klunky and ugly, rpm itself should handle this
dbstat=/usr/lib/rpm/rpmdb_stat
if [ -x "$dbstat" ]; then
    if "$dbstat" -e -h /var/lib/rpm 2>&1 | grep -q "doesn't match environment version \| Invalid argument"; then
        rm -f /var/lib/rpm/__db.* 
    fi
fi
exit 0

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc GROUPS COPYING CREDITS ChangeLog.bz2 doc/manual/[a-z]*

%dir                            %{_sysconfdir}/rpm

%attr(0755, root, root)   %dir /var/lib/rpm
%attr(0644, root, root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/lib/rpm/*
%attr(0755, root, root) %dir %{rpmhome}

/bin/rpm
%{_bindir}/rpm2cpio
%{_bindir}/rpmdb
%{_bindir}/rpmsign
%{_bindir}/rpmquery
%{_bindir}/rpmverify

%{_mandir}/man8/rpm.8*
%{_mandir}/man8/rpm2cpio.8*

# XXX this places translated manuals to wrong package wrt eg rpmbuild
%lang(fr) %{_mandir}/fr/man[18]/*.[18]*
%lang(ko) %{_mandir}/ko/man[18]/*.[18]*
%lang(ja) %{_mandir}/ja/man[18]/*.[18]*
%lang(pl) %{_mandir}/pl/man[18]/*.[18]*
%lang(ru) %{_mandir}/ru/man[18]/*.[18]*
%lang(sk) %{_mandir}/sk/man[18]/*.[18]*

%{rpmhome}/macros
%{rpmhome}/rpmpopt*
%{rpmhome}/rpmrc

%{rpmhome}/rpmdb_*
%{rpmhome}/rpm.daily
%{rpmhome}/rpm.log
%{rpmhome}/rpm.xinetd
%{rpmhome}/rpm2cpio.sh
%{rpmhome}/tgpg

%{rpmhome}/platform

%files libs
%defattr(-,root,root)
%{_libdir}/librpm*.so.*

%files build
%defattr(-,root,root)
%{_bindir}/rpmbuild
%{_bindir}/gendiff

%{_mandir}/man1/gendiff.1*

%{rpmhome}/brp-*
%{rpmhome}/check-buildroot
%{rpmhome}/check-files
%{rpmhome}/check-prereqs
%{rpmhome}/check-rpaths*
%{rpmhome}/debugedit
%{rpmhome}/find-debuginfo.sh
%{rpmhome}/find-lang.sh
%{rpmhome}/find-provides
%{rpmhome}/find-requires
%{rpmhome}/javadeps
%{rpmhome}/mono-find-provides
%{rpmhome}/mono-find-requires
%{rpmhome}/ocaml-find-provides.sh
%{rpmhome}/ocaml-find-requires.sh
%{rpmhome}/osgideps.pl
%{rpmhome}/perldeps.pl
%{rpmhome}/libtooldeps.sh
%{rpmhome}/pkgconfigdeps.sh
%{rpmhome}/perl.prov
%{rpmhome}/perl.req
%{rpmhome}/tcl.req
%{rpmhome}/pythondeps.sh
%{rpmhome}/rpmdeps
%{rpmhome}/config.guess
%{rpmhome}/config.sub
%{rpmhome}/mkinstalldirs
%{rpmhome}/rpmdiff*
%{rpmhome}/desktop-file.prov
%{rpmhome}/fontconfig.prov

%{rpmhome}/macros.perl
%{rpmhome}/macros.python
%{rpmhome}/macros.php

%{_mandir}/man8/rpmbuild.8*
%{_mandir}/man8/rpmdeps.8*

%files python
%defattr(-,root,root)
%{python_sitearch}/rpm

%files devel
%defattr(-,root,root)
%{_includedir}/rpm
%{_libdir}/librp*[a-z].so
%{_mandir}/man8/rpmgraph.8*
%{_bindir}/rpmgraph
%{_libdir}/pkgconfig/rpm.pc

%files cron
%defattr(-,root,root)
%{_sysconfdir}/cron.daily/rpm
%config(noreplace) %{_sysconfdir}/logrotate.d/rpm

%files apidocs
%defattr(-,root,root)
%doc doc/librpm/html/*

%changelog
* Wed Feb  8 2012 Arkady L. Shane <ashejn@russianfedora.ru> - 4.8.0-19.R
- add temporary rpmlib patch to support filesystem transition
  https://fedoraproject.org/wiki/Features/UsrMove

* Tue Oct 04 2011 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-19
- Fix crash on malformed OpenPGP packet (#742499)

* Thu Sep 29 2011 Jindrich Novy <jnovy@redhat.com> - 4.8.0-18
- fix CVE-2011-3378 (#742155)

* Thu Aug 11 2011 Florian Festi <ffesti@redhat.com> - 4.8.0-17
- Allow self conflicts (#651951)
- Add support for xz compression in rpm2cpio.sh (#674348)
- Don't error out on already imported GPG keys (#680889)
- Fix file conflict handling for uncolored files (#705115)
- Fix file attribute handling with %defattr(-) (#705993)
- Don't error out when trying to add the same signature again (#707449)
- Fix signature checking (#721363)

* Wed Mar 09 2011 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-16
- Erase preferred color packages last, fixing colored file removal (#680261)

* Fri Mar 04 2011 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-15
- Fix verifyscript getting run twice (#668629)

* Mon Jan 31 2011 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-14
- Fix signature comparison on package resigning (#608608)
- Let error messages from gpg through on passphrase checking (#607222)
- Only enforce default umask during transaction (#565843)

* Tue Jan 25 2011 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-13
- Require matching arch for freshen on colored transactions (#553108, #479608)
- Verify that generated signature can be used by rpm (#608599)
- Fix broken pipe on font provide generation + better error message (#609117)
- Fix find-debuginfo.sh behavior on cross-directory hardlinks (#618428)
- Generate gdb index for debuginfos (#652787)
- Fix verifyscript return code on failure (#668629)

* Fri Jul 09 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-12
- Skip past any initial comments in pubkey files

* Fri Jul 02 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-11
- Support multiple pubkeys in a single file on --import (#586827)

* Tue Jun 29 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-10
- Fix empty reply from server on url retrieve (#598988)
- Drop suid/sgid bits and capabilities on upgrade/erase (#598832)

* Tue Jun 01 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-9
- Handle non-existent dependency sets correctly in python (#593621)
- Permit DOS-style line-endings in PGP armor headers (#532992)

* Tue May 18 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-8
- Fix return from chroot on verify (#590588)

* Mon May 17 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-7
- Only recompute build-id when DWARF-data is changed (#590947)

* Tue May 04 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-6
- Permit em64t architecture in query/erasure too (#547341)
- Avoid accessing unrelated mount points in disk space checking (#495623)
- Fix disk space reporting with erasures present in transaction (#561160)
- Teach python bindings about RPMTRANS_FLAG_NOCONTEXTS (related to #573111)
- Fix python match iterator regression wrt boolean representation
- Support parallel python versions in python dependency extractor (#532118)
- Python byte-compilation fixes + improvements (#538101)
- Preserve empty lines in spec prep section (#573339)
- Fix nosrc package generation regression
- Avoid owning localized man directories through find_lang (#569536)
- Lose useless symlink to berkeley_db_svc

* Thu Jan 21 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-5
- fix segfault on failed url retrieval (#557118)
- fix verification error code depending on verbosity level (#557101)

* Tue Jan 12 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-4
- fix source URL pointing to wrong directory on rpm.org

* Fri Jan 08 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-3
- Treat em64t architecture as an alias for x86_64 (#547341)

* Fri Jan 08 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-2
- put disttag back, accidentally nuked in 4.8.0 final update

* Fri Jan 08 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-1
- update to 4.8.0 final (http://rpm.org/wiki/Releases/4.8.0)

* Thu Jan 07 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.6
- pull out macro scoping "fix" for now, it breaks font package macros

* Mon Jan 04 2010 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.5
- always clear locally defined macros when they go out of scope

* Thu Dec 17 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.4
- permit unexpanded macros when parsing spec (#547997)

* Wed Dec 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.3
- fix a bunch of python refcount-errors causing major memory leaks

* Mon Dec 07 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.2
- fix noise from python bytecompile on non-python packages (#539635)
- make all our -devel [build]requires isa-specific
- trim out superfluous -devel dependencies from rpm-devel

* Mon Dec 07 2009 Panu Matilainen <pmatilai@redhat.com> - 4.8.0-0.beta1.1
- update to 4.8.0-beta1 (http://rpm.org/wiki/Releases/4.8.0)
- rpm-build conflicts with current ocaml-runtime

* Fri Dec 04 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.2-2
- missing error exit code from signing password checking (#496754)
- dont fail build on unrecognized data files (#532489)
- dont try to parse subkeys and secret keys (#436812)
- fix chmod test on selinux, breaking %%{_fixperms} macro (#543035)

* Wed Nov 25 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.2-1
- update to 4.7.2 (http://rpm.org/wiki/Releases/4.7.2)
- fixes #464750, #529214

* Wed Nov 18 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-10
- rebuild against BDB-4.8.24

* Wed Nov 18 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-9
- drop versioned dependency to BDB

* Wed Oct 28 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-8
- support multiple python implementations in brp-python-bytecompile (#531117)
- make disk space problem reporting a bit saner (#517418)

* Tue Oct 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-7
- fix build with BDB 4.8.x by removing XA "support" from BDB backend 
- perl dep extractor heredoc parsing improvements (#524929)

* Mon Sep 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-6
- use relative paths within db environment (related to #507309, #507309...)
- remove db environment on close in chrooted operation (related to above)
- initialize rpmlib earlier in rpm2cpio (#523260)
- fix file dependency tag extension formatting (#523282)

* Tue Sep 15 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-5
- fix duplicate dependency filtering on build (#490378)
- permit absolute paths in file lists again (#521760)
- use permissions 444 for all .debug files (#522194)
- add support for optional bugurl tag (#512774)

* Fri Aug 14 2009 Jesse Keating <jkeating@redhat.com> - 4.7.1-4
- Patch to make geode appear as i686 (#517475)

* Thu Aug 06 2009 Jindrich Novy <jnovy@redhat.com> - 4.7.1-3
- rebuild because of the new xz

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.1-1
- update to 4.7.1 ((http://rpm.org/wiki/Releases/4.7.1)
- fix source url

* Mon Jul 20 2009 Bill Nottingham <notting@redhat.com> - 4.7.0-9
- enable XZ support

* Thu Jun 18 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-8
- updated OSGi dependency extractor (#506471)
- fix segfault in symlink fingerprinting (#505777)
- fix invalid memory access causing bogus file dependency errors (#506323)

* Tue Jun 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-7
- add dwarf-3 support to debugedit (#505774)

* Fri Jun 12 2009 Stepan Kasal <skasal@redhat.com> - 4.7.0-6
- require libcap >= 2.16 (#505596)

* Tue Jun 03 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-5
- don't mess up problem altNEVR in python ts.check() (#501068)
- fix hardlink size calculation on build (#503020)

* Thu May 14 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-4
- split cron-job into a sub-package to avoid silly deps on core rpm (#500722)
- rpm requires coreutils but not in %%post
- build with libcap and libacl
- fix pgp pubkey signature tag parsing

* Tue Apr 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-3
- couple of merge-review fixes (#226377)
  - eliminate bogus leftover rpm:rpm rpmdb ownership
  - unescaped macro in changelog
- fix find-lang --with-kde with KDE3 (#466009)
- switch back to default file digest algorithm

* Fri Apr 17 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-2
- file classification tweaks for text files (#494817)
  - disable libmagic text token checks, it's way too error-prone
  - consistently classify all text as such and include description

* Thu Apr 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-1
- update to 4.7.0 final (http://rpm.org/wiki/Releases/4.7.0)
- fixes #494049, #495429
- dont permit test-suite failure anymore

* Thu Apr 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.rc1.1
- update to 4.7.0-rc1
- fixes #493157, #493777, #493696, #491388, #487597, #493162

* Fri Apr 03 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.9
- fix recorded file state of otherwise skipped files (#492947)
- compress ChangeLog, drop old CHANGES file (#492440)

* Thu Apr  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4.7.0-0.beta1.8
- Fix sparcv9v and sparc64v targets

* Tue Mar 24 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.7
- prefer more specific types over generic "text" in classification (#491349)

* Mon Mar 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.6
- with the fd leak gone, let libmagic look into compressed files again (#491596)

* Mon Mar 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.5
- fix font provide generation on filenames with whitespace (#491597)

* Thu Mar 12 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.4
- handle RSA V4 signatures (#436812)
- add alpha arch ISA-bits
- enable internal testsuite on build

* Mon Mar 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.3
- fix _install_langs behavior (#489235)
- fix recording of file states into rpmdb on install

* Sun Mar 08 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.2
- load macros before creating directories on src.rpm install (#489104)

* Fri Mar 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.7.0-0.beta1.1
- update to 4.7.0-beta1 (http://rpm.org/wiki/Releases/4.7.0)

* Fri Feb 27 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-11
- build rpm itself with md5 file digests for now to ensure upgradability

* Thu Feb 26 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-10
- handle NULL passed as EVR in rpmdsSingle() again (#485616)

* Wed Feb 25 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-9
- pull out python byte-compile syntax check for now

* Mon Feb 23 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-8
- make -apidocs sub-package noarch
- fix source URL

* Sat Feb 21 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-7
- loosen up restrictions on dependency names (#455119)
- handle inter-dependent pkg-config files for requires too (#473814)
- error/warn on elf binaries in noarch package in build

* Fri Feb 20 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-6
- error out on uncompilable python code (Tim Waugh)

* Tue Feb 17 2009 Jindrich Novy <jnovy@redhat.com> - 4.6.0-5
- remove two offending hunks from anyarch patch causing that
  RPMTAG_BUILDARCHS isn't written to SRPMs

* Mon Feb 16 2009 Jindrich Novy <jnovy@redhat.com> - 4.6.0-4
- inherit group tag from the main package (#470714)
- ignore BuildArch tags for anyarch actions (#442105)
- don't check package BuildRequires when doing --rmsource (#452477)
- don't fail because of missing sources when only spec removal
  is requested (#472427)

* Mon Feb 16 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-3
- updated fontconfig provide script - fc-query does all the hard work now

* Mon Feb 09 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-2
- build against db 4.7.x

* Fri Feb 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-1
- update to 4.6.0 final
- revert libmagic looking into compressed files for now, breaks ooffice build

* Fri Feb 06 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.5
- enable fontconfig provides generation

* Thu Feb 05 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.4
- fixup rpm translation lookup to match Fedora specspo (#436941)

* Wed Feb 04 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.3
- extract mimehandler provides from .desktop files
- preliminaries for extracting font provides (not enabled yet)
- dont classify font metrics data as fonts
- only run script dep extraction once per file, duh

* Sat Jan 31 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.2
- change platform sharedstatedir to something more sensible (#185862)
- add rpmdb_foo links to db utils for documentation compatibility

* Fri Jan 30 2009 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc4.1
- update to 4.6.0-rc4
- fixes #475582, #478907, #476737, #479869, #476201

* Fri Dec 12 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.2
- add back defaultdocdir patch which hadn't been applied on 4.6.x branch yet

* Fri Dec 12 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.1
- add dist-tag, rebuild

* Tue Dec 09 2008 Panu Matilainen <pmatilai@redhat.com> - 4.6.0-0.rc3.1
- update to rpm 4.6.0-rc3
- fixes #475214, #474550, #473239

* Wed Dec  3 2008 Jeremy Katz <katzj@redhat.com> - 4.6.0-0.rc2.9
- I built into the wrong place

* Wed Dec  3 2008 Jeremy Katz <katzj@redhat.com> - 4.6.0-0.rc2.8
- python 2.6 rebuild again

* Wed Dec 03 2008 Panu Matilainen <pmatilai@redhat.com>
- make rpm-build require pkgconfig (#473978)

* Tue Dec 02 2008 Panu Matilainen <pmatilai@redhat.com>
- fix pkg-config provide generation when pc's depend on each other (#473814)

* Mon Dec 01 2008 Jindrich Novy <jnovy@redhat.com>
- include rpmfileutil.h from rpmmacro.h, unbreaks
  net-snmp (#473420)

* Sun Nov 30 2008 Panu Matilainen <pmatilai@redhat.com>
- rebuild for python 2.6

* Sat Nov 29 2008 Panu Matilainen <pmatilai@redhat.com>
- update to 4.6.0-rc2
- fixes #471820, #473167, #469355, #468319, #472507, #247374, #426672, #444661
- enable automatic generation of pkg-config and libtool dependencies #465377

* Fri Oct 31 2008 Panu Matilainen <pmatilai@redhat.com>
- adjust find-debuginfo for "file" output change (#468129)

* Tue Oct 28 2008 Panu Matilainen <pmatilai@redhat.com>
- Florian's improved fingerprinting hash algorithm from upstream

* Sat Oct 25 2008 Panu Matilainen <pmatilai@redhat.com>
- Make noarch sub-packages actually work
- Fix defaultdocdir logic in installplatform to avoid hardwiring mandir

* Fri Oct 24 2008 Jindrich Novy <jnovy@redhat.com>
- update compat-db dependencies (#459710)

* Wed Oct 22 2008 Panu Matilainen <pmatilai@redhat.com>
- never add identical NEVRA to transaction more than once (#467822)

* Sun Oct 19 2008 Panu Matilainen <pmatilai@redhat.com>
- permit tab as macro argument separator (#467567)

* Thu Oct 16 2008 Panu Matilainen <pmatilai@redhat.com>
- update to 4.6.0-rc1 
- fixes #465586, #466597, #465409, #216221, #466503, #466009, #463447...
- avoid using %%configure macro for now, it has unwanted side-effects on rpm

* Wed Oct 01 2008 Panu Matilainen <pmatilai@redhat.com>
- update to official 4.5.90 alpha tarball 
- a big pile of misc bugfixes + translation updates
- isa-macro generation fix for ppc (#464754)
- avoid pulling in pile of perl dependencies for an unused script
- handle both "invalid argument" and clear env version mismatch on posttrans

* Thu Sep 25 2008 Jindrich Novy <jnovy@redhat.com>
- don't treat %%patch numberless if -P parameter is present (#463942)

* Thu Sep 11 2008 Panu Matilainen <pmatilai@redhat.com>
- add hack to support extracting gstreamer plugin provides (#438225)
- fix another macro argument handling regression (#461180)

* Thu Sep 11 2008 Jindrich Novy <jnovy@redhat.com>
- create directory structure for rpmbuild prior to build if it doesn't exist (#455387)
- create _topdir if it doesn't exist when installing SRPM
- don't generate broken cpio in case of hardlink pointing on softlink,
  thanks to pixel@mandriva.com

* Sat Sep 06 2008 Jindrich Novy <jnovy@redhat.com>
- fail hard if patch isn't found (#461347)

* Mon Sep 01 2008 Jindrich Novy <jnovy@redhat.com>
- fix parsing of boolean expressions in spec (#456103)
  (unbreaks pam, jpilot and maybe other builds)

* Tue Aug 26 2008 Jindrich Novy <jnovy@redhat.com>
- add support for noarch subpackages
- fix segfault in case of insufficient disk space detected (#460146)

* Wed Aug 13 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8461.2
- fix archivesize tag generation on ppc (#458817)

* Fri Aug 08 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8461.1
- new snapshot from upstream
- fixes #68290, #455972, #446202, #453364, #456708, #456103, #456321, #456913,
  #458260, #458261
- partial fix for #457360

* Thu Jul 31 2008 Florian Festi <ffesti@redhat.com>
- 4.5.90-0.git8427.1
- new snapshot from upstream

* Thu Jul 31 2008 Florian Festi <ffesti@redhat.com>
- 4.5.90-0.git8426.10
- rpm-4.5.90-posttrans.patch
- use header from rpmdb in posttrans to make anaconda happy

* Sat Jul 19 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.9
- fix regression in patch number handling (#455872)

* Tue Jul 15 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.8
- fix regression in macro argument handling (#455333)

* Mon Jul 14 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.7
- fix mono dependency extraction (adjust for libmagic string change)

* Sat Jul 12 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.6
- fix type mismatch causing funky breakage on ppc64

* Fri Jul 11 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8426.5
- flip back to external bdb
- fix tab vs spaces complaints from rpmlint
- add dep for lzma and require unzip instead of zip in build (#310694)
- add pkgconfig dependency to rpm-devel
- drop ISA-dependencies for initial introduction
- new snapshot from upstream for documentation fixes

* Thu Jul 10 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.4
- handle int vs external db in posttrans too

* Wed Jul 08 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.3
- require curl as external url helper

* Wed Jul 08 2008 Panu Matilainen <pmatilai@redhat.com>
- 4.5.90-0.git8424.2
- add support for building with or without internal db

* Wed Jul 08 2008 Panu Matilainen <pmatilai@redhat.com>
- rpm 4.5.90-0.git8424.1 (alpha snapshot)
- adjust to build against Berkeley DB 4.5.20 from compat-db for now
- add posttrans to clean up db environment mismatch after upgrade
- forward-port devel autodeps patch

* Tue Jul 08 2008 Panu Matilainen <pmatilai@redhat.com>
- adjust for rpmdb index name change
- drop unnecessary vendor-macro patch for real
- add ISA-dependencies among rpm subpackages
- make lzma and sqlite deps conditional and disabled by default for now

* Fri Feb 01 2008 Panu Matilainen <pmatilai@redhat.com>
- spec largely rewritten, truncating changelog
