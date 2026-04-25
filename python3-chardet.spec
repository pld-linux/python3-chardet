#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tets

%define		module	chardet
Summary:	Character encoding auto-detection in Python 3
Summary(pl.UTF-8):	Automatyczne wykrywanie kodowania znaków w Pythonie 3
Name:		python3-%{module}
Version:	7.4.3
Release:	1
License:	0BSD
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/chardet/
Source0:	https://files.pythonhosted.org/packages/source/c/chardet/%{module}-%{version}.tar.gz
# Source0-md5:	df96bc7067630990c971ea95001f5687
URL:		https://pypi.org/project/chardet/
BuildRequires:	python3 >= 1:3.10
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-hatchling
BuildRequires:	python3-hatch-vcs
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-hypothesis
BuildRequires:	python3-pytest
# >= 9.0.2 when available in PLD
%endif
%if %{with doc}
BuildRequires:	python3-furo >= 2024.1.29
BuildRequires:	python3-sphinx_copybutton >= 0.5.2
BuildRequires:	sphinx-pdg-3 >= 8.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.10
Conflicts:	python-chardet < 4.0.0-7
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

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests -m "not benchmark"
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/chardetect
%{py3_sitescriptdir}/chardet
%{py3_sitescriptdir}/chardet-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,api,*.html,*.js}
%endif
