%{?scl:%scl_package perl-Try-Tiny}
%{!?scl:%global pkg_name %{name}}

Name:		%{?scl_prefix}perl-Try-Tiny
Summary:	Minimal try/catch with proper localization of $@
Version:	0.18
Release:	1%{?dist}
License:	MIT
Group:		Development/Libraries
URL:		http://search.cpan.org/dist/Try-Tiny
Source0:	http://search.cpan.org/CPAN/authors/id/D/DO/DOY/Try-Tiny-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{pkg_name}-%{version}-%{release}-root-%(id -nu)
BuildArch:	noarch
# Module Build
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker) >= 6.17
# Module
BuildRequires:	%{?scl_prefix}perl(base)
BuildRequires:	%{?scl_prefix}perl(Carp)
BuildRequires:	%{?scl_prefix}perl(constant)
BuildRequires:	%{?scl_prefix}perl(Exporter)
BuildRequires:	%{?scl_prefix}perl(Sub::Name)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(File::Find)
BuildRequires:	%{?scl_prefix}perl(File::Temp)
BuildRequires:	%{?scl_prefix}perl(Test::More)
# Extra Tests
%if ! 0%{?scl:1}
BuildRequires:	%{?scl_prefix}perl(Pod::Coverage::TrustPod)
BuildRequires:	%{?scl_prefix}perl(Test::EOL)
BuildRequires:	%{?scl_prefix}perl(Test::NoTabs)
BuildRequires:	%{?scl_prefix}perl(Test::Pod) >= 1.41
BuildRequires:	%{?scl_prefix}perl(Test::Pod::Coverage) >= 1.08
%endif
# Runtime
%{?scl:%global perl_version %(scl enable %{scl} 'eval "`perl -V:version`"; echo $version')}
%{!?scl:%global perl_version %(eval "`perl -V:version`"; echo $version)}
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%{perl_version})
Requires:	%{?scl_prefix}perl(Sub::Name)

%description
This module provides bare bones try/catch statements that are designed to
minimize common mistakes with eval blocks, and NOTHING else.

This is unlike TryCatch, which provides a nice syntax and avoids adding
another call stack layer, and supports calling return from the try block to
return from the parent subroutine. These extra features come at a cost of a
few dependencies, namely Devel::Declare and Scope::Upper that are occasionally
problematic, and the additional catch filtering uses Moose type constraints,
which may not be desirable either.

%prep
%setup -q -n Try-Tiny-%{version}

