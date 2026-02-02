---
comment: true
---

# 网络配置

## Clash 规则

```yaml
dns:
    default-nameserver:
        - dhcp://system
        - https://223.5.5.5/dns-query

    nameserver:
        - https://doh.pub/dns-query
        - https://dns.alidns.com/dns-query

    nameserver-policy:
        "*zju.edu.cn": dhcp://system
        "*cc98.org": dhcp://system
        "geosite:private": dhcp://system

rules:
    - DOMAIN-SUFFIX,zju.edu.cn,DIRECT
    - DOMAIN-KEYWORD,zju,DIRECT
    - DOMAIN-KEYWORD,cc98,DIRECT
    - GEOIP,PRIVATE,DIRECT,no-resolve
    - IP-CIDR,10.0.0.0/8,DIRECT,no-resolve
    - IP-CIDR,172.16.0.0/12,DIRECT,no-resolve
    - IP-CIDR,192.168.0.0/16,DIRECT,no-resolve
```

校网环境下所有校内出口的 UDP/53 均被阻断，所以需要使用 DoH。
