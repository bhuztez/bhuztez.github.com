---
layout: note
title: DNS基本配置
lang: zh
---

## 运行一个临时的DNS Server

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
        managed-keys-directory  "${ROOT}/keys";

        allow-query             { 127.0.0.1; };
        recursion               no;
};

controls {};
EOF

fi

named -c named.conf -g
{% endhighlight %}


## 添加一个zone

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


## 修改DNS记录

修改`zone`的设置，添加`allow-update`。因为BIND 9.7开始，BIND启动的时候会临时生成一个可以用来update的key。就先用这个key来操作好了。

{% highlight text %}
zone "example.com." {
        type            master;
        file            "example.com";

        allow-update    { key local-ddns; };
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
        type            master;
        file            "example.com";

        allow-update    { key user.; };
};
{% endhighlight %}

此时用`nsupdate -k Kuser.+165+40835.private`就可以修改DNS记录了

### Python

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


### Java

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


## Master/Slave

修改zone的设置，添加`allow-transfer`和`also-notify`。

{% highlight text %}
zone "example.com." {
        type            master;
        file            "example.com";

        allow-update    { key local-ddns; };
        allow-transfer  { 127.0.0.1; };
        also-notify     { 127.0.0.1 port 8153; };
};
{% endhighlight %}

slave的配置，只要把zone的`masters`设置好就可以了。

{% highlight bash %}
#!/usr/bin/env bash

ROOT="$(pwd)"

mkdir -p "${ROOT}/slave-keys"
mkdir -p "${ROOT}/slave-zones"

if [[ ! -e "slave.conf" ]]; then

cat >"slave.conf" << EOF
options {
        listen-on               port 8153       { 127.0.0.1; };
        directory               "${ROOT}/slave-zones";
        pid-file                "${ROOT}/slave.pid";        
        session-keyfile         "${ROOT}/slave.session.key";
        managed-keys-directory  "${ROOT}/slave-keys";        

        allow-query             { 127.0.0.1; };
        recursion               no;
};

controls {};

zone "example.com." {
        type    slave;
        masters { 127.0.0.1 port 8053; };
};
EOF

fi

named -c slave.conf -g
{% endhighlight %}


## DNSSEC

在zones目录下，生成ZSK

{% highlight console %}
$ dnssec-keygen -a rsasha512 -b 1024 -n ZONE example.com.
Generating key pair......................++++++ ...............++++++ 
Kexample.com.+010+41861
{% endhighlight %}

生成KSK

{% highlight console %}
$ dnssec-keygen -a rsasha512 -b 1024 -n ZONE -f KSK example.com.
Generating key pair.........................++++++ .....................................++++++ 
Kexample.com.+010+49764
{% endhighlight %}


修改`example.com`，在最后添加两行

{% highlight text %}
$INCLUDE "Kexample.com.+010+41861.key"
$INCLUDE "Kexample.com.+010+49764.key"
{% endhighlight %}

签名zone

{% highlight console %}
$ dnssec-signzone example.com
Verifying the zone using the following algorithms: RSASHA512.
Zone signing complete:
Algorithm: RSASHA512: KSKs: 1 active, 0 stand-by, 0 revoked
                      ZSKs: 1 active, 0 stand-by, 0 revoked
example.com.signed
{% endhighlight %}


修改`named.conf`

{% highlight text %}
zone "example.com." {
        type            master;
        file            "example.com.signed";
};
{% endhighlight %}

在options加上

{% highlight text %}
        dnssec-enable           yes;
{% endhighlight %}

启动bind，查看DNSKEY

{% highlight console %}
$ dig -p 8053 @localhost  +multi +noall +answer DNSKEY example.com.
example.com.            300 IN DNSKEY 256 3 10 (
                                AwEAAbexLhdu6Fk91XVCZlXPuJUD4BfigFUFhEkijwrF
                                CF6KCAuixIt4tob2l4yTw/txAbGuzNz5t4oI/GUifniJ
                                oQO5WLn18YnhPtQ/TLgyDfTB01IAqK1AMNJ4bHINEn4V
                                gh3q4V41xgh8GMdYN5LsD5qUKUpoy8hMLRSGSK6VVr6v
                                ) ; key id = 41861
