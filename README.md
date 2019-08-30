# WordsAsMarkovChains

This repository provides two modules, one is to get words from text and other implements n'th order Markov chain.

It is easily noticable that the order of consonants and vowels in any language is important for pronunciation.
I have tried to explore this in a simple way- using the concept of Markov Chains.

Most commonly, a sequence of states is considered to be a Markov chain if the next state depends only on the current state and is independent of the previous states.
A sequence in this case is a word, i.e. a sequence of letters. The letters are the states. If we treat words as Markov chains then given a letter we can predict the next letter.
However, it is not diffucult to see that in words, presence of a letter might depend on more than one previous letters. For example the suffix 'ment' is very common in English. If you knew 'men' to be the three letters, you would be much more inclined to choose 't' as the next letter than if you knew only 'n'.
Therefore a generalization of the Markov chain is needed. A generalization can be made such that the next state depends on 'n' previous states. It is then called an n'th order Markov Chain.

This python code can generate new words based on the input corpus of words.

The testMarkovModel.py program uses TextToWords.py and MarkovModel.py and generates words of different lengths using Markov chain models of different orders. It then calculates the frequency of occurrence of generated words to occur in the input words (or training words).

Complexity of models (defined by the order parameter in this case) leads to the generation of input words more frequently. As one might expect, longer words from the input words are rarely generated.

It can also be noted that when model is trained with words of a specific lengths, then the frequency of generation of input words increases substantially, suggesting that the model is able to learn length-specific features of the words.

A sample output of testMarkovModel.py can be found in testMarkovModel.out.
