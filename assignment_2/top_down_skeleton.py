# top_down_skeleton.py
# Jonas Kuhn, University of Stuttgart, 2021
# course "Parsing"

# enables input history in interactive mode
import readline

# Boolean variable for switching tracing info on and off
trace = True  # set this to False if you don't want to see intermediate steps

# Boolean variable for running parser interactively on user input or on pre-specified input
interactive = True  # False

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
    stack = TBD
    inbuffer = TBD

    # main loop:
    while inbuffer:
        if trace:
            print("           {:<40}{:>40}".format(str(stack), str(inbuffer)))

        # expand
        if TBD:
            TBD
            if trace:
                print(" >expand: ")

            stack = TBD
            inbuffer = TBD

        # match
        elif TBD:
            if trace:
                print(" >match:  ")
            stack = TBD
            inbuffer = TBD

        # no match:
        else:
            if trace:
                print(" >dead end!")
            break

    if trace:
        print("           {:<40}{:>40}".format(str(stack), str(inbuffer)))

    # termination
    if TBD:
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
        tokens = "my mouse giggled".split()
        parse(grammar, tokens)


if __name__ == "__main__":
    # Later we will take the grammar in some other format, so we will have
    # to convert it to our internal dict format:
    # grammar = load_grammar(grammar_string)
    demo(grammar)
