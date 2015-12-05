#  _    _          ___           __ _     (R)
# | |  (_)_ _____ / __|___ _ _  / _(_)__ _
# | |__| \ V / -_) (__/ _ \ ' \|  _| / _` |
# |____|_|\_/\___|\___\___/_||_|_| |_\__, |
#                                    |___/
# Copyright (c) 2009-2015 Keppler IT GmbH.
# ----------------------------------------------------------------------------
# $Id: liveconfig-meta.spec 19 2012-09-13 10:40:06Z kk $
# 
# centos7/liveconfig-meta.spec
# spec file for building RPM package
# ----------------------------------------------------------------------------

# Firewall documentation:
# https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Security_Guide/sec-Using_Firewalls.html

%define _rpmdir %(echo $PWD)/centos7

%define version    0.4.1
%define release	   1.el7

Name:		liveconfig-meta
Summary:	Metapackage for full-featured web server
Version:	%{version}
Release:	%{release}
Group:		Networking/Admin
URL:		http://www.liveconfig.com
Vendor:		Keppler IT GmbH
License:	Commercial
# Source:	liveconfig-%{version}.tar.gz
BuildRoot:	%(echo $PWD)/centos7/pkgroot
Buildarch:	noarch
Packager:	LiveConfig Package Admin <pkgadmin@liveconfig.com>
Requires:	quota bzip2 unzip
Requires:	httpd mod_ssl
Requires:	php php-cli php-gd php-mysql php-pear php-pdo php-soap php-xml php-xmlrpc
Requires:	postfix dovecot dovecot-pigeonhole spamassassin
Requires:	mariadb mariadb-server
Requires:	vsftpd libdb-utils

%description
This metapackage installs all packages required for a full-featured web server (web, mail, ftp, database, ...)

#%install
	
%post
# enable Apache httpd
/bin/systemctl enable httpd.service
/bin/systemctl start httpd.service

# patch [client] section in MariaDB config:
if ! grep -q '^socket=' /etc/my.cnf.d/client.cnf; then
	sed -i -e 's/^\(\[client\]\)/\1\nsocket=\/var\/lib\/mysql\/mysql.sock/i' \
	       /etc/my.cnf.d/client.cnf
fi

# enable MariaDB server
/bin/systemctl enable mariadb.service
/bin/systemctl start mariadb.service

# enable vsftpd
/bin/systemctl enable vsftpd.service
/bin/systemctl start vsftpd.service

# enable SpamAssassin
/bin/systemctl enable spamassassin.service
/bin/systemctl start spamassassin.service

if [ "$1" = "1" ]; then
	# initial installation of this package
	echo " _    _          ___           __ _     (R)"
	echo "| |  (_)_ _____ / __|___ _ _  / _(_)__ _"
	echo "| |__| \\ V / -_) (__/ _ \\ ' \\|  _| / _\` |"
	echo "|____|_|\\_/\\___|\\___\\___/_||_|_| |_\\__, |__________________________________"
	echo "                                   |___/"
	echo " IMPORTANT:"
	echo " - please run "mysql_secure_installation" to clean up unnecessary test"
	echo "   accounts and to set a MySQL root password"
	if [ ! -f "/etc/mail/clamav-milter.conf" ]; then
		echo " - you may want to install ClamAV-Milter to scan e-mails for"
		echo "   viruses and malware. See the installation instructions at"
		echo "   http://www.liveconfig.com/en/kb/23"
	fi
	echo " - if you have SELinux enabled (or plan to do so), you need to adjust some"
	echo "   permissions:"
	echo "     /usr/sbin/setsebool -P httpd_enable_homedirs=1"
	echo "     /usr/sbin/setsebool -P ftp_home_dir=1"
	echo " - if you're using the CentOS firewall, you may want to enable HTTP and"
	echo "   HTTPS access to your server:"
	echo "     firewall-cmd --zone=public --add-service=http --permanent"
	echo "     firewall-cmd --zone=public --add-service=https --permanent"
	echo "     firewall-cmd --reload"
	echo "___________________________________________________________________________"
	echo ""
fi

%files

# <EOF>-----------------------------------------------------------------------
