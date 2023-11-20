# import re
import itertools
from collections import Counter

import numpy as np

# FIXME: AFAIK, this just drop columns where values are the same
# but I am just abiding to the original implementation in case
# I'm missing something
def stdev_filter(raw_dict: dict[str, list[float]]):
    new_dict = dict()
    # raw dict: n keys with arrays of length k
    # dim=(n,)
    keys = list(raw_dict.keys())
    # dim=(n, k)
    array = np.array([raw_dict[key] for key in keys])
    # dim=(k,)
    std = array.std(axis=0)
    columns_to_remove = (std <= 0)
    new_array = array[:, ~columns_to_remove]
    
    for i, key in enumerate(keys):
        new_dict[key] = list(new_array[i])

    return new_dict

def reynolds_filter(sequences: dict[str, str]):
    stretches = dict()
    reynolds_score = dict()
    reynolds_descriptors = dict()

    for key in sequences.keys():
        seq = sequences[key]
        
        # quintuple codons
        # FIXME: the variable names in the original script indicates that
        # they are looking for counts. However, the way it is implemented lets
        # it return 1 when found and 0 when not found.
        # original implementation is used here, while "correct" implementation is
        # provided below in comments for reference
        AAAAA_count = int("AAAAA" in seq)
        CCCCC_count = int("CCCCC" in seq)
        GGGGG_count = int("GGGGG" in seq)
        UUUUU_count = int("UUUUU" in seq)

        # "correct" implementation: find number of A with 4 succeeding As
        # AAAAA_count = len(re.findall('A(?=A{4})', seq))
        # CCCCC_count = len(re.findall('C(?=C{4})', seq))
        # GGGGG_count = len(re.findall('G(?=G{4})', seq))
        # UUUUU_count = len(re.findall('U(?=U{4})', seq))

        stretches[key] = (AAAAA_count, CCCCC_count, GGGGG_count, UUUUU_count)

        # num of G and C codons before the last 2 codons
        gc_count = 0
        gc_score = 0

        num_codons = Counter(seq[:-2].upper())

        gc_count = num_codons.get('C', 0) + num_codons.get('G', 0)
        gc_content = gc_count / 19 * 100

        if (gc_content >= 30 and gc_content <= 52):
            gc_score += 1

        # num of A and U codons in the first 5 codons
        num_codons = Counter(seq[:5].upper())
        au_count = num_codons.get('A', 0) + num_codons.get('U', 0)

        tm_score = 0

        u_p1 = int(seq[0].upper() == 'U')
        u_p17 = int(seq[16].upper() == 'U')
        a_p10 = int(seq[9].upper() == 'A')
        gc_p1 = int(seq[0].upper() in "CG")
        # FIXME: judging from the variable name,
        # shouldn't it include 'G' as well?
        gc_p7 = int(seq[6].upper() == 'C')

        seq_string = [
            gc_content,
            au_count,
            tm_score,
            u_p1,
            u_p17,
            a_p10,
            gc_p1,
            gc_p7,
        ]

        r_score = gc_score + tm_score + u_p1 + u_p17 + a_p10 + au_count - gc_p1 - gc_p7
        reynolds_score[key] = (r_score, gc_content, gc_score)
        reynolds_descriptors[key] = seq_string
    
    return reynolds_score, reynolds_descriptors, stretches

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

# -- sequence_acc constants
basis_set = {
    "A" : (-1, -1, +1),
    "C" : (+1, -1, -1),
    "G" : (-1, +1, -1),
    "T" : (+1, +1, +1),
    "U" : (+1, +1, +1),
}
MAX_LAG = 13

def sequence_acc(sequences: dict[str, str]):
    temp = dict()

    for key in sequences.keys():
        seq = sequences[key]
        modify_seq = []

        for i in seq.upper():
            modify_seq.extend(basis_set[i])

        modify_seq = np.array(modify_seq)

        index_offsets_leading = (0, 1, 2, 0, 0, 1, 1, 2, 2)
        index_offsets_lagging = (0, 1, 2, 1, 2, 0, 2, 0, 1)

        temp_list = []

        for lag_dist in range(1, MAX_LAG):
            normalization = 1 / (len(seq) - lag_dist)
            for i in range(len(seq) - lag_dist):
                leading = 3 * i
                lagging = 3 * (i + lag_dist)
                for leading_offset, lagging_offset in zip(index_offsets_leading, index_offsets_lagging):
                    temp_list.append(modify_seq[leading + leading_offset] * modify_seq[lagging + lagging_offset] * normalization)
        
        temp[key] = temp_list
    
    acc_descriptors = stdev_filter(temp)
    acc_descriptors_length = len(next(iter(acc_descriptors.values())))

    return acc_descriptors, acc_descriptors_length

# -- thermodynamic constants
THERMOPARAMETER_SET = {
    "AA":(-6.82,-19.00,-0.93),
    "AU":(-9.38,-26.70,-1.10),
    "UA":(-7.69,-20.50,-1.33),
    "CA":(-10.44,-26.90,-2.11),
    "CU":(-10.48,-27.10,-2.08),
    "GA":(-12.44,-32.50,-2.35),
    "GU":(-11.40,-29.50,-2.24),
    "CG":(-10.64,-26.70,-2.36),
    "GC":(-14.88,-36.90,-3.42),
    "GG":(-13.39,-32.70,-3.26),
    "UU":(-6.82,-19.00,-0.93),
    "UG":(-10.44,-26.90,-2.11),
    "AG":(-10.48,-27.10,-2.08),
    "UC":(-12.44,-32.50,-2.35),
    "AC":(-11.40,-29.50,-2.24),
    "CC":(-13.39,-32.70,-3.26),
    "terminal_AU":(3.72,10.5,0.45),
    "Initiation":(3.61,-1.50,4.09),
    "Symmetry_self":(0.00,-1.40,0.43),
    "Symmetry_nonSelf":(0.00,0.00,0.00),
}
DG_3PRIME_DANGLING_U = {"AU":-0.6,"CU":-1.2,"GU":-0.6,"UU":-0.1}

def thermodynamic(sequences: dict[str, str]):
    for key in sequences.keys():
        seq = sequences[key]
        if seq[-1] in 'acgut':
            # (original) normally 3'-overhang are lowercase,
            # so here we just removed the last two nucleotides
            seq = seq[:-2]
    
        complement_dict = {
            'A': 'U',
            'U': 'A',
            'C': 'G',
            'G': 'C',
        }

        palindrome = True
        for i in range(len(seq) / 2):
            if seq[i] != seq[-i - 1]:
                palindrome = False
                break
        
        n
