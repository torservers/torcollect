#!/bin/bash

mv torcollect torcollect_src
mkdir -p torcollect/DEBIAN
mkdir -p torcollect/usr/lib/python2.7/dist-packages
mkdir -p torcollect/usr/bin
mkdir -p torcollect/etc/apache2/sites-available
mkdir -p torcollect/var/www_torcollect

cp bin/* torcollect/usr/bin/
chmod 755 torcollect/usr/bin/*
cp -r torcollect_src torcollect/usr/lib/python2.7/dist-packages/torcollect
cp resources/debian_package/* torcollect/DEBIAN/
cp -r web/* torcollect/var/www_torcollect/
cp resources/apache2_config torcollect/etc/apache2/sites-available/
cp resources/database.sql torcollect/usr/share/torcollect/

SIZE=`du -c -s torcollect/usr torcollect/var torcollect/etc | tail -n1 |  cut -f1`
sed s/\$SIZE/$SIZE/g torcollect/DEBIAN/control > torcollect/DEBIAN/control2
mv torcollect/DEBIAN/control2 torcollect/DEBIAN/control
echo $SIZE
dpkg-deb -z6 -Zgzip --build torcollect
rm -r torcollect
mv torcollect_src torcollect
