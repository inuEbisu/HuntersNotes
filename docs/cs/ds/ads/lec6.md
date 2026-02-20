---
comment: true
---

# Lec 6. Backtracing

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
