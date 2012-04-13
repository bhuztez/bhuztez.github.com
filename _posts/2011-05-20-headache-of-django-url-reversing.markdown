---
layout: post
title: Django反查URL的问题
published: false
lang: zh
---

主要是这几个问题：

1. 不知道`Django` URL的命名空间是怎么设计的，一旦设置了命名空间，就不知道该怎么反查了。
2. 直接用正则表达式来匹配，不利于表达式的重用。同时，反查URL只会匹配最后一级的参数（这也许是因为可以同时有普通的参数和命名参数，匹配多级会导致混淆）。
3. 不支持多个子域名
4. URL scheme的问题

看了下`werkzeug.routing`，第1个问题直接被忽略了，第2个问题用`Converter`解决了，第3个问题解决得还不错，第4个问题只解决了一小部分。这个问题本来不该成为问题的，目前支持`HTTP`协议的软件，几乎都不支持`startTLS`，导致HTTPS迟迟不能退休。
`werkzeug.routing`用`bind_to_environ`实现了对于通过HTTPS的请求，反查出来的URL始终是HTTPS的。对于任意一个匹配项，只支持HTTP或者HTTPS，只需要一次额外的重定向就可以解决了。如果有同时支持HTTP和HTTPS的，麻烦就大了。
