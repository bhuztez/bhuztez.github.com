---
layout: post
title: Python代码阅读基础
lang: zh
---

在阅读Python代码的时候，别忘了Python标准库里几个比较有用的库，`pdb`、`ast`和`code`。`pdb`用来调试，`ast`用来解析Python代码，`code`直接能给你一个[REPL](http://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop)。

比如，阅读`nova-api`的代码，并不关心URL Routing是怎么实现的，想知道的只是URL和相应处理代码的对应关系。把`nova-api`最后两行代码换成下面这两行。

{% highlight python %}
import code
code.interact(local=locals())
{% endhighlight %}

运行：

{% highlight pycon %}
Python 2.7.3rc2 (default, Apr 22 2012, 22:30:17) 
[GCC 4.6.3] on linux2
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> servers
[<nova.service.WSGIService object at 0x7f9cf662ff90>, <nova.service.WSGIService object at 0x2e90850>, <nova.service.WSGIService object at 0x33123d0>, <nova.service.WSGIService object at 0x4d3e390>]
>>> dir(servers[0])
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_get_manager', 'app', 'host', 'loader', 'manager', 'name', 'port', 'server', 'start', 'stop', 'wait']
>>> [ s.name for s in servers ]
['ec2', 'osapi_compute', 'osapi_volume', 'metadata']
>>> servers[1].app
{(None, ''): <nova.api.openstack.FaultWrapper object at 0x33b7a10>, (None, '/v1.1'): <nova.api.openstack.FaultWrapper object at 0x4d2e150>, (None, '/v2'): <nova.api.openstack.FaultWrapper object at 0x4866990>}
>>> dir(servers[1].app)
['__call__', '__cmp__', '__contains__', '__delitem__', '__doc__', '__getitem__', '__init__', '__iter__', '__len__', '__module__', '__repr__', '__setitem__', '_accept_strategy', '_content_type_strategy', '_match', '_munge_path', '_path_strategy', '_set_script_name', 'applications', 'clear', 'domain_url_re', 'get', 'has_key', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'norm_url_re', 'normalize_url', 'not_found_app', 'not_found_application', 'pop', 'popitem', 'setdefault', 'sort_apps', 'update', 'values']
>>> servers[1].app.applications
[((None, '/v1.1'), <nova.api.openstack.FaultWrapper object at 0x4d2e150>), ((None, '/v2'), <nova.api.openstack.FaultWrapper object at 0x4866990>), ((None, ''), <nova.api.openstack.FaultWrapper object at 0x33b7a10>)]
>>> dir(servers[1].app.applications)
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__delslice__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getslice__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__setslice__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
>>> dir(servers[1].app.applications[0][1])
['__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'application', 'factory', 'process_request', 'process_response']
>>> dir(servers[1].app.applications[0][1].application)
['__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_add_headers', '_build_user_headers', '_cache', '_cache_get', '_cache_put', '_cache_store_invalid', '_get_header', '_get_http_connection', '_get_user_token_from_header', '_header_to_env_var', '_iso8601', '_json_request', '_reject_request', '_remove_auth_headers', '_remove_headers', '_request_admin_token', '_validate_user_token', 'admin_password', 'admin_tenant_name', 'admin_token', 'admin_user', 'app', 'auth_host', 'auth_port', 'auth_uri', 'conf', 'delay_auth_decision', 'get_admin_token', 'http_client_class', 'token_cache_time']
>>> servers[1].app.applications[0][1].application
<keystone.middleware.auth_token.AuthProtocol object at 0x4d2e0d0>
>>> dir(servers[1].app.applications[0][1].application)
['__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_add_headers', '_build_user_headers', '_cache', '_cache_get', '_cache_put', '_cache_store_invalid', '_get_header', '_get_http_connection', '_get_user_token_from_header', '_header_to_env_var', '_iso8601', '_json_request', '_reject_request', '_remove_auth_headers', '_remove_headers', '_request_admin_token', '_validate_user_token', 'admin_password', 'admin_tenant_name', 'admin_token', 'admin_user', 'app', 'auth_host', 'auth_port', 'auth_uri', 'conf', 'delay_auth_decision', 'get_admin_token', 'http_client_class', 'token_cache_time']
>>> servers[1].app.applications[0][1].application.app
<nova.api.auth.NovaKeystoneContext object at 0x4990cd0>
>>> dir(servers[1].app.applications[0][1].application.app)
['__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'application', 'factory', 'process_request', 'process_response']
>>> servers[1].app.applications[0][1].application.app.application
<nova.api.openstack.compute.limits.RateLimitingMiddleware object at 0x4986b90>
>>> dir(servers[1].app.applications[0][1].application.app.application)
['__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_limiter', 'application', 'factory', 'process_request', 'process_response']
>>> servers[1].app.applications[0][1].application.app.application.application
<nova.api.openstack.compute.APIRouter object at 0x3508ed0>
>>> dir(servers[1].app.applications[0][1].application.app.application.application)
['ExtensionManager', '__call__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_dispatch', '_router', '_setup_ext_routes', '_setup_extensions', '_setup_routes', 'factory', 'map', 'resources']
>>> servers[1].app.applications[0][1].application.app.application.application.map
<nova.api.openstack.ProjectMapper object at 0x4866650>
>>> dir(servers[1].app.applications[0][1].application.app.application.application.map)
['__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_create_gens', '_create_regs', '_created_gens', '_created_regs', '_envdel', '_envget', '_envset', '_master_regexp', '_match', '_regprefix', '_routenames', 'always_scan', 'append_slash', 'collection', 'connect', 'controller_scan', 'create_regs', 'create_regs_lock', 'debug', 'decode_errors', 'directory', 'domain_match', 'encoding', 'environ', 'explicit', 'extend', 'generate', 'hardcode_names', 'match', 'matchlist', 'maxkeys', 'minimization', 'minkeys', 'prefix', 'redirect', 'req_data', 'resource', 'routematch', 'sub_domains', 'sub_domains_ignore', 'submapper', 'urlcache']
>>> route = servers[1].app.applications[0][1].application.app.application.application.map.matchlist[-1]
>>> route.name
'os-floating-ips'
>>> route.conditions
{'method': ['GET']}
>>> route._kargs
{'requirements': {'id': '[^\\/]+(?<!\\\\)'}, 'controller': <nova.api.openstack.wsgi.Resource object at 0x5093b50>, 'action': 'show'}
>>> route._kargs['controller']
<nova.api.openstack.wsgi.Resource object at 0x5093b50>
>>> route._kargs['controller'].__class__
<class 'nova.api.openstack.wsgi.Resource'>
>>> route._kargs['controller'].controller
<nova.api.openstack.compute.contrib.floating_ips.FloatingIPController object at 0x4d07d50>
>>> route._kargs['controller'].controller.show.__doc__
'Return data about the given floating ip.'
{% endhighlight %}


