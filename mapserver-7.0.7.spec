%define MS_REL %{nil}

Name:           mapserver%{MS_REL}
Version:        7.0.7
Release:        1%{?dist}
Summary:        Environment for building spatially-enabled internet applications

Group:          Development/Tools
License:        BSD
URL:            http://www.mapserver.org

Source0:        http://download.osgeo.org/mapserver/mapserver-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  cmake make gcc gcc-c++
BuildRequires:  libXpm-devel readline-devel librsvg2-devel
BuildRequires:  libxslt-devel pam-devel fcgi-devel
BuildRequires:  postgresql-devel
BuildRequires:  swig > 1.3.24
BuildRequires:  geos-devel proj-devel gdal-devel cairo-devel
BuildRequires:  freetype-devel gd-devel >= 2.0.16
BuildRequires:  python-devel curl-devel zlib-devel libxml2-devel
BuildRequires:  libjpeg-devel libpng-devel libtiff-devel fribidi-devel giflib-devel
BuildRequires:  harfbuzz-devel

%define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

%description
Mapserver is an internet mapping program that converts GIS data to
map images in real time. With appropriate interface pages, 
Mapserver can provide an interactive internet map based on 
custom GIS data.

%package python
Summary:        Python/Mapscript map making extensions to Python
Group:          Development/Languages
Requires:       %{name} = %{version}-%{release}

%description python
The Python/Mapscript extension provides full map customization capabilities
within the Python programming language.

%prep
%setup -q -n mapserver-%{version}

# fix spurious perm bits
chmod -x mapscript/python/examples/*.py
chmod -x mapscript/python/tests/rundoctests.dist

# replace fonts for tests with symlinks
rm -rf tests/vera/Vera.ttf
rm -rf tests/vera/VeraBd.ttf
pushd tests/vera/
ln -sf /usr/share/fonts/dejavu/DejaVuSans.ttf Vera.ttf
ln -sf /usr/share/fonts/dejavu/DejaVuSans-Bold.ttf VeraBd.ttf
popd

%build
mkdir build
pushd build

%cmake -DINSTALL_LIB_DIR=%{_libdir} \
       -DWITH_CLIENT_WFS=ON \
       -DWITH_CLIENT_WMS=ON \
       -DWITH_CURL=ON \
       -DWITH_SOS=ON \
       -DWITH_PHP=OFF \
       -DWITH_PYTHON=ON \
       -DWITH_PERL=OFF \
       -DWITH_JAVA=OFF \
       -DWITH_POSTGIS=ON \
       -DWITH_OGR=ON \
       -DWITH_PROJ=ON \
       -DWITH_RSVG=ON \
       -DWITH_KML=ON \
       -DWITH_SOS=ON \
       -DWITH_FRIBIDI=ON \
       -DWITH_ICONV=ON \
       -DWITH_CAIRO=ON \
       -DWITH_FCGI=ON \
       -DWITH_GEOS=ON \
       -DWITH_GDAL=ON \
       -DWITH_WFS=ON \
       -DWITH_WCS=ON \
       -DWITH_LIBXML2=ON \
       -DWITH_THREAD_SAFETY=ON \
       -DWITH_GIF=ON \
       -DORACLE_INCLUDE_DIR=/usr/lib/oracle/11.2/client64/include \
       -DWITH_ORACLESPATIAL=ON ..

make
popd

%install
pushd build
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
popd

mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_datadir}/%{name}

mv %{buildroot}/%{_bindir}/mapserv %{buildroot}%{_libexecdir}/mapserv%{MS_REL}

install -p -m 644 xmlmapfile/mapfile.xsd %{buildroot}%{_datadir}/%{name}
install -p -m 644 xmlmapfile/mapfile.xsl %{buildroot}%{_datadir}/%{name}

# cleanup junks
for junk in {*.pod,*.bs,.packlist} ; do
find %{buildroot} -name "$junk" -exec rm -rf '{}' \;
done

%files
%defattr(-,root,root)
%doc README HISTORY.TXT  
%doc INSTALL MIGRATION_GUIDE.txt
%doc symbols tests
%doc fonts
%{_bindir}/legend%{MS_REL}
%{_bindir}/msencrypt%{MS_REL}
%{_bindir}/scalebar%{MS_REL}
%{_bindir}/shp2img%{MS_REL}
%{_bindir}/shptree%{MS_REL}
%{_bindir}/shptreetst%{MS_REL}
%{_bindir}/shptreevis%{MS_REL}
%{_bindir}/sortshp%{MS_REL}
%{_bindir}/tile4ms%{MS_REL}
%{_libdir}/libmapserver.so
%{_libdir}/libmapserver.so.2
%{_libdir}/libmapserver.so.%{version}
%{_libexecdir}/mapserv
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%{_includedir}/*

%files python
%defattr(-,root,root)
%doc mapscript/python/README
%doc mapscript/python/examples
%doc mapscript/python/tests
%{python_sitearch}/*
