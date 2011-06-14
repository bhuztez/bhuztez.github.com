---
layout: post
title: Pattern Matching in Python
published: false
---



{% highlight python %}
>>> class MatchType(object):
...     def __init__(self, type):
...         self.type = type
...     def __eq__(self, other):
...         return isinstance(other, self.type)
...     def __ne__(self, other):
...         return not self.__eq__(other)
... 
>>> MatchType(int) == 1
True
>>> MatchType(int) == 'abc'
False
>>> 1 == MatchType(int)
True
>>> 'abc' == MatchType(int)
False
{% endhighlight %}




