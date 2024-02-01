from .stdev_filter import stdev_filter

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

        index_offsets_leading = (0, 1, 2, 0, 0, 1, 1, 2, 2)
        index_offsets_lagging = (0, 1, 2, 1, 2, 0, 2, 0, 1)

        temp_list = []

        for lag_dist in range(1, MAX_LAG):
            normalization = 1 / (len(seq) - lag_dist)
            temp_sum = [0.] * 9
            for i in range(len(seq) - lag_dist):
                leading = 3 * i
                lagging = 3 * (i + lag_dist)
                for k, (leading_offset, lagging_offset) in enumerate(zip(index_offsets_leading, index_offsets_lagging)):
                    temp_sum[k] += modify_seq[leading + leading_offset] * modify_seq[lagging + lagging_offset] * normalization
            temp_list.extend(temp_sum)
        
        temp[key] = temp_list
    
    acc_descriptors = stdev_filter(temp)
    acc_descriptors_length = len(next(iter(acc_descriptors.values())))

    return acc_descriptors, acc_descriptors_length