example.com.            300 IN DNSKEY 257 3 10 (
                                AwEAAboBxp1wNbmxhINtxORCNfwQQaZ3QlTtlxfV+jCR
                                Y5R44ri1ygI5kZEToqiB7W6nnxbUi9T5HRGmJmprl7Qa
                                pEzw4S8YaUXCdYAPy8tNFHMSsrj2d72r2gR2DSBp4C5Z
                                D5XGdk9kV6GSbCl0DMd0nzabSLMVw/A8N7l9cVU+MVez
                                ) ; key id = 49764
{% endhighlight %}

建立`trusted-key.key`文件

{% highlight text %}
example.com.            300 IN DNSKEY 257 3 10 AwEAAboBxp1wNbmxhINtxORCNfwQQaZ3QlTtlxfV+jCRY5R44ri1ygI5kZEToqiB7W6nnxbUi9T5HRGmJmprl7QapEzw4S8YaUXCdYAPy8tNFHMSsrj2d72r2gR2DSBp4C5ZD5XGdk9kV6GSbCl0DMd0nzabSLMVw/A8N7l9cVU+MVez
{% endhighlight %}

用`dig`来验证

{% highlight console %}
$ dig -p 8053 @localhost A example.com. +sigchase +trusted-key=trusted-key.key
;; RRset to chase:
example.com.            300     IN      A       127.0.0.1


;; RRSIG of the RRset to chase:
example.com.            300     IN      RRSIG   A 10 2 300 20120909052125 20120810052125 41861 example.com. A5raSwawZlfWejUvvWG+DYTiAMhbWyTXyScEYNxJxSyOrzZGLD4gGlFI RGmt91nmyw2+f2sHHqlRtvEmcxzFydTwZJs0lTdkQ3PODov4btEah52N aJGADObHaIAqZYcvYPlIpDDcZNIDQxbJbQyI6+JmWoFJN4QwyqXLn9dr LTU=



Launch a query to find a RRset of type DNSKEY for zone: example.com.

;; DNSKEYset that signs the RRset to chase:
example.com.            300     IN      DNSKEY  256 3 10 AwEAAbexLhdu6Fk91XVCZlXPuJUD4BfigFUFhEkijwrFCF6KCAuixIt4 tob2l4yTw/txAbGuzNz5t4oI/GUifniJoQO5WLn18YnhPtQ/TLgyDfTB 01IAqK1AMNJ4bHINEn4Vgh3q4V41xgh8GMdYN5LsD5qUKUpoy8hMLRSG SK6VVr6v
example.com.            300     IN      DNSKEY  257 3 10 AwEAAboBxp1wNbmxhINtxORCNfwQQaZ3QlTtlxfV+jCRY5R44ri1ygI5 kZEToqiB7W6nnxbUi9T5HRGmJmprl7QapEzw4S8YaUXCdYAPy8tNFHMS srj2d72r2gR2DSBp4C5ZD5XGdk9kV6GSbCl0DMd0nzabSLMVw/A8N7l9 cVU+MVez


;; RRSIG of the DNSKEYset that signs the RRset to chase:
example.com.            300     IN      RRSIG   DNSKEY 10 2 300 20120909052125 20120810052125 41861 example.com. KEAnlTPJsxS1lg4vJv3MdblH9LgPq5Mcv5uxhjnujHiyJkPw9kl57lcp GyFOZcWcE226fBoM+YkzHhziiPmTnjxZBWK9unnsyBgfsGy+t6YlvorQ XB60O0AAgrbDouWg9HO3wpYjILXK37w/J+MkCYXPpj1o5+OU5Adtl/LK HJQ=
example.com.            300     IN      RRSIG   DNSKEY 10 2 300 20120909052125 20120810052125 49764 example.com. V1fqbwK/USLsnHN2Q6tgN4mFMZtaEjtbhkSzUCPDq6TFsOEClHF09Do7 0mEDQCqW+r1DljpAPVzHBHzzKz5DAMLApn+qVeE+NaD0/WvMeh5nyvMQ 8jQ0102M7i9bVuRvnfSKRU74UxWD71Py6AS6wyg26KBgP9RIs4f5UEeN lPc=



