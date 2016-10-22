%{?scl:%scl_package perl-Try-Tiny}

Name:		%{?scl_prefix}perl-Try-Tiny
Summary:	Minimal try/catch with proper localization of $@
Version:	0.24
Release:	4%{?dist}
License:	MIT
URL:		http://search.cpan.org/dist/Try-Tiny
Source0:	http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Try-Tiny-%{version}.tar.gz
BuildArch:	noarch
# Module Build
BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	make
BuildRequires:	%{?scl_prefix}perl
BuildRequires:	%{?scl_prefix}perl-generators
BuildRequires:	%{?scl_prefix}perl(ExtUtils::MakeMaker)
# Module
BuildRequires:	%{?scl_prefix}perl(Carp)
BuildRequires:	%{?scl_prefix}perl(constant)
BuildRequires:	%{?scl_prefix}perl(Exporter) >= 5.57
BuildRequires:	%{?scl_prefix}perl(strict)
BuildRequires:	%{?scl_prefix}perl(Sub::Util)
BuildRequires:	%{?scl_prefix}perl(warnings)
# Test Suite
BuildRequires:	%{?scl_prefix}perl(File::Spec)
BuildRequires:	%{?scl_prefix}perl(Test::More)
# Optional Tests
%if !%{defined perl_small}
BuildRequires:	%{?scl_prefix}perl(Capture::Tiny) >= 0.12
%endif
BuildRequires:	%{?scl_prefix}perl(CPAN::Meta) >= 2.120900
# Runtime
Requires:	%{?scl_prefix}perl(:MODULE_COMPAT_%(%{?scl:scl enable %{scl} '}eval "$(perl -V:version)";echo $version%{?scl:'}))
Requires:	%{?scl_prefix}perl(Sub::Util)

# Do not provide private modules from tests packaged as a documentation
%if 0%{?rhel} < 7
# RPM 4.8 style
%{?filter_setup:
%filter_provides_in ^%{_docdir}/
%?perl_default_filter
}
%else
# RPM 4.9 style
%global __provides_exclude_from %{?__provides_exclude_from:%__provides_exclude_from|}^%{_docdir}/
%endif

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
%{?scl:scl enable %{scl} '}perl Makefile.PL INSTALLDIRS=vendor && make %{?_smp_mflags}%{?scl:'}

%install
%{?scl:scl enable %{scl} '}make pure_install DESTDIR=%{buildroot}%{?scl:'}
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
%{_fixperms} %{buildroot}

%check
%{?scl:scl enable %{scl} '}make test%{?scl:'}

%files
%doc LICENCE
%doc Changes CONTRIBUTING README t/
%{perl_vendorlib}/Try/
%{_mandir}/man3/Try::Tiny.3*

%changelog
* Tue Jul 12 2016 Petr Pisar <ppisar@redhat.com> - 0.24-4
- SCL

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.24-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 11 2015 Paul Howarth <paul@city-fan.org> - 0.24-1
- Update to 0.24
  - Fix syntax of example code (PR#22)
  - 'perl' removed from prerequisite recommendations, to avoid tripping up CPAN
    clients
  - Sub::Util is used preferentially to Sub::Name in most cases (PR#27)
- This release by ETHER → update source URL
- Modernize spec
- Don't run the extra tests

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-5
- Perl 5.22 rebuild

* Thu Jan 15 2015 Petr Pisar <ppisar@redhat.com> - 0.22-4
- Correct dependencies

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.22-3
- Perl 5.20 rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Paul Howarth <paul@city-fan.org> - 0.22-1
- Update to 0.22
  - Add optional test deps as recommended prereqs
    (https://github.com/doy/try-tiny/pull/18)
- Update patch for building with Test::More < 0.88

* Tue Apr 15 2014 Paul Howarth <paul@city-fan.org> - 0.21-1
- Update to 0.21
  - Also skip the test if Capture::Tiny is too old
    (https://github.com/doy/try-tiny/issues/17)

* Sat Mar 22 2014 Paul Howarth <paul@city-fan.org> - 0.20-1
- Update to 0.20
  - Documentation updates
- Update patch for building with Test::More < 0.88

* Thu Jan 23 2014 Paul Howarth <paul@city-fan.org> - 0.19-1
- Update to 0.19
  - Fix an obscure issue with loading modules during global destruction
    (https://github.com/doy/try-tiny/pull/11)
  - Documentation updates (https://github.com/doy/try-tiny/pull/12)
- Add patch to support building with Test::More < 0.88 again

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
