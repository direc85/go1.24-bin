# Ignore missing build-id links for now
%global _missing_build_ids_terminate_build 0

# go_api is the major version of Go.
# Used by go1.x packages and go metapackage for:
# RPM Provides: golang(API), RPM Requires: and rpm_vercmp
# as well as derived variables such as go_label.
%define go_api 1.24

# go_label is the configurable Go toolchain directory name.
# Used for packaging multiple Go toolchains with the same go_api.
# go_label should be defined as go_api with optional suffix, e.g.
# go_api or go_api-foo
%define go_label %{go_api}

# This is a binary re-package, no need for strip
%define __strip /bin/true

%define go_arch arm64

Name:           go1.24-bin
Version:        1.24.0
Release:        1
Summary:        A compiled, garbage-collected, concurrent programming language
License:        BSD-3-Clause
Group:          Development/Languages/Go
URL:            https://github.com/sailfishos-mirror/go/
Source:         go1.24.0-aarch64.tar.xz

Suggests:       %{name}-doc = %{version}
Suggests:       %{name}-libstd = %{version}
BuildRequires:  gcc-c++
#BNC#818502 debug edit tool of rpm fails on i586 builds
BuildRequires:  rpm >= 4.11.1
Requires:       gcc

# Binary repackage provides
Provides:       go1.24

Provides:       go = %{version}
Provides:       go-devel = go%{version}
Provides:       go-devel-static = go%{version}
Provides:       golang(API) = %{go_api}
Obsoletes:      go-devel < go%{version}
# go-vim/emacs were separate projects starting from 1.4
Obsoletes:      go-emacs <= 1.3.3
Obsoletes:      go-vim <= 1.3.3
ExclusiveArch:  aarch64

%description
Go is an expressive, concurrent, garbage collected systems programming language
that is type safe and memory safe. It has pointers but no pointer arithmetic.
Go has fast builds, clean syntax, garbage collection, methods for any type, and
run-time reflection. It feels like a dynamic language but has the speed and
safety of a static language.

%package doc
Summary:        Go documentation
Group:          Documentation/Other
Provides:       go-doc = %{version}

%description doc
Go examples and documentation.

%package race
Summary:        Go runtime race detector
Group:          Development/Languages/Go
URL:            https://compiler-rt.llvm.org/
Requires:       %{name} = %{version}
Supplements:    %{name} = %{version}
ExclusiveArch:  %{tsan_arch}

%description race
Go runtime race detector libraries. Install this package if you wish to use the
-race option, in order to detect race conditions present in your Go programs.

%prep

%build

%install
pushd "%{buildroot}" 
tar xf %{SOURCE0}
popd

%files
%{_bindir}/go
%{_bindir}/gofmt
%dir %{_libdir}/go
%{_libdir}/go/%{go_label}
%dir %{_datadir}/go
%{_datadir}/go/%{go_label}
%dir %{_sysconfdir}/gdbinit.d/
%config %{_sysconfdir}/gdbinit.d/go.gdb
%ghost %{_sysconfdir}/alternatives/go
%ghost %{_sysconfdir}/alternatives/gofmt
%ghost %{_sysconfdir}/alternatives/go.gdb
%dir %{_docdir}/go
%dir %{_docdir}/go/%{go_label}
%doc %{_docdir}/go/%{go_label}/CONTRIBUTING.md
%doc %{_docdir}/go/%{go_label}/PATENTS
%doc %{_docdir}/go/%{go_label}/README.md
%doc %{_docdir}/go/%{go_label}/LICENSE
%license %{_docdir}/go/%{go_label}/LICENSE

# We don't include TSAN in the main Go package.
%exclude %{_datadir}/go/%{go_label}/src/runtime/race/race_linux_%{go_arch}.syso

%files doc
# SLE-12 SP5 rpm macro environment does not work with single glob {*.html,godebug.md}
%doc %{_docdir}/go/%{go_label}/*.html
%doc %{_docdir}/go/%{go_label}/godebug.md

%files race
%{_datadir}/go/%{go_label}/src/runtime/race/race_linux_%{go_arch}.syso

%changelog

