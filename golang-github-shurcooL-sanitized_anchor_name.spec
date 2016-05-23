#
# Conditional build:
%bcond_without	src		# build devel package with sources
%bcond_without	tests	# build without tests

%define		rel	1
%define		commit	10ef21a
%define		pkgname		sanitized_anchor_name
Summary:	Package sanitized_anchor_name provides a func to create sanitized anchor names
Name:		golang-github-shurcooL-%{pkgname}
Version:	0
Release:	%{rel}.%{commit}
License:	MIT
Group:		Libraries
Source0:	https://github.com/shurcooL/sanitized_anchor_name/archive/%{commit}/sanitized_anchor_name-%{commit}.tar.gz
# Source0-md5:	4c5e1f92888b9553363c2e94151aa1f0
URL:		https://github.com/shurcooL/sanitized_anchor_name
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/shurcooL/%{pkgname}

%description
%{summary}

%package devel
Summary:	%{summary}
Provides:	golang(%{import_path}) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for building other
packages which use import path with %{import_path} prefix.

%prep
%setup -qc -n %{pkgname}-%{commit}
mv %{pkgname}-*/* .

%build
%if %{with test}
export GOPATH=$(pwd):%{gopath}

go test %{import_path}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with src}
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go"); do
	echo "%dir %{gopath}/src/%{import_path}/$(dirname $file)" >> devel.file-list
	install -d -p $RPM_BUILD_ROOT%{gopath}/src/%{import_path}/$(dirname $file)
	cp -pav $file $RPM_BUILD_ROOT%{gopath}/src/%{import_path}/$file
	echo "%{gopath}/src/%{import_path}/$file" >> devel.file-list
done
sort -u -o devel.file-list devel.file-list
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with src}
%files devel -f devel.file-list
%defattr(644,root,root,755)
%doc README.md LICENSE
%dir %{gopath}/src/github.com
%dir %{gopath}/src/github.com/shurcooL
%endif
