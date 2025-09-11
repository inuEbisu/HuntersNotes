# MkDocs

写 MkDocs 常常忘记语法，于是这或许是自用的 Cheatsheet。

## 代码块

```cpp
#include <iostream>

int main(void) {
    std::cout << "Hello world!" << std::endl;
    return 0;
}
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