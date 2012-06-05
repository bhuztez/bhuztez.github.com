---
layout: post
title: 在本地测试DNSSEC配置
lang: zh
---


关于zone签名的基本操作可以参考这个[DNSSEC Tutorial](http://meetings.apnic.net/29/program/tutorials/dnssec)。需要注意的是，用`unbound`作为recursive resolver的时候，`do-not-query-localhost`要设置成`no`，不然就不会使用配置里面地址是本地的forwarder。因为authoritative server不会设置AD flag[^dnssec-ad-flag]，所以，一定要在本地运行一个recursive resolver。


为了让ssh的DNS查询都通过本地recursive resolver，使用LD_PRELOAD，覆盖掉socket相关函数。值得注意的是，在Fedora 16上，得覆盖connect而不是sendto。ssh设置

~~~~~~~~~~
VerifyHostKeyDNS yes
StrictHostKeyChecking ask
~~~~~~~~~~

这样DNS上有DNSSEC签名过的SSHFP记录，ssh第一次连上去的时候，就不需要输入yes来确认公钥了。

[^dnssec-ad-flag]: 参考[DNSSEC - Ad Flag not activated](http://serverfault.com/questions/179463/dnssec-ad-flag-not-activated)