%build
%{?scl:scl enable %{scl} "}
perl Makefile.PL INSTALLDIRS=vendor
%{?scl:"}
%{?scl:scl enable %{scl} "}
make %{?_smp_mflags}
%{?scl:"}

%install
rm -rf %{buildroot}
%{?scl:scl enable %{scl} "}
make pure_install DESTDIR=%{buildroot}
%{?scl:"}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} "}
make test
%{?scl:"}
%if ! 0%{?scl:1}
%{?scl:scl enable %{scl} - << \EOF}
make test TEST_FILES="$(echo $(find xt/ -name '*.t'))"
%{?scl:EOF}
%endif

%clean
rm -rf %{buildroot}

%files
%doc Changes LICENSE README t/
%{perl_vendorlib}/Try/
%{_mandir}/man3/Try::Tiny.3pm*

%changelog
* Thu Nov 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 0.18-2
- Rebuilt for SCL
- Disable extra tests

* Sat Aug 17 2013 Paul Howarth <paul@city-fan.org> - 0.18-1
- Update to 0.18
  - Fix tests for pre-Test-More-0.88 (https://github.com/doy/try-tiny/pull/10)
- Drop upstreamed patch for building with Test::More < 0.88

* Sat Aug 17 2013 Paul Howarth <paul@city-fan.org> - 0.17-1
- Update to 0.17
  - Work around Perl RT#119311, which was causing incorrect error messages in
    some cases during global destruction
    (https://github.com/doy/try-tiny/pull/9)
- Add patch to support building with Test::More < 0.88

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Petr Pisar <ppisar@redhat.com> - 0.16-2
- Perl 5.18 rebuild

* Wed Jul 10 2013 Paul Howarth <paul@city-fan.org> - 0.16-1
- Update to 0.16
  - Remove accidental Sub::Name test dependency

* Tue Jul  9 2013 Paul Howarth <paul@city-fan.org> - 0.15-1
- Update to 0.15
  - Optionally use Sub::Name to name the try/catch/finally blocks, if available
- BR:/R: perl(Sub::Name)
- Drop obsoletes/provides for old -tests subpackage

* Sat Jul  6 2013 Paul Howarth <paul@city-fan.org> - 0.14-1
- Update to 0.14
  - Also throw an exception for catch/finally in scalar context (CPAN RT#81070)

* Fri Jul  5 2013 Paul Howarth <paul@city-fan.org> - 0.13-1
- Update to 0.13
  - Fix tests failing on 5.6.x due to differing DESTROY semantics
  - Excise superfluous local($@) call - 7%% speedup
  - Fix broken URLs (CPAN RT#55659)
  - Proper exception on erroneous usage of bare catch/finally (CPAN RT#81070)
  - Proper exception on erroneous use of multiple catch{} blocks
  - Clarify exception occuring on unterminated try block (CPAN RT#75712)
  - Fix the prototypes shown in docs to match code (CPAN RT#79590)
  - Warn loudly on exceptions in finally() blocks
  - dzilify
- Ship upstream LICENSE and README files
- Classify buildreqs by usage
- Add buildreqs for extra tests and explicitly run them

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan  2 2013 Paul Howarth <paul@city-fan.org> - 0.12-1
- Update to 0.12
  - Documentation fixes

* Tue Aug 28 2012 Jitka Plesnikova <jplesnik@redhat.com> - 0.11-7
- Add BR/R perl(Exporter)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 08 2012 Petr Pisar <ppisar@redhat.com> - 0.11-5
- Perl 5.16 rebuild

* Mon Mar 26 2012 Paul Howarth <paul@city-fan.org> - 0.11-4
- BR: perl(Carp)
- Don't need to remove empty directories from buildroot
- Don't use macros for commands
- Drop redundant %%{?perl_default_filter}
- Enhance %%description
- Reinstate EPEL-5 compatibility:
  - Define buildroot
  - Clean buildroot in %%install and %%clean
- Use tabs

* Sun Jan 22 2012 Iain Arnell <iarnell@gmail.com> - 0.11-3
- Drop tests subpackage; move tests to main package documentation

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Iain Arnell <iarnell@gmail.com> - 0.11-1
- Update to latest upstream version

* Wed Jun 15 2011 Marcela Mašláňová <mmaslano@redhat.com> - 0.09-2
- Perl mass rebuild

* Fri Mar 18 2011 Iain Arnell <iarnell@gmail.com> - 0.09-1
- Update to latest upstream version
- Clean up spec for modern rpmbuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  1 2010 Paul Howarth <paul@city-fan.org> - 0.07-1
- Update to 0.07
  - Allow multiple finally blocks
  - Pass the error, if any, to finally blocks when called
  - Documentation fixes and clarifications
- This release by RJBS -> update source URL

* Fri May 07 2010 Marcela Maslanova <mmaslano@redhat.com> - 0.04-2
- Mass rebuild with perl-5.12.0

* Tue Mar 02 2010 Chris Weyl <cweyl@alumni.drew.edu> - 0.04-1
- Update by Fedora::App::MaintainerTools 0.004
- PERL_INSTALL_ROOT => DESTDIR
- Updating to latest GA CPAN version (0.04)

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 0.02-2
- Rebuild against perl 5.10.1

* Tue Sep 15 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-1
- Submission

* Tue Sep 15 2009 Chris Weyl <cweyl@alumni.drew.edu> - 0.02-0
- Initial RPM packaging
- Generated with cpan2dist (CPANPLUS::Dist::RPM version 0.0.8)
