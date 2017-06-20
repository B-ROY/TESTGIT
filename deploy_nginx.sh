#!/usr/bin/env bash

# names of latest versions of each package
export NGINX_VERSION=1.11.6
export VERSION_PCRE=pcre-8.38
export VERSION_LIBRESSL=libressl-2.5.0
export VERSION_NGINX=nginx-$NGINX_VERSION
#export NPS_VERSION=1.9.32.10
#export VERSION_PAGESPEED=v${NPS_VERSION}-beta

# URLs to the source directories
export SOURCE_LIBRESSL=http://ftp.openbsd.org/pub/OpenBSD/LibreSSL/
export SOURCE_PCRE=ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/
export SOURCE_NGINX=http://nginx.org/download/
#export SOURCE_RTMP=https://github.com/arut/nginx-rtmp-module.git
#export SOURCE_PAGESPEED=https://github.com/pagespeed/ngx_pagespeed/archive/

# clean out any files from previous runs of this script
#rm -rf build
#mkdir build

# proc for building faster
NB_PROC=$(grep -c ^processor /proc/cpuinfo)

#wget -c http://checkinstall.izto.org/files/source/checkinstall-1.6.2.tar.gz
#yum install git

# ensure that we have the required software to compile our own nginx
#sudo apt-get -y install curl wget build-essential libgd-dev libgeoip-dev checkinstall git

# grab the source files
echo "Download sources"
wget -P ./ $SOURCE_PCRE$VERSION_PCRE.tar.gz --no-check-certificate
wget -P ./ $SOURCE_LIBRESSL$VERSION_LIBRESSL.tar.gz
wget -P ./ $SOURCE_NGINX$VERSION_NGINX.tar.gz
#wget -P ./build $SOURCE_PAGESPEED$VERSION_PAGESPEED.tar.gz
#wget -P ./build https://dl.google.com/dl/page-speed/psol/${NPS_VERSION}.tar.gz
#git clone $SOURCE_RTMP ./build/rtmp

# expand the source files
echo "Extract Packages"
cd /mydata/downloads
tar xzf $VERSION_NGINX.tar.gz
tar xzf $VERSION_LIBRESSL.tar.gz
tar xzf $VERSION_PCRE.tar.gz
#tar xzf $VERSION_PAGESPEED.tar.gz
#tar xzf ${NPS_VERSION}.tar.gz -C ngx_pagespeed-${NPS_VERSION}-beta
cd ../
# set where LibreSSL and nginx will be built
export BPATH=/mydata/downloads
export STATICLIBSSL=$BPATH/$VERSION_LIBRESSL

# build static LibreSSL
echo "Configure & Build LibreSSL"
cd $STATICLIBSSL

#./configure LDFLAGS=-lrt --prefix=${STATICLIBSSL}/.openssl/ && make install-strip -j $NB_PROC

# build nginx, with various modules included/excluded
echo "Configure & Build Nginx"
cd $BPATH/$VERSION_NGINX
#echo "Download and apply path"
#wget -q -O - $NGINX_PATH | patch -p0

mkdir -p $BPATH/nginx
./configure  --with-openssl=$STATICLIBSSL \
--with-ld-opt="-lrt"  \
--prefix=/mydata/nginx \
--with-pcre=$BPATH/$VERSION_PCRE \
--with-http_ssl_module \
--with-http_v2_module \
--add-module=/mydata/downloads/ngx_devel_kit-0.2.19 \
--add-module=/mydata/downloads/lua-nginx-module-0.10.2 \
--with-pcre=$BPATH/$VERSION_PCRE \
--with-file-aio \
--with-ipv6 \
--with-http_gzip_static_module \
--with-http_stub_status_module \
 --with-debug \
 --with-pcre-jit \
 --with-http_stub_status_module \
 --with-http_realip_module \
 --with-http_auth_request_module \
 --with-http_addition_module \
 --with-http_gzip_static_module
# --add-module=$BPATH/rtmp
 #--add-module=$BPATH/ngx_pagespeed-${NPS_VERSION}-beta
mkdir -p $STATICLIBSSL/.openssl/include/openssl/
touch $STATICLIBSSL/.openssl/include/openssl/ssl.h
make -j $NB_PROC
make install
#&& sudo checkinstall --pkgname="nginx-libressl" --pkgversion="$NGINX_VERSION" \
#--provides="nginx" --requires="libc6, libpcre3, zlib1g" --strip=yes \
#--stripso=yes --backup=yes -y --install=yes

echo "All done.";
echo "This build has not edited your existing /etc/nginx directory.";
echo "If things aren't working now you may need to refer to the";
echo "configuration files the new nginx ships with as defaults,";
echo "which are available at /etc/nginx-default";

