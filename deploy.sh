#!/bin/bash
if [ ! -d "/mydata/downloads" ];then
 mkdir -p /mydata/downloads
fi
echo '[start install g++!]'
yum -y install gcc-c++.x86_64

yum -y install wget
yum -y install gcc
yum -y install gcc-c++
yum -y install openssl-devel
yum -y install readline-devel
yum -y install mysql-devel



echo '[start install pcre!]'
cd /mydata/downloads/
wget -O pcre-8.38.tar.gz http://sourceforge.net/projects/pcre/files/pcre/8.38/pcre-8.38.tar.gz/download --no-check-certificate
tar zxvf pcre-8.38.tar.gz
cd pcre-8.38
./configure
make
make install

cd /lib64/
ln -s libpcre.so.0.0.1 libpcre.so.1
ldconfig

echo '[start install zlib!]'
cd /mydata/downloads/
wget https://prdownloads.sourceforge.net/libpng/zlib-1.2.7.tar.gz --no-check-certificate
tar zxvf zlib-1.2.7.tar.gz
cd  zlib-1.2.7
./configure --prefix=/usr/local
make 
make install



cd /mydata/downloads/ 
wget http://www.lua.org/ftp/lua-5.1.2.tar.gz --no-check-certificate
tar zxvf lua-5.1.2.tar.gz
cd lua-5.1.2
make linux
make install

cd /mydata/downloads/ 
wget http://luajit.org/download/LuaJIT-2.1.0-beta2.tar.gz
tar zxvf LuaJIT-2.1.0-beta2.tar.gz
cd LuaJIT-2.1.0-beta2
make
make install

cd /mydata/downloads/ 
wget https://codeload.github.com/simpl/ngx_devel_kit/tar.gz/v0.2.19
tar zxvf v0.2.19

cd /mydata/downloads/ 
wget https://codeload.github.com/openresty/lua-nginx-module/tar.gz/v0.10.2
tar zxvf v0.10.2

export LUAJIT_LIB=/usr/local/lib 
export LUAJIT_INC=/usr/local/include/luajit

#vim .bash_profile 

num=$( cat /root/.bash_profile|grep -c LUAJIT_LIB ) 
if [ $num = 0 ];then 
   echo "OK-O-O-O write hosts"
   echo 'export LUAJIT_LIB=/usr/local/lib'>> /root/.bash_profile
   echo 'export LUAJIT_INC=/usr/local/include/luajit-2.0'>> /root/.bash_profile
fi 


#ssl http://manual.seafile.com/deploy/https_with_nginx.html
#openssl genrsa -out privkey.pem 2048
#openssl req -new -x509 -key privkey.pem -out cacert.pem -days 1095openssl req -new -x509 -key privkey.pem -out cacert.pem -days 1095
echo '[start install nginx-1.11.6!]'
cd /mydata/downloads/
wget http://nginx.org/download/nginx-1.11.6.tar.gz
tar zxvf nginx-1.11.6.tar.gz
cd nginx-1.11.6
./configure --prefix=/mydata/nginx --add-module=/mydata/downloads/ngx_devel_kit-0.2.19 --add-module=/mydata/downloads/lua-nginx-module-0.10.2   --with-pcre=/mydata/downloads/pcre-8.38  --with-http_stub_status_module --with-http_ssl_module
make
make install



echo '[start install python!]'
cd /mydata/downloads/
wget http://www.python.org/ftp/python/2.7.2/Python-2.7.2.tgz
tar zxf Python-2.7.2.tgz
cd Python-2.7.2
./configure --prefix=/mydata/python2.7
make
make install
export PATH=/mydata/python2.7/bin:$PATH
echo "export PATH=/mydata/python2.7/bin:\$PATH" > /etc/profile.d/python.sh

echo "[setup setuptools from ]"
cd /mydata/downloads/
wget --no-check-certificate  http://pypi.python.org/packages/source/s/setuptools/setuptools-0.6c11.tar.gz#md5=7df2a529a074f613b509fb44feefe74etar zxvf setuptools-0.6c11.tar.gz
tar zxvf setuptools-0.6c11.tar.gz
cd setuptools-0.6c11
/mydata/python2.7/bin/python setup.py install


cd /mydata/downloads/
wget http://pypi.python.org/packages/source/d/distribute/distribute-0.6.28.tar.gz
cd distribute-0.6.28
tar xzvf distribute-0.6.28.tar.gz
cd distribute-0.6.28
/mydata/python2.7/bin/python setup.py install


cd /mydata/downloads/
wget  --no-check-certificate https://codeload.github.com/farcepest/MySQLdb1/zip/utf8mb4
unzip utf8mb4
cd MySQLdb1-utf8mb4/
/mydata/python2.7/bin/python setup.py install

cd /mydata/downloads/
wget https://pypi.python.org/packages/source/r/rsa/rsa-3.4.tar.gz#md5=9e78250000664a0be51966951d06cc17 --no-check-certificate
tar zxf rsa-3.4.tar.gz
cd rsa-3.4
/mydata/python2.7/bin/python setup.py install

echo "[install supervisord]"
cd /mydata/downloads/
wget https://github.com/Supervisor/supervisor/archive/3.0a10.tar.gz --no-check-certificate
tar zxvf 3.0a10.tar.gz
cd supervisor-3.0a10
/mydata/python2.7/bin/python setup.py install

#echo "[install ldap]"
#yum install openldap24-libs  openldap

# if [ ! -d "/mydata/downloads" ];then
# mkdir /mydata/downloads
# fi
# echo "[setup git]"
# cd /mydata/downloads/
# wget http://git-core.googlecode.com/files/git-1.8.1.1.tar.gz
# tar zxvf git-1.8.1.1.tar.gz
# cd git-1.8.1.1
# ./configure --prefix=/usr/local
# make
# make install


echo "make libmemcached"
cd /mydata/downloads/
wget https://launchpadlibrarian.net/91217116/libmemcached-1.0.4.tar.gz
tar zxf libmemcached-1.0.4.tar.gz
cd libmemcached-1.0.4
./configure 
make 
make install

export LD_LIBRARY_PATH=/usr/local/lib/:$LD_LIBRARY_PATH
sudo ldconfig
# /etc/ld.so.conf
# add /usr/local/lib/

echo "/usr/local/lib/" >> /etc/ld.so.conf
ldconfig /etc/ld.so.conf

echo "pylibmc"
cd /mydata/downloads/
wget https://pypi.python.org/packages/23/f4/3904b7171e61a83eafee0ed3b1b8efe4d3c6ddc05f7ebdff1831cf0e15f1/pylibmc-1.5.1.tar.gz#md5=9077704e34afc8b6c7b0b686ae9579de --no-check-certificate
tar zxf pylibmc-1.5.1.tar.gz
cd pylibmc-1.5.1
/mydata/python2.7/bin/python setup.py install

cd /mydata/downloads
echo '[start install libressl!]'
wget https://ftp.openbsd.org/pub/OpenBSD/LibreSSL/libressl-2.5.0.tar.gz --no-check-certificate
tar zxvf libressl-2.5.0.tar.gz
cd libressl-2.5.0
./config --prefix=/usr/local
make
make install



#用于网络优化 暂时瓶颈不在这里 且安装出现问题 暂不安装
echo "make libevent"
cd /mydata/downloads/
wget https://github.com/downloads/libevent/libevent/libevent-2.0.20-stable.tar.gz --no-check-certificate
tar zxf libevent-2.0.20-stable.tar.gz
cd libevent-2.0.20-stable
./configure
make
make install

