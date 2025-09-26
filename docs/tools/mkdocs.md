---
comment: true
---

# MkDocs

写 MkDocs 常常忘记语法，于是这或许是自用的 Cheatsheet。

## Pymdownx

简单记录一下扩展 `pymdownx` 的用法。

### Tabbed 选项卡

=== "C++"

    ```cpp
    #include <iostream>

    int main(void) {
        std::cout << "Hello World!" << std::endl;
        return 0;
    }
    ```

=== "Python"

    ```py
    print("Hello World!")
    ```

Source Code:

````md

=== "C++"

    ```cpp
    #include <iostream>

    int main(void) {
        std::cout << "Hello World!" << std::endl;
        return 0;
    }
    ```

=== "Python"

    ```py
    print("Hello World!")
    ```

````

### Tasklist 任务清单

- [x] Alice
- [x] Bob
- [ ] Charlie
- [ ] Eve

```md
- [x] Alice
- [x] Bob
- [ ] Charlie
- [ ] Eve
```

## Admonitions

简单记录一下扩展 `admonition` 的用法。

### 通常的用法

!!! note

    这里是一些提示。

```md
!!! note

    这里是一些提示。
```

### 自定义标题

!!! note "标题"

    这里是一些记录。

```md
!!! note "标题"

    这里是一些记录。
```

### 内联的用法

!!! note inline

    这是一个靠左侧的内联块。

```md
!!! note inline

    这是一个靠左侧的内联块。
```

而且

!!! note inline end

    这是一个靠右侧的内联块。

```md
!!! note inline end

    这是一个靠右侧的内联块。
```

### 嵌套的用法

!!! note "外部标题"

    这是外部内容。

    !!! note "这是一个嵌套标题"

        这是一个嵌套内容。

```md
!!! note "外部标题"

    这是外部内容。

    !!! note "这是一个嵌套标题"

        这是一个嵌套内容。
```

### 不同的类型

!!! note

!!! tip

!!! info

!!! abstract

!!! success

!!! question

!!! warning

!!! failure

!!! danger

!!! bug

!!! example

!!! quote

```md
!!! note

!!! tip

!!! info

!!! abstract

!!! success

!!! question

!!! warning

!!! failure

!!! danger

!!! bug

!!! example

!!! quote
```

## LaTeX 公式

!!! note

    使用 KaTeX 进行渲染。

假设 $\sum_{n=1}^\infty a_n$ 是一个条件收敛的无穷级数。对任意的一个实数 $C$ ，都存在一种从自然数集合到自然数集合的排列 $\sigma : \, \, n \mapsto \sigma (n)$，使得

$$
  \sum_{n=1}^\infty a_{\sigma (n)} = C.
$$

此外，也存在另一种排列 $\sigma' : \, \, n \mapsto \sigma' (n)$ ，使得

$$
  \sum_{n=1}^\infty a_{\sigma' (n)} = \infty.
$$

类似地，也可以有办法使它的部分和趋于 $-\infty$ ，或没有任何极限。

反之，如果级数是绝对收敛的，那么无论怎样重排，它仍然会收敛到同一个值，也就是级数的和。

```md
假设 $\sum_{n=1}^\infty a_n$ 是一个条件收敛的无穷级数。对任意的一个实数 $C$ ，都存在一种从自然数集合到自然数集合的排列 $\sigma : \, \, n \mapsto \sigma (n)$，使得

$$
  \sum_{n=1}^\infty a_{\sigma (n)} = C.
$$

此外，也存在另一种排列 $\sigma' : \, \, n \mapsto \sigma' (n)$ ，使得

$$
  \sum_{n=1}^\infty a_{\sigma' (n)} = \infty.
$$

类似地，也可以有办法使它的部分和趋于 $-\infty$ ，或没有任何极限。

反之，如果级数是绝对收敛的，那么无论怎样重排，它仍然会收敛到同一个值，也就是级数的和。
```
