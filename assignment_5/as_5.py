# top_down_solution.py
# Jonas Kuhn, University of Stuttgart, 2021
# course "Parsing"

# enables input history in interactive mode
# import readline

import copy
from nltk import CFG, Tree

# Boolean variable for switching tracing info on and off
trace = True  # set this to False if you don't want to see intermediate steps

# Boolean variable for running parser interactively on user input or on pre-specified input
# interactive = True  # False
interactive = False

log_action = True

lr_grammar = """
S -> NP VP 
NP -> NP N |DET N | DET N PP | 'I'
VP -> V | V NP | V NP PP
PP -> P NP 
DET -> 'the' | 'an' | 'my' | 'most'
P -> 'in'
N -> 'elephant' | 'elephants' | 'mouse' | 'mice' | 'pajamas' | 'fish' | 'factory' | 'worker'
V -> 'sneezed' | 'giggled' | 'trumpeted' | 'saw' | 'shot'
"""

# Additional grammars used in Assignment 03
grammar_string2 = """
S    -> '(' S Op S ')' | Num
Num  -> Sign Num | '1'|'2'|'3'|'4'|'5'|'6'|'7'|'8'|'9'|'0'
Op   -> '+' | '-' | '*' | '/'
Sign -> '-'
"""

# load this for exercise 4.1
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
def load_grammar(grammar):
    G = {}
    cfg = CFG.fromstring(grammar)
    for p in cfg.productions():
        p = p.__str__().split()
        for i in range(len(p)):
            p[i] = p[i].strip("'")
        left = p[2:]
        production = tuple(left)
        G.setdefault(production, [])
        G[production].append(p[0])
    return G


def bottom_up_parse(G, tokens):
    step_counter = 0
    if trace:
        print("parsing ", tokens, "...")

    # initialize agenda:
    agenda = [([], tokens, [])]
    # initalize list for collecting complete solutions:
    parses = []

    # main loop:
    while len(agenda) > 0:
        (stack, inbuffer, deriv) = agenda.pop()

        # accept
        if stack == ['S'] and inbuffer == []:
            print(" >accept!")
            parses += [deriv]

        elif stack == ['S'] and len(inbuffer) > 0:
            if log_action:
                print(" >backtracking (stack or buffer was empty)")
            # again: we need to do nothing; next agenda item will be considered

        else:
            step_counter += 1
            # shift
            if len(inbuffer) > 0:
                if trace:
                    print('           {:<40}{:>40}'.format(str(stack), str(inbuffer)))
                if log_action:
                    print(" >shift:  ", inbuffer[0])
                stack_temp = stack + [inbuffer[0]]
                if stack_temp != []:
                    deriv_temp = deriv + [(0, stack_temp[-1])]
                else:
                    deriv_temp = list(deriv)
                inbuffer_temp = inbuffer[1:]
                agenda += [(stack_temp, inbuffer_temp, deriv_temp)]

            # reduce
            for i in range(0, len(stack)):
                if tuple(stack[i:len(stack)]) in G:
                    if trace:
                        print('           {:<40}{:>40}'.format(str(stack), str(inbuffer)))
                    if log_action:
                        print(" >reduce: ", stack[i:len(stack)], " -R-> ", G[tuple(stack[i:len(stack)])])

                    deriv_temp = deriv + [(len(stack[i:len(stack)]), G[tuple(stack[i:len(stack)])])]

                    stack_temp = stack[0:i] + G[tuple(stack[i:len(stack)])]
                    inbuffer_temp = list(inbuffer)
                    agenda += [(stack_temp, inbuffer_temp, deriv_temp)]

    if trace:
        print(len(parses), ' solutions')

    sol = 0
    for deriv in parses:
        sol += 1
        print("solution ", sol)
        print(deriv)
    print(f"total solutions : {sol}")

    return step_counter


def demo(grammar, test_sentences=[]):
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
                bottom_up_parse(grammar, tokens)
    else:
        for test_sentence in test_sentences:
            tokens = test_sentence.split(" ")
            result = bottom_up_parse(grammar, tokens)
            # build_tree(result)


if __name__ == "__main__":
    # Convert grammar into our internal dict format
    # grammar = load_grammar(grammar_string3)
    grammar = load_grammar(lr_grammar)

    test_sentences = [
        "I shot an elephant in my pajamas",
        # "the elephant sneezed",
        # "my mouse giggled"
    ]

    demo(grammar, test_sentences)
