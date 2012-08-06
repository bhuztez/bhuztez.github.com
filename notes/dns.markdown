---
layout: note
title: DNS
lang: zh
---

### 运行一个临时的DNS Server

在配置文件里把文件/目录地址改到当前目录下。BIND 9.7多了一个`session-keyfile`[^bind97-session-key]。

[^bind97-session-key]: [New Features in BIND 9.7](http://www.isc.org/software/bind/new-features/9.7)

{% highlight bash %}
#!/usr/bin/env bash

ROOT="$(pwd)"

mkdir -p "${ROOT}/keys"
mkdir -p "${ROOT}/zones"

if [[ ! -e "named.conf" ]]; then

cat >"named.conf" << EOF
options {
        listen-on               port 8053       { 127.0.0.1; };
        directory               "${ROOT}/zones";
        pid-file                "${ROOT}/named.pid";
        session-keyfile         "${ROOT}/session.key";

        allow-query             { 127.0.0.1; };
        recursion               no;

        managed-keys-directory  "${ROOT}/keys";
};

controls {};
EOF

fi

named -c named.conf -g
{% endhighlight %}


### 添加一个zone

修改`named.conf`，添加一个zone。

{% highlight text %}
zone "example.com." {
        type    master;
        file    "example.com";
};
{% endhighlight %}

在`zones`目录下，新建`example.com`文件

{% highlight text %}
$ORIGIN .
$TTL 300
example.com		IN SOA	example.com. root.example.com. (
				201208061  ; serial
				300        ; refresh
				300        ; retry
				300        ; expire
				300        ; minimum
				)
			NS	ns.example.com.
			A	127.0.0.1
ns.example.com.		A	127.0.0.1
{% endhighlight %}

使用`dig`来查询

{% highlight console %}
$ dig -p 8053 @127.0.0.1 example.com

; <<>> DiG 9.8.2-RedHat-9.8.2-1.fc16 <<>> -p 8053 @127.0.0.1 example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 2269
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            300     IN      A       127.0.0.1

;; AUTHORITY SECTION:
example.com.            300     IN      NS      ns.example.com.

;; ADDITIONAL SECTION:
ns.example.com.         300     IN      A       127.0.0.1

;; Query time: 1 msec
;; SERVER: 127.0.0.1#8053(127.0.0.1)
;; WHEN: Mon Aug  6 16:35:14 2012
;; MSG SIZE  rcvd: 78
{% endhighlight %}


### 修改DNS记录

修改`zone`的设置，添加`allow-update`。因为BIND 9.7开始，BIND启动的时候会临时生成一个可以用来update的key。就先用这个key来操作好了。

{% highlight text %}
zone "example.com." {
        type    master;
        file    "example.com";

        allow-update {
                key local-ddns;
        };
};
{% endhighlight %}

用`nsupdate`添加一条记录

{% highlight console %}
$ nsupdate -k session.key
> server localhost 8053
> update add www.example.com. 300 A 127.0.0.1
> send
> quit
$
{% endhighlight %}

用`dig`查询结果

{% highlight console %}
$ dig -p 8053 @127.0.0.1 www.example.com

; <<>> DiG 9.8.2-RedHat-9.8.2-1.fc16 <<>> -p 8053 @127.0.0.1 www.example.com
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 40774
;; flags: qr aa rd; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; QUESTION SECTION:
;www.example.com.               IN      A

;; ANSWER SECTION:
www.example.com.        300     IN      A       127.0.0.1

;; AUTHORITY SECTION:
example.com.            300     IN      NS      ns.example.com.

;; ADDITIONAL SECTION:
ns.example.com.         300     IN      A       127.0.0.1

;; Query time: 2 msec
;; SERVER: 127.0.0.1#8053(127.0.0.1)
;; WHEN: Mon Aug  6 16:47:02 2012
;; MSG SIZE  rcvd: 82
{% endhighlight %}


删除一条记录可以用

{% highlight text %}
update delete www.example.com. 300 A 127.0.0.1
{% endhighlight %}

要一次删除`www.example.com.`所有A记录，用

{% highlight text %}
update delete www.example.com. A
{% endhighlight %}

生成修改记录用的key

{% highlight console %}
$ dnssec-keygen -T KEY -a HMAC-SHA512 -b 512 -n USER user
Kuser.+165+40835
$ cat Kuser.+165+40835.key 
user. IN KEY 0 3 165 C25Jqxj2ZY8m18yaANh9FpvKhHPXksoOtlOH8XemcV4YB4JSfmbqEmbf lpZIBgeTHqPkMNv08jbyluawecL5yA==
$ cat Kuser.+165+40835.private 
Private-key-format: v1.3
Algorithm: 165 (HMAC_SHA512)
Key: C25Jqxj2ZY8m18yaANh9FpvKhHPXksoOtlOH8XemcV4YB4JSfmbqEmbflpZIBgeTHqPkMNv08jbyluawecL5yA==
Bits: AAA=
Created: 20120807063255
Publish: 20120807063255
Activate: 20120807063255
{% endhighlight %}

修改`named.conf`

{% highlight text %}
key "user." {
        algorithm       HMAC-SHA512;
        secret          "C25Jqxj2ZY8m18yaANh9FpvKhHPXksoOtlOH8XemcV4YB4JSfmbqEmbflpZIBgeTHqPkMNv08jbyluawecL5yA==";
};

zone "example.com." {
        type    master;
        file    "example.com";

        allow-update {
                key user.;
        };
};
{% endhighlight %}

此时用`nsupdate -k Kuser.+165+40835.private`就可以修改DNS记录了

#### Python

可以用[dnspython](http://www.dnspython.org/)来修改DNS记录

{% highlight python %}
import dns.query
import dns.tsig
import dns.tsigkeyring
import dns.update
import dns.rdatatype

keyring = dns.tsigkeyring.from_text({
    'user.': "C25Jqxj2ZY8m18yaANh9FpvKhHPXksoOtlOH8XemcV4YB4JSfmbqEmbflpZIBgeTHqPkMNv08jbyluawecL5yA=="
})

update = dns.update.Update(
    'example.com.', 
    keyring=keyring,
    keyalgorithm=dns.tsig.HMAC_SHA512)

update.add('www', 300, dns.rdatatype.A, '127.0.0.1')

response = dns.query.tcp(update, '127.0.0.1', port=8053)
print response
{% endhighlight %}

运行

{% highlight console %}
$ python dnsupdate.py
id 49584
opcode UPDATE
rcode NOERROR
flags QR
;ZONE
example.com. IN SOA
;PREREQ
;UPDATE
;ADDITIONAL
{% endhighlight %}


#### Java

可以用[dnsjava](http://www.dnsjava.org/)来修改DNS记录

{% highlight java %}
import org.xbill.DNS.*;

class DNSUpdate {
    public static void main(String args[]) throws org.xbill.DNS.TextParseException, java.io.IOException {
        Name zone = Name.fromString("example.com.");
        Update update = new Update(zone);
        Name host = Name.fromString("www", zone);
        TSIG key = new TSIG(
            TSIG.HMAC_SHA512,
            "user.",
            "C25Jqxj2ZY8m18yaANh9FpvKhHPXksoOtlOH8XemcV4YB4JSfmbqEmbflpZIBgeTHqPkMNv08jbyluawecL5yA==");

        update.add(host, Type.A, 300, "127.0.0.1");

        Resolver resolver = new SimpleResolver("127.0.0.1");
        resolver.setTCP(true);
        resolver.setPort(8053);
        resolver.setTSIGKey(key);
        
        Message response = resolver.send(update);

        System.out.println(response);
    }
};
{% endhighlight %}

编译运行

{% highlight console %}
$ javac -cp dnsjava-2.1.3.jar DNSUpdate.java
$ java -cp .:dnsjava-2.1.3.jar DNSUpdate
;; ->>HEADER<<- opcode: UPDATE, status: NOERROR, id: 54821
;; flags: qr ; qd: 1 an: 0 au: 0 ad: 1
;; TSIG ok
;; ZONE:
;;      example.com., type = SOA, class = IN

;; PREREQUISITES:

;; UPDATE RECORDS:

;; ADDITIONAL RECORDS:
user.                   0       ANY     TSIG    hmac-sha512. 1344326060 300 64 YmqR2FI00zkP+K8oikeip7QM+QSZgAJg/b+vCCFi18AFFarRdOrkNSRNouPMGec9qUko0Gf6AywU2W7YXsKUtA== NOERROR 0

;; Message size: 138 bytes
{% endhighlight %}






