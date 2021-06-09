from as_5 import *
from data import grammar, sentences

import matplotlib.pyplot as plt
import numpy as np


def run_batch():
    num_tokens = np.zeros(len(sentences))
    num_steps = np.zeros(len(sentences))

    # load grammer
    G = load_grammar(grammar=grammar)
    for idx, sentence in enumerate(sentences):
        tokens = sentence.split(" ")
        parser_steps = bottom_up_parse(G=G, tokens=tokens)

        num_tokens[idx] = len(tokens)
        num_steps[idx] = parser_steps

    # plot
    plt.plot(num_tokens, num_steps)
    plt.xlabel("Number of tokens")
    plt.ylabel("Number of steps")
    plt.show()


run_batch()
