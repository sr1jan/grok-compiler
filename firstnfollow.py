"""
---------------------
Author: Srijan Singh
---------------------

Important:
    1. First(t) --> {t}, where t is terminal
    2. First(X) --> ε, if X --> ε or X --> Ai...An where First(Ai) --> ε for 1<=i<=n
    3. Follow(S) --> {$}, where S is start symbol
    4. Follow(B) --> Follow(X), where X --> AB
    5. Follow(A) --> First(B) - ε + Follow(X), where X --> AB and ε ∈ First(B)

Production rules (Grammar):
    E --> TE'
    E' --> +TE' | ε
    T --> FT'
    T' --> *FT' | ε
    F --> id | (E)

Assumptions (for input):
    E' --> X
    T' --> Y
    ε  --> ?

Expected answer:
    First:
        E --> First(T) --> First(F) --> {id, '('}
        X --> {+, ?}
        T --> First(F) --> {id, '('}
        Y --> {*, ?}
        F --> {id, '('}

Expected answer:
    Follow:
        E --> {$, ')'}
        X --> {$, ')'}
        T --> {+, $, ')'}
        Y --> {+, $, ')'}
        F --> {*, $, ')', +}

Lexical Structure :
    Terminals (<token_class, lexeme>):
        keyword: id
        char: [a-z]
        special notations: +, *, '(', ')'
    epsilon: ? as (ε)
"""

import re
from sys import exit
from typing import Dict, Set


class FirstnFollow:
    """
    FirstnFollow Manual:
        Generates First and Follow for production rules
        1. FirstnFollow.first --> First Table
        2. FirstnFollow.follow --> Follow Table
        3. FirstnFollow.table --> First and Follow together

        Input format --> string<NT --> NT/T/?=ε>:
            E --> TX
            X --> +TX | ?
            T --> FY
            Y --> *FY | ?
            F --> id | (E)
    """

    def __init__(self, prod_rules: str) -> None:
        # {NT --> List[<NT/T/ε>]}
        try:
            self.rules_dict: Dict = {
                rule.strip()
                .split("-->")[0]
                .strip(): [T.strip() for T in rule.strip().split("-->")[1].split("|")]
                for rule in prod_rules.split("\n")
                if len(rule.strip()) > 1
            }
        except Exception:
            print(f"Kindly use a valid input!\n{FirstnFollow.__doc__}")
            exit()
        print(f"Grammar:{re.sub(r'[?]', 'ε', prod_rules)}")
        # (special notation | id | chars | {? | ?=ε})
        self.regex = "(?:[*+()]|(id)|[a-z]|[?])"
        # first, follow
        self.__first: Dict = {}
        self.__follow: Dict = {}

    def __str__(self):
        return f"Production Rules --> {self.rules_dict}"

    @property
    def first(self) -> str:
        """Display First (FirstnFollow.first)"""
        self.get_first()
        display: str = "NT\t\tFirst\n"
        for n_t, rhs in self.__first.items():
            first_rhs = (",  ".join(rhs)).replace("?", "ε")
            display += f"{n_t}\t\t{first_rhs}\n"
        return display

    @property
    def follow(self) -> str:
        """Display follow (FirstnFollow.follow)"""
        self.get_first()
        self.get_follow()
        display: str = "NT\t\tFollow\n"
        for n_t, rhs in self.__follow.items():
            follow_rhs = ",  ".join(rhs)
            display += f"{n_t}\t\t{follow_rhs}\n"
        return display

    @property
    def table(self) -> str:
        """Display first and follow table (FirstnFollow.table)"""
        self.get_first()
        self.get_follow()
        display: str = "NT\t\tFirst\t\tFollow\n"
        for n_t in self.rules_dict.keys():
            first_rhs = (",  ".join(self.__first[n_t])).replace("?", "ε")
            follow_rhs = ",  ".join(self.__follow[n_t])
            display += f"{n_t}\t\t{first_rhs}\t\t{follow_rhs}\n"

        return display

    def get_first(self):
        """Generates First"""
        # init first
        for n_t in self.rules_dict:
            self.__first[n_t] = set()
        for n_t in self.rules_dict:
            self.__first[n_t].update(self.__recur_first(n_t))

    def __recur_first(self, n_t: str) -> Set:
        """Find Firsts recursively"""
        firsts: Set = set()
        try:
            for rhs in self.rules_dict[n_t]:
                for i, val in enumerate(rhs):
                    match = re.match(self.regex, rhs[i:])
                    # got epsilon or terminal
                    if match:
                        firsts.add(match.group())
                        break
                    # got non-terminal
                    else:
                        if len(self.__first[val]) != 0:
                            child_firsts = self.__first[val]
                        else:
                            child_firsts = self.__recur_first(val)
                        firsts.update(child_firsts)
                        # child node firsts does not include epsilon
                        if "?" not in child_firsts:
                            break
        except KeyError:
            pass  # invalid n_t

        return firsts

    def get_follow(self):
        """Generates Follow"""
        self.__follow[next(iter(self.rules_dict))] = {"$"}
        # init follow
        for n_t in self.rules_dict.keys():
            if n_t not in self.__follow:
                self.__follow[n_t] = set()
        for n_t in self.rules_dict:
            nt_follow = self.__recur_follow(n_t)
            self.__follow[n_t].update(nt_follow)

    def __recur_follow(self, n_t: str) -> Set:
        ans = self.__follow
        for cur_nt, rhs in self.rules_dict.items():
            match_rhs = list(filter(lambda x: n_t in x, rhs))
            for item in match_rhs:
                start_idx = item.index(n_t) + 1
                while start_idx <= len(item):
                    # Last item of rhs
                    if start_idx == len(item):
                        if len(ans[cur_nt]) != 0:
                            ans[n_t].update(ans[cur_nt])
                        else:
                            ans[n_t].update(self.__recur_follow(cur_nt))
                    else:
                        val = re.match(self.regex, item[start_idx:])
                        # terminal or epsilon as right item
                        if val:
                            if val.group() != "?":
                                ans[n_t].add(val.group())
                                break
                        # right item is NT
                        else:
                            nt_right = item[start_idx]
                            child_first = set.copy(self.__first[nt_right])
                            # substitute epsilon
                            if "?" in child_first:
                                child_first.remove("?")
                                ans[n_t].update(child_first)
                            else:
                                ans[n_t].update(child_first)
                                break
                    start_idx += 1

        return self.__follow[n_t]


# driver code
if __name__ == "__main__":
    PROD_RULES = """
                    E --> TX
                    X --> +TX | ?
                    T --> FY
                    Y --> *FY | ?
                    F --> id | (E)
                """

    # PROD_RULES = """
    #                 S --> aBDh
    #                 B --> cC
    #                 C --> bC | ?
    #                 D --> EF
    #                 E --> g | ?
    #                 F --> f | ?
    #             """

    # PROD_RULES = """
    #                 S --> ACB | Cbb | Ba
    #                 A --> da | BC
    #                 B --> g | ?
    #                 C --> h | ?
    #             """

    ff = FirstnFollow(PROD_RULES)
    print(ff.table)
