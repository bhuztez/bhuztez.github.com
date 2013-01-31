---
layout: link
title: 沙盒
lang: zh
---

[Tutorial: Function Interposition in Linux](http://www.jayconrod.com/cgi/view_post.py?23)

[rtld-audit - auditing API for the dynamic linker](http://www.kernel.org/doc/man-pages/online/pages/man7/rtld-audit.7.html)


## 打包

Fedora用的mock虽然能用，但很成问题，有执行mock权限的用户就相当于是root了。

[Mock](https://fedoraproject.org/wiki/Projects/Mock)

Debian可以在fakechroot里用debootstrap。在Fedora下没成功用起来过。

[Debootstrap and fakechroot](http://g0dilstuff.a.wiki-site.com/index.php/Debootstrap_and_fakechroot)

另外找到一个叫pseudo的工具不知道能不能用。

[pseudo: A utility for emulating root privileges](https://github.com/wrpseudo/pseudo)


## 运行不信任的代码

尽管有很多其他方法。在限制上，但都比不上SECCOMP。SECCOMP只允许四个syscall。

[seccomp-nurse: secure sandbox on Linux](http://chdir.org/~nico/seccomp-nurse/)

可以尝试自己实现exec

[Announcing Userland Exec](http://marc.info/?l=bugtraq&m=107298764827122&w=2)

[Modern Userland Exec](http://www.stratigery.com/userlandexec.html)

也可以尝试实现自己的GCC Plugin

[GCC Internals: Plugins](http://gcc.gnu.org/onlinedocs/gccint/Plugins.html)

[An introduction to creating GCC plugins](http://lwn.net/Articles/457543/)

[Parsing C++ with GCC plugins, Part 1](http://www.codesynthesis.com/~boris/blog/2010/05/03/parsing-cxx-with-gcc-plugin-part-1/)

[GCC Python Plugin](https://gcc-python-plugin.readthedocs.org/en/latest/index.html)

[GCC MELT](http://gcc-melt.org/)







