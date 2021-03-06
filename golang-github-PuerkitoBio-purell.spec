%if 0%{?fedora} || 0%{?rhel} == 6
%global with_devel 1
%global with_bundled 0
%global with_debug 0
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 0
%global with_bundled 0
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         PuerkitoBio
%global repo            purell
# https://github.com/PuerkitoBio/purell
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit 0bcb03f4b4d0a9428594752bd2a3b9aa0a9d4bd4
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        1.1.0
Release:        9%{?dist}
Summary:        Tiny Go library to normalize URLs
License:        BSD
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/v%{version}/%{name}-%{version}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
Purell is a tiny Go library to normalize URLs. It returns a pure URL.
Based on the wikipedia paper (URL_normalization) and the RFC 3986 document.

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/PuerkitoBio/urlesc)
BuildRequires: golang(golang.org/x/net/idna)
BuildRequires: golang(golang.org/x/text/unicode/norm)
BuildRequires: golang(golang.org/x/text/width)
%endif

Requires:      golang(github.com/PuerkitoBio/urlesc)
Requires:      golang(golang.org/x/net/idna)
Requires:      golang(golang.org/x/text/unicode/norm)
Requires:      golang(golang.org/x/text/width)

Provides:      golang(%{import_path}) = %{version}-%{release}

%description devel
Purell is a tiny Go library to normalize URLs. It returns a pure URL.
Based on the wikipedia paper (URL_normalization) and the RFC 3986 document.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test-devel
Purell is a tiny Go library to normalize URLs. It returns a pure URL.
Based on the wikipedia paper (URL_normalization) and the RFC 3986 document.

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%autosetup -n %{repo}-%{version}

%build

%install
# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md
%endif

%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 15 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 1.1.0-5
- Include cvs revision information for golang tools

* Tue Mar 14 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 1.1.0-4
- Run all tests
- Remove empty conditionals
- Fix GOPATH in %%check
- Improve Source URL

* Sun Mar 12 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 1.1.0-3
- Remove package name from summary
- Use dist tag

* Sun Feb 26 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 1.1.0-2
- Use different version of urlesc

* Sun Feb 26 2017 Athos Ribeiro <athoscr@fedoraproject.org> - 1.1.0-1
- Update version

* Sun Nov 13 2016 Athos Ribeiro <athoscr@fedoraproject.org> - 1.0.0-1
- Initial package