Launch a query to find a RRset of type DS for zone: example.com.
;; NO ANSWERS: no more

;; WARNING There is no DS for the zone: example.com.



;; WE HAVE MATERIAL, WE NOW DO VALIDATION
;; VERIFYING A RRset for example.com. with DNSKEY:41861: success
;; OK We found DNSKEY (or more) to validate the RRset
;; Ok, find a Trusted Key in the DNSKEY RRset: 49764
;; VERIFYING DNSKEY RRset for example.com. with DNSKEY:49764: success

;; Ok this DNSKEY is a Trusted Key, DNSSEC validation is ok: SUCCESS

{% endhighlight %}


### recursive resolver

建立`trusted-keys`文件

{% highlight text %}
trusted-keys {
example.com.            257 3 10 "AwEAAboBxp1wNbmxhINtxORCNfwQQaZ3QlTtlxfV+jCRY5R44ri1ygI5kZEToqiB7W6nnxbUi9T5HRGmJmprl7QapEzw4S8YaUXCdYAPy8tNFHMSsrj2d72r2gR2DSBp4C5ZD5XGdk9kV6GSbCl0DMd0nzabSLMVw/A8N7l9cVU+MVez";
};
{% endhighlight %}

#### bind 

启动bind作为recursive resolver

{% highlight bash %}
#!/usr/bin/env bash

ROOT="$(pwd)"

mkdir -p "${ROOT}/recursive-keys"
mkdir -p "${ROOT}/recursive-zones"

if [[ ! -e "recursive.conf" ]]; then

cat >"recursive.conf" << EOF
options {
        listen-on               port 8253       { 127.0.0.1; };
        directory               "${ROOT}/recursive-zones";
        pid-file                "${ROOT}/recursive.pid";
        session-keyfile         "${ROOT}/recursive.session.key";
        managed-keys-directory  "${ROOT}/recursive-keys";

        allow-query             { 127.0.0.1; };
        recursion               yes;
        dnssec-validation       yes;        
        forwarders { 127.0.0.1 port 8053; };
};

controls {};

include "${ROOT}/trusted-keys";
EOF

fi

named -c recursive.conf -g
{% endhighlight %}

使用`dig`查看结果

{% highlight console %}
$ dig -p 8253 @localhost example.com. +dnssec

; <<>> DiG 9.8.2-RedHat-9.8.2-1.fc16 <<>> -p 8253 @localhost example.com. +dnssec
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 29620
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 2, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 4096
;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            78      IN      A       127.0.0.1
example.com.            78      IN      RRSIG   A 10 2 300 20120909052125 20120810052125 41861 example.com. A5raSwawZlfWejUvvWG+DYTiAMhbWyTXyScEYNxJxSyOrzZGLD4gGlFI RGmt91nmyw2+f2sHHqlRtvEmcxzFydTwZJs0lTdkQ3PODov4btEah52N aJGADObHaIAqZYcvYPlIpDDcZNIDQxbJbQyI6+JmWoFJN4QwyqXLn9dr LTU=

;; AUTHORITY SECTION:
example.com.            78      IN      NS      ns.example.com.
example.com.            78      IN      RRSIG   NS 10 2 300 20120909052125 20120810052125 41861 example.com. JMTkJtNQ75fRhHY+QgMqkVChHKAOiV+tnG3YiEKEBVmgBoslNaCdTFvw PJXfxCh776Nl+o5xbNkA6nZNcAA6UlM8/v9piK5+K1as7n5MJTiIDacC KiHYIwZvBrs8F3OVybXV+rTshFz4t19NNx8snJD9yP+UJLjmxV3Ej0OP QKo=

;; Query time: 1 msec
;; SERVER: 127.0.0.1#8253(127.0.0.1)
;; WHEN: Fri Aug 10 15:39:16 2012
;; MSG SIZE  rcvd: 415

{% endhighlight %}

#### unbound

启动unbound作为recursive resolver

{% highlight bash %}
#!/usr/bin/env bash

ROOT="$(pwd)"


if [[ ! -e "unbound.conf" ]]; then

