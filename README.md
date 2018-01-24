# MapServer 7.0.7 Spec

Spec file for building MapServer RPMs

MapServer compilation with Oracle Spatial support and only Python MapScript


## Instructions

Requires EPEL Repository and Oracle InstantClient libraries

``` 
$ yum -y install git rpm-build rpmdevtools yum-utils
$ rpmdev-setuptree
$ spectool -g -C ~/rpmbuild/SOURCES mapserver-7.0.7.spec
$ yum-builddep -y mapserver-7.0.7.spec
$ QA_RPATHS=$[ 0x0001|0x0002 ] rpmbuild -ba --target x86_64 mapserver-7.0.7.spec
```

Tested in CentOS 7
