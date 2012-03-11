---
layout: post
title: 从硬盘用LiveCD安装Fedora 15
lang: zh
---

Fedora 15的安装DVD一如既往地[不支持从LVM分区硬盘安装](http://docs.fedoraproject.org/en-US/Fedora/15/html/Installation_Guide/s1-steps-hd-installs-x86.html)。无奈，只能试试LiveCD了。LiveCD和DVD不同的一点是，LiveCD复制出来必须放在分区的根目录。

~~~~~~~~~~
title Fedora 15 LiveCD
	root (hd0,0)
	kernel /vmlinuz0 root=live:/dev/mapper/VolGroup00-LogVol02 rootfstype=auto ro liveimg quiet rhgb
	initrd /initrd0.img
~~~~~~~~~~

进入直接就登录了，没机会在登录那里选语言。进去之后`系统设置`->`区域和语言`那里可以选`汉语（中国）`，注销再进去就能看见汉字了。这个时候运行安装程序也是中文的了。我的硬盘上`/home`是单独一个ext3分区，自定义文件系统结构的时候，不能给那个分区设置挂载点，不然在格式化其他分区之后就只能退出安装了。等到安装完了之后，再修改`/etc/fstab`，添加下面这行，把那个分区挂载起来，重启。

~~~~~~~~~~
/dev/mapper/VolGroup00-LogVol02 /home			ext3	defaults	1 2
~~~~~~~~~~

装完之后不知道从哪里设置ADSL，`Alt+F1` `nm-connection-editor` 回车，我就搞不懂了为什么系统设置里面设置网络那里不搞个按钮出来。不乱找还不知道这东西在哪里呢。登录后的菜单里面连关机都没有了。装上`gnome-shell-extensions-alternative-status-menu`，注销再进去之后就会出现了。桌面默认是空的，用`gnome-tweak-tool`可以把桌面调出来。桌面其实没啥用，空桌面才是好桌面。

把自己设置为管理员之后，用自己的密码就可以在`PackageKit`那里安装软件了。安装都很顺利，如果软件包的信息都能有翻译就好了。


