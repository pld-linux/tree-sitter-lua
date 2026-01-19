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
