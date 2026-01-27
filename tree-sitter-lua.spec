#
# Conditional build:
%bcond_without	python3	# Python 3.x binding
%bcond_without	tests	# Python binding load test

Summary:	Lua grammar for tree-sitter
Summary(pl.UTF-8):	Gramatyka języka Lua dla tree-sittera
Name:		tree-sitter-lua
Version:	0.4.1
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/tree-sitter-grammars/tree-sitter-lua/releases
Source0:	https://github.com/tree-sitter-grammars/tree-sitter-lua/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	52f8009d0bd6052557b10df0cb1028e8
URL:		https://github.com/tree-sitter-grammars/tree-sitter-lua
# c11
BuildRequires:	gcc >= 6:4.7
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-setuptools >= 1:42
BuildRequires:	python3-wheel
%if %{with tests}
BuildRequires:	python3-tree-sitter >= 0.24
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		soname_ver	15.0

%description
Lua grammar for tree-sitter.

%description -l pl.UTF-8
Gramatyka języka Lua dla tree-sittera.

%package devel
Summary:	Header files for tree-sitter-lua
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tree-sitter-lua
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-lua.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki tree-sitter-lua.

%package static
Summary:	Static tree-sitter-lua library
Summary(pl.UTF-8):	Statyczna biblioteka tree-sitter-lua
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-lua library.

%description static -l pl.UTF-8
Statyczna biblioteka tree-sitter-lua.

%package -n neovim-parser-lua
Summary:	Lua parser for Neovim
Summary(pl.UTF-8):	Analizator składni języka Lua dla Neovima
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-lua
Lua parser for Neovim.

%description -n neovim-parser-lua -l pl.UTF-8
Analizator składni języka Lua dla Neovima.

%package -n python3-tree-sitter-lua
Summary:	Lua parser for Python
Summary(pl.UTF-8):	Analizator składni języka Lua dla Pythona
Group:		Libraries/Python
Requires:	python3-tree-sitter >= 0.24

%description -n python3-tree-sitter-lua
Lua parser for Python.

%description -n python3-tree-sitter-lua -l pl.UTF-8
Analizator składni języka Lua dla Pythona.

%prep
%setup -q

%build
%{__make} \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}" \
	CC="%{__cc}" \
	CFLAGS="%{rpmcppflags} %{rpmcflags}" \
	LDFLAGS="%{rpmldflags}"

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(readlink -f build-3/lib.*) \
%{__python3} -m unittest discover -s bindings/python/tests
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/nvim/parser

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	PREFIX="%{_prefix}" \
	INCLUDEDIR="%{_includedir}" \
	LIBDIR="%{_libdir}" \
	PCLIBDIR="%{_pkgconfigdir}"

%{__ln_s} -f libtree-sitter-lua.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-lua.so

%{__ln_s} ../../libtree-sitter-lua.so.%{soname_ver} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/lua.so

# redundant symlink
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libtree-sitter-lua.so.15

%if %{with python3}
%py3_install

%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/tree_sitter_lua/*.c
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%{_libdir}/libtree-sitter-lua.so.%{soname_ver}
# XXX: who should own top dirs?
%dir %{_datadir}/tree-sitter
%dir %{_datadir}/tree-sitter/queries
%{_datadir}/tree-sitter/queries/lua

%files devel
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-lua.so
%{_includedir}/tree_sitter/tree-sitter-lua.h
%{_pkgconfigdir}/tree-sitter-lua.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-lua.a

%files -n neovim-parser-lua
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/lua.so

%if %{with python3}
%files -n python3-tree-sitter-lua
%defattr(644,root,root,755)
%dir %{py3_sitedir}/tree_sitter_lua
%{py3_sitedir}/tree_sitter_lua/_binding.abi3.so
%{py3_sitedir}/tree_sitter_lua/__init__.py
%{py3_sitedir}/tree_sitter_lua/__init__.pyi
%{py3_sitedir}/tree_sitter_lua/py.typed
%{py3_sitedir}/tree_sitter_lua/__pycache__
%{py3_sitedir}/tree_sitter_lua/queries
%{py3_sitedir}/tree_sitter_lua-%{version}-py*.egg-info
%endif