cat >"unbound.conf" << EOF
server:
    num-threads: 1
    port: 8353
    directory: "${ROOT}"
    trusted-keys-file: "${ROOT}/trusted-keys"
    pidfile: "${ROOT}/unbound.pid"
    verbosity: 1
    use-syslog: no
    do-daemonize: no
    username: "$(whoami)"
    do-not-query-localhost: no


forward-zone:
    name: "example.com."
    forward-addr: 127.0.0.1@8053
EOF

fi

unbound -c unbound.conf
{% endhighlight %}

使用`dig`查看结果

{% highlight console %}
$ dig -p 8353 @localhost example.com. +dnssec

; <<>> DiG 9.8.2-RedHat-9.8.2-1.fc16 <<>> -p 8353 @localhost example.com. +dnssec
; (1 server found)
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 28672
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 2, AUTHORITY: 2, ADDITIONAL: 3

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags: do; udp: 4096
;; QUESTION SECTION:
;example.com.                   IN      A

;; ANSWER SECTION:
example.com.            300     IN      A       127.0.0.1
example.com.            300     IN      RRSIG   A 10 2 300 20120909052125 20120810052125 41861 example.com. A5raSwawZlfWejUvvWG+DYTiAMhbWyTXyScEYNxJxSyOrzZGLD4gGlFI RGmt91nmyw2+f2sHHqlRtvEmcxzFydTwZJs0lTdkQ3PODov4btEah52N aJGADObHaIAqZYcvYPlIpDDcZNIDQxbJbQyI6+JmWoFJN4QwyqXLn9dr LTU=

;; AUTHORITY SECTION:
example.com.            300     IN      NS      ns.example.com.
example.com.            300     IN      RRSIG   NS 10 2 300 20120909052125 20120810052125 41861 example.com. JMTkJtNQ75fRhHY+QgMqkVChHKAOiV+tnG3YiEKEBVmgBoslNaCdTFvw PJXfxCh776Nl+o5xbNkA6nZNcAA6UlM8/v9piK5+K1as7n5MJTiIDacC KiHYIwZvBrs8F3OVybXV+rTshFz4t19NNx8snJD9yP+UJLjmxV3Ej0OP QKo=

;; ADDITIONAL SECTION:
ns.example.com.         300     IN      A       127.0.0.1
ns.example.com.         300     IN      RRSIG   A 10 3 300 20120909052125 20120810052125 41861 example.com. MgDjvx9Xmfg/p872Im2QhRgehKZi8yKr8E8dfueT+uhfp5KCx0g6pIX4 5VLJO/lYmdaG+vRQyj0FLTLntDIM9G/5rlKp9CISH4yD6nsyfQI63FM1 lwDM29fytCilHXvgWb64jbGf/lHxuKsaZjsvaJyRZeWyEzpFKNq8BB5v RHI=

;; Query time: 1 msec
;; SERVER: 127.0.0.1#8353(127.0.0.1)
;; WHEN: Fri Aug 10 15:48:40 2012
;; MSG SIZE  rcvd: 602

{% endhighlight %}

## SSHFP

生成SSH密钥对

{% highlight console %}
$ ssh-keygen -q -N '' -f id_rsa
{% endhighlight %}

转换成SSHFP记录，并把这行添加到`zones/example.com`里

{% highlight console %}
$ ssh-keygen -r example.com. -f id_rsa.pub 
example.com. IN SSHFP 1 1 5727cac5dcca0d87c2b74f33e6e6106f09a03d27
{% endhighlight %}

SSH客户端使用的`config`文件

{% highlight text %}
Host example.com
    Port 8022
    VerifyHostKeyDNS yes
    StrictHostKeyChecking ask
{% endhighlight %}

运行一个临时的SSH Server

{% highlight python %}
#!/usr/bin/env python2

from twisted.python import log
import sys
log.startLogging(sys.stderr)

from twisted.internet import reactor
from twisted.conch.ssh import factory
from twisted.conch.ssh import keys

SSHD_KEY = 'id_rsa'

PUBLIC_KEY = keys.Key.fromFile(SSHD_KEY)
PRIVATE_KEY = keys.Key.fromFile(SSHD_KEY)

SSH_TYPE = PUBLIC_KEY.sshType()
FINGERPRINT = PUBLIC_KEY.fingerprint()

