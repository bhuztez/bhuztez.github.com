---
layout: post
title: 神奇的JavaScript
lang: zh
---


在Google上搜索"JavaScript sucks"，很多关于这个话题的链接都在2008年或者更早，搜索"JavaScript rocks -ebook"几乎是刚好相反。如果Google没有骗我，那几乎是一夜之间，JavaScript就变得优雅了，天生适合这适合那了。

而JavaScript本身在这段时间并没有发生显著的变化，特别是ECMAScript 4提案被简单地否定掉了。除了Firefox，其他浏览器都有了充分的理由不去支持ECMAScript 4提案中哪怕是很有用的特性。随后出现了基于V8的node.js。没有语言级的支持，`yield`，`import`之类的又被重新发明了很多遍。

事实上，在不预设场景的情况下，找不到任何理由选择node.js。如果只是因为只会JavaScript，所以就选node.js。首先，JavaScript和Python并没有多大差别。其次，用了node.js，你最后不得不去写一些C++，因为很不幸，node.js有太多部分是用C++写的。且不说很多发行版都没有打包node.js，为了部署node.js写的应用，你不得不看点Python，因为node.js的`configure`其实只是去调用了一下Python脚本。

同样的代码在Python里是Twisted的，不可能一到JavaScript里就优雅了。用Twisted处理不了的，不可能一换成node.js就能处理了。所以，要写点什么凑合着能用的，那就直接选Twisted，如果真的想学点什么，还是去看Erlang。


