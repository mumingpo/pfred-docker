import itertools
from collections import Counter

from .stdev_filter import stdev_filter

def sequence_positions(sequences: dict[str, str]):
    unabridged_descriptors = dict()

    for key in sequences.keys():
        seq = sequences[key].upper()
        length_seq = len(seq) * 4
        seq_string = [0] * length_seq
        gc_count = 0

        # convert sequence to side-by-side one-hot representation: why?
        offsets = {
            'A': 0,
            'C': 1,
            'G': 2,
            'U': 3,
            'T': 3,
        }

        for i, codon in enumerate(seq):
            seq_string[4 * i + offsets[codon]] = 1

        # calculating gc content before lst 2 codons again
        num_codons = Counter(seq[:-2])

        gc_count = num_codons.get('C', 0) + num_codons.get('G', 0)
        gc_content = gc_count / 19 * 100
        
        # WHY??????
        seq_string.append(gc_content)

        unabridged_descriptors[key] = seq_string

    seq_descriptors = stdev_filter(unabridged_descriptors)
    seq_length = len(next(iter(seq_descriptors.values())))

    return seq_descriptors, seq_length

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
