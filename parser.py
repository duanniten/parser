import nltk
import re
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP                    
S -> S Conj S                 
NP -> Det N                   
NP -> Det AdjP N              
NP -> N                       
NP -> NP PP                   
NP -> Pron                    
VP -> V                       
VP -> V NP                    
VP -> V NP PP                 
VP -> V PP                    
VP -> Adv VP                  
VP -> VP Conj VP              
AdjP -> Adj                   
AdjP -> Adj AdjP              
PP -> P NP                   
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    #filtering the data and make a list
    result = re.findall(r'\b\w*[a-zA-Z]+\w*\b', sentence)
    
    return [word.lower() for word in result]
    

def np_chunk(tree:nltk.Tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    np_chunks = []

    for subtree in tree.subtrees():
        # Verifica se o rótulo do subtree é 'NP'
        if subtree.label() == 'NP':
            # Verifica se não há NPs filhos dentro deste subtree
            contains_np = False
            for child in subtree:
                if isinstance(child, nltk.Tree) and child.label() == 'NP':
                    contains_np = True
                    break
            if not contains_np:
                np_chunks.append(subtree)

    return np_chunks

if __name__ == "__main__":
    main()
