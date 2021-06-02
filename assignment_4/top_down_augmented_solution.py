# top_down_solution.py
# Jonas Kuhn, University of Stuttgart, 2021
# course "Parsing"

# enables input history in interactive mode
import readline

from nltk import CFG, Tree


# Boolean variable for switching tracing info on and off
trace = True  # set this to False if you don't want to see intermediate steps

# Boolean variable for running parser interactively on user input or on pre-specified input
interactive = True  # False

# internal format of cfg production rules with reversed right-hand sides (!)
# grammar = {'S': [['VP', 'NP']],
#      'NP': [['N', 'DET']],
#      'VP': [['V']], 'DET': [['the'], ['an'], ['my'], ['most']],
#      'N': [['elephant'], ['elephants'], ['mouse'], ['mice']],
#      'V': [['sneezed'], ['giggled'], ['trumpeted']]}

# string format used in nltk.CFG class:
# our test grammar:
grammar_string = """
S -> NP VP
NP -> DET N
VP -> V
DET -> 'the' | 'an' | 'my' | 'most'
N -> 'elephant' | 'elephants' | 'mouse' | 'mice'
V -> 'sneezed' | 'giggled' | 'trumpeted'
"""

# Additional grammars used in Assignment 03
grammar_string2 = """
S    -> '(' S Op S ')' | Num
Num  -> Sign Num | '1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'0'
Op   -> '+' | '-' | '*' | '/'
Sign -> '-'
"""

grammar_string3 = """
S -> NP VP
NP -> DET N | DET N PP | 'I'
VP -> V | V NP | V NP PP
PP -> P NP
DET -> 'the' | 'an' | 'my' | 'most'
P -> 'in'
N -> 'elephant' | 'elephants' | 'mouse' | 'mice' | 'pajamas'
V -> 'sneezed' | 'giggled' | 'trumpeted' | 'saw' | 'shot'
"""


# conversion procedure for grammar:
def load_grammar(grammar_string):
    cfg = CFG.fromstring(grammar_string)

    grammar = {}
    for prod in cfg.productions():
        nt = str(prod.lhs())
        rrhs = [str(a) for a in reversed(prod.rhs())]
        if nt not in grammar:
            grammar[nt] = [rrhs]
        else:
            grammar[nt].append(rrhs)
    return grammar


# recursive procedure for converting sequence of arity/symbol pairs into a tree
# (this version generates a representation format that can be graphically displayed
# using an nltk method)
def build_tree(deriv):
    if deriv:
        (arity, nt) = deriv[0]
        deriv_rest = deriv[1:]

        subtrees = []
        for i in range(arity):
            (subtree_i, deriv_rest) = build_tree(deriv_rest)
            subtrees.append(subtree_i)
        return Tree(nt, subtrees), deriv_rest
    else:
        return [], []


# main procedure:
def parse(grammar, tokens):
    # grammar:  dict with list of reversed rhs's for each non-terminal
    # tokens:   list of input tokens

    if trace:
        print("parsing ", tokens, "...")

    # initialize data structures:
    stack = ["S"]
    inbuffer = tokens
    # record-keeping for parser output:
    deriv = []

    # main loop:
    while inbuffer:
        if trace:
            print("           {:<40}{:>40}".format(str(stack), str(inbuffer)))

        # expand
        if stack[-1] in grammar:  # there must be a non-terminal on top of the stack
            # no backtracking, i.e. always pick the first production:
            rrhs = grammar[stack[-1]][0]  # RRHS: "reversed rhs"

            # to avoid being completely blind, choose a different production
            # in case it starts with the terminal that's next in the inbuffer:
            for prod in grammar[stack[-1]]:
                if inbuffer[0] == prod[-1]:
                    rrhs = prod
                    break  # keep the one for which there is a match, discard other productions

            if trace:
                print(" >expand: ", stack[-1], " -R-> ", rrhs)

            # for output: put pair of arity and NT in the list
            deriv += [(len(rrhs), stack[-1])]

            # the reversed rhs from the chosen production replaces NT on the stack
            stack = (stack[:-1] + rrhs)

            # leave variable inbuffer unchanged

        # match
        elif stack[-1] == inbuffer[0]:  # terminal on top of the stack matches next input symbol
            if trace:
                print(" >match:  ", stack[-1])
            deriv += [(0, stack[-1])]  # for output: put terminal (arity 0) in the list
            stack = stack[:-1]  # pop top element from the stack
            inbuffer = inbuffer[1:]  # consume first element from input buffer

        # no match:
        else:  # terminal on top of the stack doesn't match next input symbol
            if trace:
                print(" >dead end!")
            break  # since we cannot backtrack, we have to discard this attempt
            # (without having reached a termination condition)

    if trace:
        print("           {:<40}{:>40}".format(str(stack), str(inbuffer)))

    # termination
    if not (stack or inbuffer):
        print("success!")

        # convert output (the list named deriv) into the tree format that can be displayed:
        tree, subtrees = build_tree(deriv)
        tree.draw()

    # failure
    else:
        print("failure!")
    print()


def demo(grammar):
    # show internal representation of grammar
    if trace:
        print("Internal grammar representation:\n", grammar)
        print("----------------------------------------------------------------\n")

    # interactive way of running the parser in user input
    if interactive:
        while True:
            sentence = input('Type sentence ("q" to quit): ')  # user can input the string to be parsed
            if sentence == "q":
                break
            else:
                # split up string in tokens (using the default separator, i.e. space)
                tokens = sentence.split()

                # call actual parsing procedure:
                parse(grammar, tokens)
    else:
        tokens = "the elephant sneezed".split()
        parse(grammar, tokens)
        tokens = "my mouse giggled".split()
        parse(grammar, tokens)


if __name__ == "__main__":
    # Convert grammar into our internal dict format
    grammar = load_grammar(grammar_string)
    demo(grammar)
