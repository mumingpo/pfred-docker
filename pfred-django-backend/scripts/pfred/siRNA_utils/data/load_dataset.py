# import os
from collections import defaultdict

COLUMN_INDEX_TO_FIELD_NAME = {
    # 0: "key",
    # 1: "sequence",
    2: "training_all",
    3: "training_all_human",
    4: "training_human_e2s",
    5: "training_rodent",
    6: "training_random_1",
    7: "training_random_2",
    8: "training_random_3",
    9: "training_random_4",
    10: "testing_all",
    11: "testing_all_human",
    12: "testing_human_e2s",
    13: "testing_rodent",
    # 14: "activity",
}

def novartis_data(filepath: str) -> dict[str, dict[str, str]]:
    """
    Parse sequence activity data from csv file.

    Keyword arguments:
    filepath: path to novartis_data.csv to be parsed

    Return:
    defaultdict object containing the data parsed
    """
    data = defaultdict(lambda: dict())
    sequences = data["sequences"]
    activity = data["activity"]
    activity_class = data["activity_class"]

    # print(os.path.abspath(filepath))

    with open(filepath, "rt") as f:
        # header unused, skipping first line
        f.readline()

        for line in f:
            fields = line.strip().split(',')
            key = fields[0]

            sequences[key] = fields[1]
            activity[key] = fields[14]

            if (float(fields[14])) >= 0.7:
                activity_class[key] = '1'
            else:
                activity_class[key] = '0'

            for i in range(2, len(fields) - 1):
                if (fields[i] == 'X'):
                    field_name = COLUMN_INDEX_TO_FIELD_NAME[i]
                    data[field_name][key] = fields[14]

    return data

def seq_to_predict(filepath: str, data: dict[str, dict[str, str]]) -> (dict[str, dict[str, str]], list[str], list[str]):
    """
    Tally the sequences to predict and update activity of sequences in novartis data
    according to the values in sequence data csv file.

    Keyword arguments:
    filepath: path to the sequence_data.csv to be parsed
    data: a novartis dataset

    Return:
    data: a modified copy of the novartis dataset
    sequence_names: names of sequences contained in the sequence_data.csv
    activity_to_predict_tags: I have no idea what this is supposed to represent
    """

    # work on a copy instead of the original
    data = defaultdict(lambda: dict(), { key: value.copy() for key, value in data.items() })

    sequences = data["sequences"]
    activity = data["activity"]
    activity_class = data["activity_class"]

    sequence_names = []

    with open(filepath, "rt") as f:
        header = f.readline().strip().split(',')

        if (len(header) > 2):
            # activity reported in sequence data?
            activity_to_predict_tags = ['0', '1']

            for line in f:
                fields = line.strip().split(',')
                key = fields[1]
                sequence_names.append(key)
                sequences[key] = fields[0]
                activity[key] = fields[2]
                activity_class[key] = fields[2]

        else:
            # activity not reported in sequence data?
            activity_to_predict_tags = ['0',]

            for line in f:
                fields = line.strip().split(',')
                key = fields[1]
                sequence_names.append(key)
                sequences[key] = fields[0]
                activity[key] = "0.000"
                activity_class[key] = "0.000"

    return data, sequence_names, activity_to_predict_tags
