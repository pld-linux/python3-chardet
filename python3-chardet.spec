#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tets

%define		module	chardet
Summary:	Character encoding auto-detection in Python 3
Summary(pl.UTF-8):	Automatyczne wykrywanie kodowania znaków w Pythonie 3
Name:		python3-%{module}
Version:	5.2.0
Release:	1
License:	LGPL v2.1+
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/chardet/
Source0:	https://files.pythonhosted.org/packages/source/c/chardet/%{module}-%{version}.tar.gz
# Source0-md5:	cc2d8cc9a751641463b4f7cfecad2ffa
Patch0:		failtest.patch
URL:		https://pypi.org/project/chardet/
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-devel >= 1:3.7
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Character encoding auto-detection in Python. As smart as your browser.

%description -l pl.UTF-8
Automatyczne wykrywanie kodowania znaków w Pythonie. Tak zmyślne jak w
przeglądarce.

%package apidocs
Summary:	API documentation for Python chardet module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona chardet
Group:		Documentation

%description apidocs
API documentation for Python chardet module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona chardet.

%prep
%setup -q -n %{module}-%{version}
%patch -P 0 -p1

cat > setup.py <<EOF
#!%{_bindir}/python3
from setuptools import setup
setup()
EOF

%build
%py3_build

%if %{with tests}
%{__python3} -m pytest test.py
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%attr(755,root,root) %{_bindir}/chardetect
%{py3_sitescriptdir}/chardet
%{py3_sitescriptdir}/chardet-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,api,*.html,*.js}
%endif
