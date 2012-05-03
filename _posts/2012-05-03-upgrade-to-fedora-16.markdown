---
layout: post
title: 升级到Fedora 16
lang: zh
---


在虚拟机里用Fedora 15 DVD最小安装后，没有网络。把DVD挂载起来，从`Packages`目录里装上`dhclient`。修改`/etc/sysconfig/network-scripts/ifcfg-eth0`，把这三项改成下面这样。

~~~~~~~~~~
ONBOOT="yes"
BOOTPROTO="dhcp"
NM_CONTROLLED="no"
~~~~~~~~~~

修改启动项

~~~~~~~~~~
chkconfig network on
~~~~~~~~~~

启动网络

~~~~~~~~~~
service network start
~~~~~~~~~~

尝试了很多次都没能从`grub2`引导改回`grub`引导，升级的时候，选择直接排除`grub2`和`grub-efi`。另外，有`yum-plugin-downloadonly`，这样就可以放心地让它在后台先下载了。

~~~~~~~~~~
yum --releasever=16 --disableplugin=presto -xgrub2 -xgrub-efi --downloadonly distro-sync
~~~~~~~~~~

安装

~~~~~~~~~~
yum --releasever=16 --disableplugin=presto -xgrub2 -xgrub-efi distro-sync
~~~~~~~~~~

重启之后，发现少了`gnome-contacts`

~~~~~~~~~~
yum install gnome-contacts
~~~~~~~~~~


输入法也很纠结了。别的程序对的时候，Emacs悲剧了。Emacs对的时候，别的程序都悲剧了。




