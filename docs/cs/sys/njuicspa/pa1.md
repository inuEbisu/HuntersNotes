---
comment: true
---

# PA1

!!! abstract

    PA1 的实验心得。

!!! quote "WIP"

配置了 `ccache`。

## 部分蓝框思考题

!!! question

    计算机可以没有寄存器吗？如果可以，这会对硬件提供的编程模型有什么影响呢？

??? info "Answer"

    可以。

    编程模型主要包括指令集架构、内存模型、数据类型与执行模型等方面。指令集架构上，会导致每条指令的操作数都必须是内存地址，每条指令都会变得很长而且很慢；内存模型会变得简单，无需再进行寄存器分配。

    ```s
    ADD [C], [A], [B] ; *c = *a + *b
    ```

!!! question

    对于 GNU/Linux 上的一个程序，怎么样才算开始？怎么样才算是结束？对于在 NEMU 中运行的程序，问题的答案又是什么呢？NEMU 中为什么要有 `nemu_trap`？为什么要有 `monitor`？

??? info "Answer"

    对于 GNU/Linux 上的程序，在 `Shell` 中输入 `./my_program` 时：

    + Shell 进程会调用 `fork()` 创建一个新的子进程，然后调用 `execve()` 系统调用。
    + 内核处理 `execve()` 系统调用，具体会检查 ELF 格式，为新程序建立页表，将程序的代码段和数据段从磁盘加载到内存，初始化堆栈等。
    + 如果程序需要动态链接库，内核会加载并运行动态链接器，进行动态链接。
    + 操作系统将 CPU 的 PC 设置为程序入口点（通常是 `_start`，由 C 运行时库提供），从此程序开始真正执行。`_start` 进行一些初始化后调用 `main()` 函数。

    结束过程是这样的：

    + 程序执行到 `main()` 函数的 `return` 语句或调用 `exit()` 函数；实质上最终会执行 `exit_group()` 或类似的系统调用。
    + 内核接管控制权，释放该进程占用的所有资源（内存、打开的文件描述符、信号量等），随后通知父进程该子进程已终止（发送 `SIGCHLD` 信号）。

    由于 NEMU 中没有 OS，所以没有 `exit` 等系统调用；程序需要 `nemu_trap` 来宣告结束。

    Monitor 负责解析命令行参数、读入客户程序镜像、初始化内存和寄存器等引导与初始化工作；同时还集成了简易调试器（`sdb`）。

!!! question

    如果在运行 NEMU 之后直接键入 `q` 退出，你会发现终端输出了一些错误信息。请分析这个错误信息是什么原因造成的，然后尝试在 NEMU 中修复它。

??? info "Answer"

    在 NEMU 的交互（sdb）中，`q` 命令只是让命令循环退出（`handler` 返回 `-1`），但并没有把全局状态 `nemu_state.state` 设为 `NEMU_QUIT`。因此程序在 `main()` 处最终的 `is_exit_status_bad()` 返回了退出码 1。

    ```c title="sdb.c" linenums="51" hl_lines="2"
    static int cmd_q(char *args) {
        nemu_state.state = NEMU_QUIT;
        return -1;
    }
    ```
