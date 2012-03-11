---
layout: post
title: 解码支付宝三月八日密文
lang: zh
---


支付宝在三月八日[贴了段密文出来让大家猜](http://weibo.com/1627897870/y8UFSzJwC)：

> 密文：
>
>     NRFHFLOGTBIHURDAFCKTFONJTNGFMESQSLBQEQJILGJRNNBOUSDRGXJRIQQRJZQURVSYRLRDOFVBFKKKFFGXDNYXLWPNFPGDIDBOGXHDNBMDSQSAKPXJHSBWYXLWWCZHJBIEHKXXYZRTPITVDOGJILLRUMCVULWZMQDSRALFRPNIZIBMOUSCKPWBELJGZOLOOZXJMAANELTFYLOSZFGKYDLKJGRPDVNWULPEOKTKFDPGNYCJPENIPQBOFDZRBOHTSHZMOMYANWSAMKLRAGTROJEXNZTAIAJRDSDNHQVMMXDZMPTUTOMLOSNGSLOPGTYUJJNSEHQJGSODKYPAH
>{: style="word-wrap: break-word; white-space: pre-wrap; margin: 0 2em"}
> 
> 提示：
>
> 1. 这是按二战时期一种知名商业密码机的原理加密后的密文，提示：
>
>        AZ BY, A, L, I
>
> 2. 也许这张映射表在破解的时候用的到。
>
>        {34=65, 32=66, 33=67, 40=68, 41=69, 46=70, 44=71, 93=72, 59=73, 126=74, 125=75, 124=76, 123=78, 63=77, 62=79, 61=81, 91=80, 60=82}
>    {: style="word-wrap: break-word; white-space: pre-wrap;"}


很明显，可以搜到答案的，肯定已经有人把结果贴出来了。那就立即搜索`支付宝 解密 "AZ BY"`(比如：[Google](https://encrypted.google.com/search?q=%E6%94%AF%E4%BB%98%E5%AE%9D+%E8%A7%A3%E5%AF%86+%22AZ+BY%22)，[百度](http://www.baidu.com/s?wd=%E6%94%AF%E4%BB%98%E5%AE%9D+%E8%A7%A3%E5%AF%86+%22AZ+BY%22)<s markdown="span">，[搜搜](http://www.soso.com/q?w=%E6%94%AF%E4%BB%98%E5%AE%9D+%E8%A7%A3%E5%AF%86+%22AZ+BY%22)，[搜狗](http://www.sogou.com/web?query=%E6%94%AF%E4%BB%98%E5%AE%9D+%E8%A7%A3%E5%AF%86+%22AZ+BY%22)，[中国雅虎](http://www.yahoo.cn/s?q=%E6%94%AF%E4%BB%98%E5%AE%9D+%E8%A7%A3%E5%AF%86+%22AZ+BY%22), [即刻](http://www.jike.com/so?q=%E6%94%AF%E4%BB%98%E5%AE%9D+%E8%A7%A3%E5%AF%86+%22AZ+BY%22)，[有道](http://www.youdao.com/search?q=%E6%94%AF%E4%BB%98%E5%AE%9D+%E8%A7%A3%E5%AF%86+%22AZ+BY%22), [必应](http://cn.bing.com/search?q=%E6%94%AF%E4%BB%98%E5%AE%9D+%E8%A7%A3%E5%AF%86+%22AZ+BY%22)</s>[^order-1])。注意到很前面就有一条“[破解三八妇女节 支付宝MM发出的邀请卡 - 死理性派小组 - 果壳网](http://www.guokr.com/post/111242/)”，里面提到：

> `AZ BY`指的是线路连接板的接线是`A`接`Z` `B`接`Y`；......`ALI`正是三个转轮的初始位置，也就是密钥。......我用的是**Enigma**的模拟软件

现在就去搜索`Enigma Simulator`(比如：[Google](https://encrypted.google.com/search?q=Enigma+Simulator)，[百度](http://www.baidu.com/s?wd=Enigma+Simulator)，[必应](http://cn.bing.com/search?q=Enigma+Simulator)，[Yahoo](http://search.yahoo.com/search?p=Enigma+Simulator)，[搜搜](http://www.soso.com/q?w=Enigma+Simulator)<s markdown="span">，[有道](http://www.youdao.com/search?q=Enigma+Simulator)，[搜狗](http://www.sogou.com/web?query=Enigma+Simulator)，[即刻](http://www.jike.com/so?q=Enigma+Simulator)，[中国雅虎](http://www.yahoo.cn/s?q=Enigma+Simulator)</s>[^order-2])。对了，就是[这个](http://users.telenet.be/d.rijmenants/en/enigmasim.htm)。但这操作也实在太麻烦了。幸好，在Google搜索结果第一页倒数第二个的位置，有[一个用JavaScript写的](http://startpad.googlecode.com/hg/labs/js/enigma/enigma-sim.html)。

可是又该怎么解码呢？先看看维基百科的[Enigma machine](http://en.wikipedia.org/wiki/Enigma_machine)词条。查找`decrypt`，全部高亮显示。

> The reflector ensured that Enigma is [self-reciprocal](http://en.wikipedia.org/wiki/Involution_(mathematics)): conveniently, __encryption was the same as decryption__. 
> {: style="line-height: 125%; letter-spacing: 0px; word-spacing: 0px;"}

好了，打开那个[用JavaScript写的](http://startpad.googlecode.com/hg/labs/js/enigma/enigma-sim.html)，`Rotor Start`填`ALI`，`Plugboard`填`AX BY`，在`Type Message Here`下面填上密文，就完了。如果你不看见代码就不死心的话，那这个[Gist](https://gist.github.com/2016510)就是为你而存在的。

现在是下结论的时候了。原以为其他几个搜索引擎不至于这么烂的，万万没有想到的是，那几个号称要挑战百度的搜索引擎，还远远不配做百度的对手。只要愿意，百度就是可以继续恶心下去。


[^order-1]: 以2012年3月11日查询结果为准。有删除线表示没在第一页看到答案。没删除线的，以第一页相关内容比例排序，有删除线的以大致结果数排序。
[^order-2]: 以2012年3月11日查询结果为准。有删除线表示没在第一页看到果壳网那帖里提到的模拟器。没删除线的，以模拟器地址在第一页的出现位置排序。有删除线的，以[Terry Long](http://www.terrylong.org/)写的Enigma模拟器在第一页出现的位置排序，没有的排在最后。


