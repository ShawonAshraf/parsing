# task1.py
# Jonas Kuhn, University of Stuttgart, 2021
# course "Parsing"

# enables input history in interactive mode
import readline

# CFG
from nltk import CFG, Tree

# Boolean variable for switching tracing info on and off
trace = True  # set this to False if you don't want to see intermediate steps

# Boolean variable for running parser interactively on user input or on pre-specified input
interactive = False  # False

# string format used in nltk.CFG class:
# our test grammar:
grammar_string = """
S    -> '(' S Op S ')' | Num
Num  -> Sign Num | '1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'0'
Op   -> '+' | '-' | '*' | '/'
Sign -> '-'
"""


# calculate FIRST
def calculate_first_sets(G):
    non_terminals = list(G.keys())
    first = dict()

    for nt in non_terminals:
        production_choices = G[nt]

        # pick the first production choice
        if nt in first.keys():
            first[nt].append(production_choices[0])
        else:
            first[nt] = production_choices[0]

    return first

# recursive tree builder
def build_tree(derivation):
    if len(derivation) > 0:
        (arity, non_terminal) = derivation[0]

        subtrees = []
        d = derivation[1:]
        for i in range(arity):
            (subtree_i, d) = build_tree(d)
            subtrees = subtrees + [subtree_i]
        return Tree(non_terminal, subtrees), d
    else:
        result = list(derivation)
        return [], result


# load grammar from nltk format string
def load_grammar(grammar_str):
    cfg = CFG.fromstring(grammar_str)
    grammar = {}

    for production in cfg.productions():
        production_str = str(production)

        lhs, rhs = production_str.split("->")
        lhs = lhs.strip()
        rhs = rhs.strip()

        # split
        rhs = rhs.split(" ")
        # reverse rhs
        rhs = rhs[::-1]

        # remove '' from terminals
        for i in range(len(rhs)):
            rhs[i] = rhs[i].replace("'", "")

        # lhs -> list(rhs) mapping
        # check in lhs is in keys
        if lhs in grammar.keys():
            grammar[lhs].append(rhs)
        else:
            grammar[lhs] = [rhs]

    return grammar


# main procedure:
def parse(grammar, first, tokens):
    # grammar:  dict with list of reversed rhs's for each non-terminal
    # tokens:   list of input tokens

    if trace:
        print("parsing ", tokens, "...")

    # initialize data structures:
    # stack, tokens/inputs, derivation
    tape = [(["S"], tokens, [])]  # -> S is the start symbol in stack
    inbuffer = tokens  # -> buffer is the tokens from the input string

    solns = []
    counter = 0

    # main loop:
    while len(tape) > 0:
        # take from tape
        stack, inbuffer, derivation_buffer = tape.pop()
        counter += 1
        d = list(derivation_buffer)

        if trace:
            print("           {:<40}{:>40}".format(str(stack), str(inbuffer)))

        if len(stack) > 0 and len(stack) > 0:
            # expand
            if stack[-1] in grammar:
                # backtrack, pick the non terminal on top, add all possible RHS to tape
                non_terminal = stack.pop()
                for prod in grammar[non_terminal]:
                    if trace: print(" >expand:\t", non_terminal, "\t", "->\t", prod)
                    d1 = d + [(len(prod), non_terminal)]
                    stack1 = stack + prod
                    tape += [(stack1, inbuffer, d1)]
            # match
            elif stack[-1] == inbuffer[0]:
                if trace:
                    print(" >match:\t", stack[-1])
                d1 += [(0, stack[-1])]
                tape += [(stack[:-1], inbuffer[1:], d1)]

                # no match:
            else:
                if trace:
                    print(" >backtracking (no match for terminal)")

        # termination condition (inbuffer == []:)
        elif stack == [] and inbuffer == []:
            print(" >success!")
            solns += [d1]

        else:
            if trace:
                print(" >backtracking (stack or buffer was empty)")

    if trace:
        print(f"{len(solns)} -> solutions for parsing")

    return counter, len(solns)


def demo(grammar):
    # show internal representation of grammar
    if trace:
        print("Internal grammar representation:\n", grammar)
        print("----------------------------------------------------------------\n")

    # interactive way of running the parser in user input
    if interactive:
        while True:
            # user can input the string to be parsed
            sentence = input('Type sentence ("q" to quit): ')
            if sentence == "q":
                break
            else:
                # split up string in tokens (using the default separator, i.e. space)
                tokens = sentence.split()
                firsts = calculate_first_sets(grammar)

                # call actual parsing procedure:
                parse(grammar, firsts, tokens)
    else:
        tokens = "( - 4 * ( 2 + 3 )".split()
        firsts = calculate_first_sets(grammar)
        parse(grammar, firsts, tokens)
        # print(firsts)


if __name__ == "__main__":
    # Later we will take the grammar in some other format, so we will have
    # to convert it to our internal dict format:
    grammar = load_grammar(grammar_string)
    demo(grammar)
