# top_down_skeleton.py
# Jonas Kuhn, University of Stuttgart, 2021
# course "Parsing"

# enables input history in interactive mode
import readline

# Boolean variable for switching tracing info on and off
trace = True  # set this to False if you don't want to see intermediate steps

# Boolean variable for running parser interactively on user input or on pre-specified input
interactive = False  # False

# internal format of cfg production rules with reversed right-hand sides (!)
grammar = {'S': [['VP', 'NP']],
           'NP': [['N', 'DET']],
           'VP': [['V']], 'DET': [['the'], ['an'], ['my'], ['most']],
           'N': [['elephant'], ['elephants'], ['mouse'], ['mice']],
           'V': [['sneezed'], ['giggled'], ['trumpeted']]}

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


# main procedure:
def parse(grammar, tokens):
    # grammar:  dict with list of reversed rhs's for each non-terminal
    # tokens:   list of input tokens

    if trace:
        print("parsing ", tokens, "...")

    # initialize data structures:
    stack = ["S"]  # -> S is the start symbol
    inbuffer = tokens  # -> buffer is the tokens from the input string

    # main loop:
    while len(inbuffer) > 0:
        if trace:
            print("           {:<40}{:>40}".format(str(stack), str(inbuffer)))

        # expand
        #
        # -> look for the symbol at the top of the stack in the grammar
        stack_top = stack[-1]
        # -> don't match with input!
        if stack_top in grammar and stack_top != inbuffer[0]:
            # ->
            if trace:
                print(f" >expand:\t{stack_top}\t->\t{grammar[stack_top][0]}")

            # -> pop
            stack.pop()

            # add the expanded symbols in stack
            stack.extend(grammar[stack_top][0])
            # inbuffer = TBD

        # match
        # stack_top matches with input symbol, consume
        elif stack_top == inbuffer[0]:
            if trace:
                print(f" >match:\t{stack_top}\t->\t{inbuffer[0]}")

            # pop from stack and inbuffer
            stack.pop()
            inbuffer = inbuffer[1:]

        # no match:
        else:
            if trace:
                print(" >dead end!")
            break

    if trace:
        print("           {:<40}{:>40}".format(str(stack), str(inbuffer)))

    # termination
    if len(stack) == 0 and len(inbuffer) == 0:
        print("success!")
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
            # user can input the string to be parsed
            sentence = input('Type sentence ("q" to quit): ')
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
        # tokens = "my mouse giggled".split()
        # parse(grammar, tokens)


if __name__ == "__main__":
    # Later we will take the grammar in some other format, so we will have
    # to convert it to our internal dict format:
    # grammar = load_grammar(grammar_string)
    demo(grammar)
