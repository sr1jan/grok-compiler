# init(grok-compiler)

while (grok != '100%' | !bored): 
    continue


## Syntax Analysis
- First and Follow ([code](https://github.com/sr1jan/grok-compiler/blob/master/firstnfollow.py))

    - Both **First** and **Follow** helps the compiler to optimize the construction of parse/syntax tree inorder to verify syntax correctness
    of the input string (code).

    - **First** precomputes the correct node of a production rule hence saving the compiler from backtracking to retrieve the node needed to generate the string from the parse tree.

    - **Follow** helps when a production rule fails to return the required [terminal value](https://en.wikipedia.org/wiki/Terminal_and_nonterminal_symbols). It basically lets the compiler to jump to a different node by applying the ε (epsilon) value and thereby vanishes the non-terminal value to generate the string. 


### References
 - [Compilers by Alex Aiken](https://archive.org/details/academictorrents_e31e54905c7b2669c81fe164de2859be4697013a) (Internet Archive <3)
