"""
Author: Srijan Singh

important:
    1. First(terminal) --> terminal

Production rules:
    E --> TE'
    E' --> +TE' | e
    T --> FT'
    T' --> *FT' | e
    F --> id | (E)
    ----------------
    E --> TX
    X --> +TX | e
    T --> FY
    Y --> *FY | e
    F --> id | (E)

Assumptions:
    E' --> X
    T' --> Y

Lexical Structure:
    keyword: id
    char: [a-z]
    special notations: +, *, '(', ')'

First:
    expected answer:
        E --> First(T) --> First(F) --> {id, '('}
        X --> {+, e}
        T --> First(F) --> {id, '('}
        Y --> {*, e}
        F --> {id, '('}

"""

import re
from typing import Dict, List


class FirstnFollow:
    """Generates First and Follow for production rules"""

    def __init__(self, prod_rules: str) -> None:
        # {NT --> List[<NT/T>]}
        self.rules_dict = {
            rule.strip()
            .split("-->")[0]
            .strip(): [T.strip() for T in rule.strip().split("-->")[1].split("|")]
            for rule in prod_rules.split("\n")
            if len(rule.strip()) > 1
        }
        # Terminals (special notation | id | chars)
        self.regex = "(?:[*+()]|(id)|[a-z])"

    def __str__(self):
        return f"Production Rules --> {self.rules_dict}"

    def recur_first(self, n_t: str) -> List:
        """Find Firsts recursively"""
        firsts = []
        for val in self.rules_dict[n_t]:
            term = re.match(self.regex, val)
            if term:
                firsts.append(term.group())  # got terminal
            else:
                firsts.extend(self.recur_first(val[0]))  # got non-terminal
        return firsts

    def get_first(self) -> Dict:
        """Generates First"""
        ans: Dict = {}
        for n_t in self.rules_dict:
            ans[n_t] = self.recur_first(n_t)
        return ans

    @property
    def first(self) -> str:
        """Display First (FirstnFollow.first)"""
        firsts = self.get_first()
        display: str = "NT\t\tFirst\n"
        for n_t, rhs in firsts.items():
            display += f"{n_t}\t\t{',  '.join(rhs)}\n"
        return display

    # def getFollows(self) -> Dict:
    #     """Generates Follow"""
    #     ans: Dict = {}
    #     return ans


# driver code
if __name__ == "__main__":
    PROD_RULES = """
                    E --> TX
                    X --> +TX | e
                    T --> FY
                    Y --> *FY | e
                    F --> id | (E)
                """

    ff = FirstnFollow(PROD_RULES)
    print(ff.first)