class SSHFactory(factory.SSHFactory):
    publicKeys = {SSH_TYPE: PUBLIC_KEY}
    privateKeys = {SSH_TYPE: PRIVATE_KEY}


reactor.listenTCP(8022, SSHFactory())
reactor.run()
{% endhighlight %}

劫持SSH客户端的DNS请求，将其发往8253端口

{% highlight c %}
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include <errno.h>

#include <stdio.h>
#include <stdint.h>
#define __USE_GNU
#include <dlfcn.h>


static in_port_t sendto_port = 0;
static in_addr_t sendto_addr = INADDR_NONE;

int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen) {
  static int (*_connect)(int sockfd, const struct sockaddr *addr, socklen_t addrlen) = NULL;
  if (!_connect) _connect = dlsym(RTLD_NEXT, "connect");
  struct sockaddr_in *addr_in = (struct sockaddr_in *)addr;
  if (ntohs(addr_in->sin_port) != 53) return _connect(sockfd, addr, addrlen);

  struct sockaddr_in new_addr_in = {
    .sin_family = addr_in->sin_family,
    .sin_port = htons(8253),
    .sin_addr = { .s_addr = htonl(INADDR_LOOPBACK) },
    .sin_zero = {0,0,0,0,0,0,0,0},
  };

  sendto_addr = addr_in->sin_addr.s_addr;
  sendto_port = addr_in->sin_port;

  return _connect(sockfd, (struct sockaddr *)&new_addr_in, sizeof(new_addr_in));
}

ssize_t recvfrom(int sockfd, void *buf, size_t len, int flags, struct sockaddr *src_addr, socklen_t *addrlen) {
  static ssize_t (*_recvfrom)(int sockfd, void *buf, size_t len, int flags, struct sockaddr *src_addr, socklen_t *addrlen) = NULL;
  if (!_recvfrom) _recvfrom = dlsym(RTLD_NEXT, "recvfrom");

  ssize_t result = _recvfrom(sockfd, buf, len, flags, src_addr, addrlen);
  ((struct sockaddr_in *)src_addr)->sin_addr.s_addr = sendto_addr;
  ((struct sockaddr_in *)src_addr)->sin_port = sendto_port;
  return result;
}
{% endhighlight %}

编译，通过`LD_PRELOAD`运行SSH客户端

{% highlight console %}
$ gcc -shared -fPIC -o hook.so hook.c -ldl
$ LD_PRELOAD="$(pwd)/hook.so" ssh -v -i id_rsa -F config example.com
OpenSSH_5.8p2, OpenSSL 1.0.0i-fips 19 Apr 2012
debug1: Reading configuration data config
debug1: Applying options for example.com
debug1: Connecting to example.com [127.0.0.1] port 8022.
debug1: Connection established.
debug1: identity file id_rsa type 1
debug1: identity file id_rsa-cert type -1
debug1: Remote protocol version 2.0, remote software version Twisted
debug1: no match: Twisted
debug1: Enabling compatibility mode for protocol 2.0
debug1: Local version string SSH-2.0-OpenSSH_5.8
debug1: SSH2_MSG_KEXINIT sent
debug1: SSH2_MSG_KEXINIT received
debug1: kex: server->client aes128-ctr hmac-md5 none
debug1: kex: client->server aes128-ctr hmac-md5 none
debug1: sending SSH2_MSG_KEXDH_INIT
debug1: expecting SSH2_MSG_KEXDH_REPLY
debug1: Server host key: RSA c4:04:b5:ef:1f:d3:0b:9a:44:13:a3:4e:e8:69:20:f2
debug1: found 1 secure fingerprints in DNS
debug1: matching host key fingerprint found in DNS
debug1: ssh_rsa_verify: signature correct
debug1: SSH2_MSG_NEWKEYS sent
debug1: expecting SSH2_MSG_NEWKEYS
debug1: SSH2_MSG_NEWKEYS received
debug1: Roaming not allowed by server
debug1: SSH2_MSG_SERVICE_REQUEST sent
Connection closed by 127.0.0.1

{% endhighlight %}

现在就不再提示需要确认服务端公钥了



