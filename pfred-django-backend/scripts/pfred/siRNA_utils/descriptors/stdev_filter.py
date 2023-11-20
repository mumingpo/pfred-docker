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
