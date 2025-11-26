---
comment: true
---

# Hackergame 2024

!!! abstract

    中国科学技术大学第十一届信息安全大赛。

    - 比赛链接：[Hackergame 2024](https://hack.lug.ustc.edu.cn/)
    - 比赛时间：2024 年 11 月 2 日 12:00 - 2024 年 11 月 9 日 12:00
    - 成绩：总分数 5000，总排名 56 / 2460，浙江大学组内排名 6 / 44

本题解记录一些和大家不一样的解及个人比较喜欢的题目。

## 喜爱的题目

### PowerfulShell

Bash 变量展开。

`~` 展开为 `/players`，`$[]` 为 0，`$-` 为 `hB`，通过字符串切片可拼接出 `sh`。

```sh
__=~                    # /players
___=$[]                 # 0
____=$-                 # hB

${__:7:1}               # s
${____:___:1}           # h
${__:7:1}${____:___:1}  # sh
```

### 强大的正则表达式

构造 DFA 后状态消除算法转换为正则表达式。

### 优雅的不等式

构造积分

$$
\int_0^1 \frac{x^{2n} ( 1 - x^2 )^n (a + b x^2)}{1 + x^2} \mathrm{d}x,
$$

该积分的结果为 $p\pi - q$ 形式，计算积分后解方程可得 $a, b$。需满足 $a > 0$ 且 $a + b > 0$，$n$ 需足够大。观察到测试点对应的 $n$ 单调不减，据此优化枚举。

## 不一样的解

### 猫咪问答 Q4 & Q6

枚举爆破。

### 旅行照片 Q5

其实截取图中建筑物进行 Google 识图可直接匹配到原建筑，为京张高铁北京北动车所。

### 不太分布式的软总线

D-Bus 通信题。

大家都是 C 写的，然而我一直配不好这里编译所需的 C 环境；这里使用了 Rust 实现。

??? example

    ```rs
    use std::ffi::CString;
    use zbus::{Connection, Result, dbus_proxy};
    use nix::unistd::{pipe, write};
    use zbus::zvariant::Fd;

    #[dbus_proxy(
        interface = "cn.edu.ustc.lug.hack.FlagService",
        default_path = "/cn/edu/ustc/lug/hack/FlagService"
    )]

    trait FlagService {
        fn GetFlag1(&self, input: &str) -> Result<String>;
        fn GetFlag2(&self, input: Fd) -> Result<String>;
        fn GetFlag3(&self) -> Result<String>;
    }

    fn set_process_name(name: &str) {
        let c_name = CString::new(name).unwrap();
        unsafe {
            libc::prctl(libc::PR_SET_NAME, c_name.as_ptr() as usize, 0, 0, 0);
        }
    }

    #[tokio::main]
    async fn main() -> Result<()> {
        let connection = Connection::system().await?;
        let proxy = FlagServiceProxy::new(&connection).await?;

        // Flag 1

        let flag1 = proxy.GetFlag1("Please give me flag1").await?;
        println!("{flag1}");

        // Flag 2

        let (read_fd, write_fd) = pipe().expect("Failed to create pipe");
        write(write_fd, b"Please give me flag2\n").expect("Failed to write to pipe");
        nix::unistd::close(write_fd).expect("Failed to close write end of pipe");

        let fd = Fd::from(read_fd);
        let flag2 = proxy.GetFlag2(fd).await?;
        println!("{flag2}");

        // Flag 3
        set_process_name("getflag3");
        let flag3 = proxy.GetFlag3().await?;
        println!("{flag3}");

        Ok(())

    }
    ```

### 禁止内卷

目录穿透任意文件写，由于开了 debug 所以 RCE 了。

比较非预期的地方是，不查看 `answers.json`，直接读取 `/flag` 文件。

`prerun.py` 中有 `open("/flag")` 逻辑，修改 `app.py` 在 flash 消息中输出 flag 内容即可。

```python
flag = open("/flag", "r").read()
flash(f"评测成功，你的平方差为 {flag}")
```
