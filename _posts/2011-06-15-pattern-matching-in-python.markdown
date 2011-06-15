---
layout: post
title: Pattern Matching in Python
---


In Python, operators could be overloaded with special methods. 
However ugly it is, pattern matching is possible in this way.


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


Moreover, with a little trick, we can do pattern matching in function 
definitions.

{% highlight python %}
>>> @match
... def qsort(l=[]):
...     return []
... 
>>> @match
... def qsort(l):
...     p, r = l[0], l[1:]
...     return qsort([i for i in r if i<p])+[p]+qsort([i for i in r if i>p])
... 
>>> qsort(list(reversed(range(10))))
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
{% endhighlight %}


To play the trick, we [inspect](http://docs.python.org/library/inspect.html)
the arguments of a function, wrap it up, and check arguments against their
default values before actually call the function.


{% highlight python %}
from functools import wraps
from inspect import getargspec

def get_pattern_wrapper(func):
    fn_args, fn_varargs, fn_keywords, fn_defaults = getargspec(func)
    fn_defaults = fn_defaults or ()
    pattern_args = len(fn_args) - len(fn_defaults)
    pattern_keywords = dict(zip(fn_args[-len(fn_defaults):], fn_defaults))

    @wraps(func)
    def wrapper(*args, **kwargs):
        count = 0
        if fn_defaults:
            for i, arg in enumerate(args[pattern_args:]):
                if fn_defaults[i] != arg:
                    raise TypeError
                count += 1

        for key, value in pattern_keywords.items():
            if key in kwargs:
                if value != kwargs[key]:
                    raise TypeError
                count += 1

        if count < len(fn_defaults):
            raise TypeError

        return func(*args, **kwargs)

    return wrapper
{% endhighlight %}


A dispatcher holds a list of wrapped functions, calls them one by one until one 
of them matches.


{% highlight python %}
import sys

class PatternDispatcher(list):

    def __init__(self, name):
        self.__name__ = name


    def __call__(self, *args, **kwargs):
        for func in self:
            try:
                return func(*args, **kwargs)
            except TypeError:
                exc_type, value, tb = sys.exc_info()
                if tb.tb_next.tb_next:
                    raise

        raise TypeError('%s(): no matching pattern'%(self.__name__))


    def __get__(self, instance, owner):
        if instance is None:
            return self
        return lambda *args, **kwargs: self(instance, *args, **kwargs)


    def match(self, func):
        self.append(get_pattern_wrapper(func))
        return self

{% endhighlight %}


The decorator will try to find in the local symbol table of where it is called
from, if any dispatcher has the same name as the passed-in function, append it 
to the list of functions which the dispatcher holds, and return the dispatcher.


{% highlight python %}
from inspect import currentframe

def match(func):
    frame = currentframe()
    try:
        dispatcher = frame.f_back.f_locals.get(
            func.__name__,
            PatternDispatcher(func.__name__))
    finally:
        del frame

    assert isinstance(dispatcher, PatternDispatcher)
    dispatcher.append(get_pattern_wrapper(func))
    return dispatcher
{% endhighlight %}




