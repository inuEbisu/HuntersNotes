# Ch 3. Optimization of Learning

## Cost Functions

### The Motivation: Gradient Desensitization

In a network using **Sigmoid neurons** and **Quadratic cost** ($C = \frac{1}{2}\|y-a\|^2$), the error in the output layer is

$$\delta^L_j = (a^L_j - y_j) \sigma'(z^L_j).$$

**Saturation Problem**: When a neuron saturates ($\sigma'(z) \approx 0$), learning stalls even if the error $(a-y)$ is huge.

So we want

$$\delta^L_j = a^L_j - y_j.$$

To achieve it, we "cancel out" the $\sigma'(z)$ term by choosing specific cost functions for different neuron types.

### Sigmoid Neurons & Cross-Entropy Cost

For binary or multi-label classification, we pair Sigmoid with **Cross-Entropy**:

$$C_x = -[y \ln a + (1-y) \ln(1-a)].$$

### Softmax & Log-Likelihood Cost

For exclusive multi-class classification, we use **Softmax** output and **Log-Likelihood** cost:

$$a_j^L = \frac{e^{z_j^L}}{\sum_k e^{z_k^L}},$$

$$C_x = -\ln a^L_{y},$$

where $y$ is the index of the correct label.

### Linear Neurons & Quadratic Cost

For regression tasks, **Linear neurons** paired with **Quadratic cost** naturally satisfy the condition.

$$C = \frac{1}{2}\|y-a\|^2.$$

## Regularization

!!! quote "WIP"

## Weight Initialization

!!! quote "WIP"
