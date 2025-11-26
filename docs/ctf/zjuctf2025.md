---
comment: true
---

# ZJUCTF 2025

!!! abstract

    浙江大学 2025 年信息安全校赛。

    - 比赛链接：[ZJUCTF 2025 - ZJU::CTF](https://ctf.zjusec.com/games/6)
    - 比赛时间：2025 年 11 月 17 日 20:00 - 2025 年 11 月 25 日 20:00
    - 成绩：无

## 出题

很荣幸能够为浙江大学 2025 年信息安全校赛（ZJUCTF 2025）出题！

点子略有些枯竭 :( 希望来年自己的水平会更高。

### 陆拾肆

> Intonation!!! 有感

猜谜 Misc。

这是一个用六十四平均律写的 Base64。即每一个正弦波的频率满足

$$
f = f_0 \cdot 2^{\frac{i}{64}}
$$

其中 $f_0 = 440 ~ \text{Hz}$，$i$ 为 Base64 字符集中的索引。

朴素 FFT 分析频率时只能精确到 $\frac{1}{T}$，对于本题来说，每一个正弦波长度 0.1s，故只能精确到 10 Hz，并不足以解出本题；可考虑 Zero Padding 或插值等方法。

音频中包含国际标准音高 A4 = 440 Hz，测题时发现大模型可以注意到所以没有放提示。预期中不必知道乐理知识，但需要猜测的是这里可能存在一个双射，而不是将所有出现过的频率从小到大排列分别对应索引 0-40 之类。事实上这个双射是等比数列，使用指数函数拟合即可，甚至用二次函数拟合也可以。

原本为此准备了两个 Hint：

- FFT 只能精确到 $\frac{1}{T}$

- Geometric Progression

不过一个都还没放就已经有解了，于是就不放了。

??? example

    ```py
    import numpy as np
    from scipy.io.wavfile import read
    from scipy.fft import rfft, rfftfreq
    import base64

    # Constants
    FILE = "sixty_four.wav"
    CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    BASE_FREQ = 440.0
    DURATION = 0.1

    # Read Audio
    fs, data = read(FILE)
    if data.ndim > 1:
        data = data[:, 0]
    N = int(DURATION * fs)

    # Decode
    res = ""
    for i in range(0, len(data) - len(data) % N, N):
        chunk = data[i : i + N]

        # FFT
        padded_n = len(chunk) * 100
        yf = np.abs(rfft(chunk, n=padded_n))
        freq = rfftfreq(padded_n, 1 / fs)[np.argmax(yf[1:]) + 1]

        # Map to Char
        idx = int(round(64 * np.log2(freq / BASE_FREQ)))
        res += CHARS[idx] if 0 <= idx < 64 else "?"

    # Print Flag
    print(base64.b64decode(res).decode())
    ```

### Fall in Love

> 和 WuYan、城堡合作出题，最后变成了我不怎么看得懂的样子

## 做题

赛程中有很多考试，所以没空看太多；不过也做了几道感兴趣的。

### ZJUWLAN-Insecure

题目给出了一个 `.pcap`，其中主要内容是两个 HTTP 请求：

```
GET /cgi-bin/get_challenge?callback=jQuery112404819198703215103_1756311042671&username=3220100721&ip=10.10.98.98&_=1756311042673 HTTP/1.1\r\n
    Request Method: GET
    Request URI: /cgi-bin/get_challenge?callback=jQuery112404819198703215103_1756311042671&username=3220100721&ip=10.10.98.98&_=1756311042673
    Request Version: HTTP/1.1

HTTP/1.1 200 OK\r\n
jQuery112404819198703215103_1756311042671({"challenge":"517557d10a3aff098a898753317e8ef0b2822540d067490585c41d39d847ed7a","client_ip":"10.10.98.98","ecode":0,"error":"ok","error_msg":"","expire":"60","online_ip":"10.10.98.98","res":"ok","srun_ver":"SRunCGIAuthIntfSvr V1.18 B20210926","st":1756309856})

GET /cgi-bin/srun_portal?callback=jQuery112404819198703215103_1756311042671&action=login&username=3220100721&password=%7BMD5%7D5f9601066c7ee059d8fdf0d710c7bc50&ac_id=3&ip=10.10.98.98&chksum=a5d4e260a6bd874d7036cb1ed3b251aaef3bd522&in
    Request Method: GET
    Request URI […]: /cgi-bin/srun_portal?callback=jQuery112404819198703215103_1756311042671&action=login&username=3220100721&password=%7BMD5%7D5f9601066c7ee059d8fdf0d710c7bc50&ac_id=3&ip=10.10.98.98&chksum=a5d4e260a6bd874d7036cb1ed3b251aaef
        Request URI Path: /cgi-bin/srun_portal
        Request URI Query […]: callback=jQuery112404819198703215103_1756311042671&action=login&username=3220100721&password=%7BMD5%7D5f9601066c7ee059d8fdf0d710c7bc50&ac_id=3&ip=10.10.98.98&chksum=a5d4e260a6bd874d7036cb1ed3b251aaef3bd522&info=%7B
            Request URI Query Parameter: callback=jQuery112404819198703215103_1756311042671
            Request URI Query Parameter: action=login
            Request URI Query Parameter: username=3220100721
            Request URI Query Parameter: password=%7BMD5%7D5f9601066c7ee059d8fdf0d710c7bc50
            Request URI Query Parameter: ac_id=3
            Request URI Query Parameter: ip=10.10.98.98
            Request URI Query Parameter: chksum=a5d4e260a6bd874d7036cb1ed3b251aaef3bd522
            Request URI Query Parameter: info=%7BSRBX1%7DKxvFtemc1wBEGdNAbPEfd7s02umxP0Nagix%2BYxJsqbAEh5%2FfzuIYqad8xrqKW4yzfA9%2FI3xGKPMTNziE1wPFhfnCaX8CWsnglgKKjVozxsa46BrEY0n4kc%2Fy2rdlbE7wWPBjdWxaZ4yfs8DLRovR7L%3D%3D
            Request URI Query Parameter: n=200
            Request URI Query Parameter: type=1
            Request URI Query Parameter: os=Linux
            Request URI Query Parameter: name=Linux
            Request URI Query Parameter: double_stack=0
            Request URI Query Parameter: _=1756311042674
    Request Version: HTTP/1.1
```

查阅 `net2.zju.edu.cn` 中的 `srun.portal.js` `main.js` `md5.js` 等源代码，发现 `info` 参数的生成是 `"{SRBX1}" + base64.encode(xEncode(json(d), token))`。这里的 `token` 就是 `challenge`，而 `d` 中有明文密码。故 Base64（这里是个换表 Base64）解码之后 `xDecode`（需要自己实现）即可。

??? example

    ```js
    function xEncode(str, key) {
        if (str == "") {
            return "";
        }
        var v = s(str, true),
            k = s(key, false);
        if (k.length < 4) {
            k.length = 4;
        }
        var n = v.length - 1,
            z = v[n],
            y = v[0],
            c = 0x86014019 | 0x183639A0,
            m,
            e,
            p,
            q = Math.floor(6 + 52 / (n + 1)),
            d = 0;
        while (0 < q--) {
            d = d + c & (0x8CE0D9BF | 0x731F2640);
            e = d >>> 2 & 3;
            for (p = 0; p < n; p++) {
                y = v[p + 1];
                m = z >>> 5 ^ y << 2;
                m += (y >>> 3 ^ z << 4) ^ (d ^ y);
                m += k[(p & 3) ^ e] ^ z;
                z = v[p] = v[p] + m & (0xEFB8D130 | 0x10472ECF);
            }
            y = v[0];
            m = z >>> 5 ^ y << 2;
            m += (y >>> 3 ^ z << 4) ^ (d ^ y);
            m += k[(p & 3) ^ e] ^ z;
            z = v[n] = v[n] + m & (0xBB390742 | 0x44C6F8BD);
        }
        return l(v, false);
    }

    function xDecode(str, key) {
        if (str == "") {
            return "";
        }
        var v = s(str, false),
            k = s(key, false);
        if (k.length < 4) {
            k.length = 4;
        }
        var n = v.length - 1,
            z = v[n],
            y = v[0],
            c = 0x86014019 | 0x183639A0,
            m,
            e,
            p,
            q = Math.floor(6 + 52 / (n + 1)),
            d = q * c;
        while (d !== 0) {
            e = d >>> 2 & 3;
            for (p = n; p > 0; p--) {
                z = v[p - 1];
                m = z >>> 5 ^ y << 2;
                m += (y >>> 3 ^ z << 4) ^ (d ^ y);
                m += k[(p & 3) ^ e] ^ z;
                y = v[p] = v[p] - m & (0xEFB8D130 | 0x10472ECF);
            }
            z = v[n];
            m = z >>> 5 ^ y << 2;
            m += (y >>> 3 ^ z << 4) ^ (d ^ y);
            m += k[(p & 3) ^ e] ^ z;
            y = v[0] = v[0] - m & (0xBB390742 | 0x44C6F8BD);
            d = d - c & (0x8CE0D9BF | 0x731F2640);
        }
        return l(v, true);
    }

    function s(a, b) {
        var c = a.length, v = [];
        for (var i = 0; i < c; i += 4) {
            v[i >> 2] = a.charCodeAt(i) | a.charCodeAt(i + 1) << 8 | a.charCodeAt(i + 2) << 16 | a.charCodeAt(i + 3) << 24;
        }
        if (b) {
            v[v.length] = c;
        }
        return v;
    }

    function l(a, b) {
        var d = a.length, c = (d - 1) << 2;
        if (b) {
            var m = a[d - 1];
            if ((m < c - 3) || (m > c))
                return null;
            c = m;
        }
        for (var i = 0; i < d; i++) {
            a[i] = String.fromCharCode(a[i] & 0xff, a[i] >>> 8 & 0xff, a[i] >>> 16 & 0xff, a[i] >>> 24 & 0xff);
        }
        if (b) {
            return a.join('').substring(0, c);
        } else {
            return a.join('');
        }
    }


    function customBase64Decode(encodedStr) {
        var custom_alpha = "LVoJPiCN2R8G90yg+hmFHuacZ1OWMnrsSTXkYpUq/3dlbfKwv6xztjI7DeBE45QA";
        var std_alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

        var translationMap = {};
        for (var i = 0; i < custom_alpha.length; i++) {
            translationMap[custom_alpha[i]] = std_alpha[i];
        }

        var std_b64_str = "";
        for (var i = 0; i < encodedStr.length; i++) {
            var char = encodedStr[i];
            if (char === '=') { // padding character
                std_b64_str += '=';
            } else {
                std_b64_str += translationMap[char];
            }
        }

        return Buffer.from(std_b64_str, 'base64').toString('latin1');
    }


    var encoded_info = "KxvFtemc1wBEGdNAbPEfd7s02umxP0Nagix+YxJsqbAEh5/fzuIYqad8xrqKW4yzfA9/I3xGKPMTNziE1wPFhfnCaX8CWsnglgKKjVozxsa46BrEY0n4kc/y2rdlbE7wWPBjdWxaZ4yfs8DLRovR7L==";

    var token = "517557d10a3aff098a898753317e8ef0b2822540d067490585c41d39d847ed7a";

    // Custom Base64 Decoding
    var binary_ciphertext = customBase64Decode(encoded_info);

    // xDecode
    var decrypted_json_string = xDecode(binary_ciphertext, token);
    console.log(decrypted_json_string);
    ```

### cs_master

> 出题出到一半被 5db 告知和 cs_master 撞 idea 了

题目给出了一个 CPU，目标是越权读取内核态内存。

这颗 CPU 的特权级信号 `privileged` 被实现为了一个全局寄存器。Control 单元会在 ID 阶段根据指令计算下一周期的特权状态 `next_privileged`，并在时钟上升沿更新 `privileged`；RAM 单元在 MEM 阶段进行内存读写时，会直接引用这个全局 `privileged` 信号校验权限。

故 `lw` 后紧跟 `ecall` 即可。`ecall` 在 ID 阶段将 `privileged` 置 1，此时 `lw` 在 MEM 阶段尝试读取 secret，读 `privileged` 为 1，就成功读到了。

一点小细节是需要将 `x3` 和 `x10` 置为一个比 `0x10000` 大的值，否则 Trap Handler 会死循环。

??? example

    ```py
    from pwn import *
    import base64

    context.arch = "riscv32"
    context.log_level = "debug"

    asm_code = """
        li x3, 0x20000
        li x10, 0x20000
        li x1, 0x80000000
        lw x14, 0(x1)
        ecall
        lw x15, 4(x1)
        ecall
        lw x16, 8(x1)
        ecall
        lw x17, 12(x1)
        ecall
        lw x18, 16(x1)
        ecall
        lw x19, 20(x1)
        ecall
        lw x20, 24(x1)
        ecall
        lw x21, 28(x1)
        ecall
        lw x22, 32(x1)
        ecall
        lw x23, 36(x1)
        ecall
        lw x24, 40(x1)
        ecall
        lw x25, 44(x1)
        ecall
    """


    binary = asm(asm_code)
    encoded = base64.b64encode(binary).decode()
    print(f"Base64 encoded binary:\n{encoded}")
    ```
