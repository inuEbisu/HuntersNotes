---
comment: true
---

# Lec 6. Backtracing

## 一些数学

!!! tip

    当 $n \to +\infty$ 时，对于常数 $a > 1$，有

    $$
    n^a \ll a^n \ll n! \ll n^n.
    $$

    其中 $f(n) \ll g(n)$ 表示 $\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0$，即 $f(n) = o(g(n))$。

!!! tip

    推论：

    $$
    \log{n!} = o(n \log{n}).
    $$

## Turnpike Reconstruction Problem

!!! quote "WIP"

## Alpha-beta Pruning

!!! info "推荐阅读"

    - OI Wiki: [Alpha-beta 剪枝](https://oi-wiki.org/search/alpha-beta/)

???+ example

    ```c
    int alphabeta(Node* node, int alpha, int beta, int is_max) {
        if(node->is_leaf) return node->value;

        if(is_max) {
            // max node
            for(int i = 0; i < node->child_amount; i ++) {
                Node* child = node->children[i];
                alpha = max(alpha, alphabeta(child, alpha, beta, !is_max));
                if(alpha >= beta) break;
            }
            return alpha;
        } else {
            // min node
            for(int i = 0; i < node->child_amount; i ++) {
                Node* child = node->children[i];
                beta = min(beta, alphabeta(child, alpha, beta, !is_max));
                if(alpha >= beta) break;
            }
            return beta;
        }
    }

    int main() {
        Node *root = read_tree();
        int result = alphabeta(root, INT_MIN, INT_MAX, 1);
        printf("%d\n", result);

        return 0;
    }
    ```
