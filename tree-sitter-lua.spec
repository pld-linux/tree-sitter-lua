Summary:	Lua grammar for tree-sitter
Name:		tree-sitter-lua
Version:	0.2.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/tree-sitter-grammars/tree-sitter-lua/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e851527aa24801b8e9dcd1fb9eb3693f
URL:		https://github.com/tree-sitter-grammars/tree-sitter-lua
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		ts_lua_soname	libtree-sitter-lua.so.0

%description
Lua grammar for tree-sitter.

%package devel
Summary:	Header files for tree-sitter-lua
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for tree-sitter-lua.

%package static
Summary:	Static tree-sitter-lua library
Group:		Development/Libraries
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description static
Static tree-sitter-lua library.

%package -n neovim-parser-lua
Summary:	Lua parser for Neovim
Group:		Applications/Editors
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description -n neovim-parser-lua
Lua parser for Neovim.

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

%{__ln_s} %{_libdir}/%{ts_lua_soname} $RPM_BUILD_ROOT%{_libdir}/nvim/parser/lua.so

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%attr(755,root,root) %{_libdir}/libtree-sitter-lua.so.*.*
%attr(755,root,root) %ghost %{_libdir}/%{ts_lua_soname}

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtree-sitter-lua.so
%{_includedir}/tree_sitter/tree-sitter-lua.h
%{_pkgconfigdir}/tree-sitter-lua.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libtree-sitter-lua.a

%files -n neovim-parser-lua
%defattr(644,root,root,755)
%{_libdir}/nvim/parser/lua.so
