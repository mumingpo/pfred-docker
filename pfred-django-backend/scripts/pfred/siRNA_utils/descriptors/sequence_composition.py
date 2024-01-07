import itertools
from .stdev_filter import stdev_filter

# -- sequence_composition constants

CODONS = ['A', 'C', 'G', 'U']
SUBSEQUENCES = \
    CODONS + \
    [''.join(combination) for combination in itertools.product(CODONS, CODONS)] + \
    [''.join(combination) for combination in itertools.product(CODONS, CODONS, CODONS)]

SUBSEQUENCE_INDEX_LOOKUP = dict()
for i, subseq in enumerate(SUBSEQUENCES):
    SUBSEQUENCE_INDEX_LOOKUP[subseq] = i

# -- sequence_composition

def sequence_composition(sequences: dict[str, str]):
    temp = dict()

    for key in sequences.keys():
        comp_string = [0] * len(SUBSEQUENCES)
        seq = sequences[key]

        if seq[-1] in 'acgut':
            # (from original) normally 3'-overhang are lowercase
            # so here we just removed the last two nucleotides
            seq = seq[:-2]
        
        for subseq_length in (1, 2, 3):
            for i in range(len(seq) + 1 - subseq_length):
                subseq = seq[i:i+subseq_length]
                comp_string[SUBSEQUENCE_INDEX_LOOKUP[subseq]] += 1
        
        temp[key] = comp_string
    
    comp_descriptors = stdev_filter(temp)
    comp_length = len(next(iter(comp_descriptors.values())))

    return comp_descriptors, comp_length
