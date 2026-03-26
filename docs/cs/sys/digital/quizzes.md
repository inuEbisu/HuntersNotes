---
comment: true
---

# Quizzes

## Quiz 1

1. Represent the decimal number 75 as a 7-bit binary number: `( 1 )`, and as a BCD code: `( 2 )`. Then add an even parity bit at the most significant bit (MSB) of the BCD code to form a 9-bit code: `( 3 )`.

2. Simplify the Boolean expression $XY + \bar{X}Z + X\bar{Y} + \bar{Y}Z$ to its minimum number of literals:
    - A: $Y + Z$
    - B: $X + Z$
    - C: $X + Y$
    - D: $X + Y + Z$

3. Which of the following expressions has its dual equal to its complement?
    - A: $\bar{A} + BC$
    - B: $\bar{A}B + BC$
    - C: $\bar{A}\bar{B} + BC$
    - D: $\bar{A}B + A\bar{B}$

4. What is the sum-of-minterms (SOM) form of the expression $F(A,B,C) = \bar{A}B + BC$?
    - A: $\sum m(2,3,7)$
    - B: $\sum m(0,1,4)$
    - C: $\sum m(2,4,6)$
    - D: $\sum m(2,3,6)$

??? info "Answer"

    1. As below:
        - **Binary Code**: $1001011_2$
            - $75 = 64 + 11$
        - **BCD Code**: $0111\ 0101$
        - **9-bit Code (Even Parity)**: $1\ 0111\ 0101$

    2. B ($X + Z$)
    3. D ($\bar{A}B + A\bar{B}$)
        - $f^D(x, y, z) = \bar{f}(x, y, z) = f^D(\bar{x}, \bar{y}, \bar{z}) \Longleftrightarrow f(x, y, z) = f(\bar{x}, \bar{y}, \bar{z})$
    4. A ($\sum m(2,3,7)$)
