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
