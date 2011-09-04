---
layout: post
title: 调整 Gnome Shell
---


Fedora 15带来了Gnome Shell。尽管是非典型地用LiveCD硬盘安装了Fedora 15，也没碰到什么问题，能顺利进入桌面。刚开始的时候先是被菜单里消失了的关机吓到了。不久又发现，应用程序搜索结果里按``Ctrl-Enter``竟然和Ctrl加鼠标左键不一样。幸好，这些都是用JavaScript写的，没什么好怕的，还看得懂的嘛，Clutter和Gtk也没相差太多，就先看看代码再说吧。

看代码的时候才发现，那些扩展就没那么省心了。``windowsNavigator``，你说你至于么，只是切换窗口，你把整个区域的键盘事件都吃掉了。你让我怎么实现``Ctrl-Enter``弹出新窗口的功能啊。这里就不提按``Ctrl-3``还切换不到第三个工作区了。只能把你在``~/.local/share/gnome-shell/extensions``里覆盖了。

还没完啊，一用``user-theme``啊，之前载入的扩展的样式表都被无视了啊，用``themeselector``换个主题，所有扩展的样式表都被抛弃了啊。最后，Bugzilla里竟然说是Gnome Shell的问题，会在3.2里修复。那我现在怎么办，那也只能先覆盖你们了。

还有要注意，如果开了``native-window-placement``，必须在``windowsNavigator``之前载入才行。不然``windowsNavigator``就傻掉了。如果你像我一样在自己的目录里覆盖了``windowsNavigator``的话，你只能多试几次运气，希望多次符号链接->删除->符号链接这两个家伙之后，会碰到正确的载入顺序，那时候就请他们站住别动就好了。

好了，窗口切换符合预期了，主题也换了。先让自己慢慢变成键盘控吧。
