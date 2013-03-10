Title: 升级到Fedora 16
Date: 2012-05-03
Slug: upgrade-to-fedora-16


在虚拟机里用Fedora 15 DVD最小安装后，没有网络。把DVD挂载起来，从`Packages`目录里装上`dhclient`。修改`/etc/sysconfig/network-scripts/ifcfg-eth0`，把这三项改成下面这样。

```text
ONBOOT="yes"
BOOTPROTO="dhcp"
NM_CONTROLLED="no"
```

修改启动项

```console
$ chkconfig network on
```

启动网络

```console
$ service network start
```

尝试了很多次都没能从`grub2`引导改回`grub`引导，升级的时候，选择直接排除`grub2`和`grub-efi`。另外，有`yum-plugin-downloadonly`，这样就可以放心地让它在后台先下载了。

```console
$ yum --releasever=16 --disableplugin=presto -xgrub2 -xgrub-efi --downloadonly distro-sync
```

安装

```console
$ yum --releasever=16 --disableplugin=presto -xgrub2 -xgrub-efi distro-sync
```

重启之后，桌面进不去了。解决方法参考 <https://bugzilla.redhat.com/show_bug.cgi?id=751729#c9> 。

```console
$ restorecon -R ~/.local
```


进桌面之后，发现少了`gnome-contacts`

```console
$ yum install gnome-contacts
```


输入法也很纠结了。别的程序对的时候，Emacs悲剧了。Emacs对的时候，别的程序都悲剧了。最后发现是iBus变了。现在不用中文输入法的时候，切换到`xkb:layout:default:#0`，而不是直接`disable`掉。另外要注意的是，切换过去的时候，得`(ibus-disable-keymap)`一下，不然就没自动补全了。



