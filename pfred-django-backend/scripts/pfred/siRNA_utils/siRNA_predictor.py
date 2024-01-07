import logging
import sys
import os

from .data.load_dataset import novartis_data
from .data.load_dataset import seq_to_predict

from .descriptors.reynolds_filter import reynolds_filter
from .descriptors.sequence_positions import sequence_positions
from .descriptors.sequence_composition import sequence_composition
from .descriptors.sequence_acc import sequence_acc
from .descriptors.thermodynamic import thermodynamic

from .siRNA_stats import svm_regression
from .siRNA_stats import pls_regression_varSelection_extValidation

logger = logging.getLogger("pfred.scripts.siRNA_predictor")

OUTPUT_COLUMN_NAMES = \
    ["siRNA_id", "guide_strand_seq"] + \
    ["SVMpred","PLS_InHouse"] + \
    ["AAAAA", "CCCCC", "GGGGG", "UUUUU", "G:C_content"] + \
    ["Reynolds_rule1", "Reynolds_rule2", "Reynolds_rule3", "Reynolds_rule4", "Reynolds_rule5", "Reynolds_rule6", "Reynolds_rule7", "Reynolds_rule8", "ReynoldsScore"] + \
    ["dH", "dS", "dG", "Tm"] + \
    ["AIS"] + \
    ["ddG_18_1", "ddG_18_10", "ddG_1_13"] + \
    ["dG1","dG2","dG3","dG4","dG5","dG6","dG7","dG8","dG9","dG10","dG11","dG12","dG13","dG14","dG15","dG16","dG17","dG18"]

THERMO_DESCRIPTORS_INDEX_ORDER = list(range(4)) + [35, 4] + list(range(15, 35))

def main():
    try:
        assert sys.argv[1] == "novartis"
        novartis_data_file_path = sys.argv[2]
        assert sys.argv[3] == "p_c_a_thermo"
        assert sys.argv[4] == "predict"
        sequences_data_file_path = sys.argv[5]
    except AssertionError as e:
        raise NotImplementedError("Feature not refactored.") from e
    
    data = novartis_data(novartis_data_file_path)
    data, sequence_names, activity_to_predict_tags = seq_to_predict(sequences_data_file_path, data)

    sequences = data['sequences']
    activity = data['activity']
    # activity_class = data['activity_class']
    
    reynolds_score, reynolds_descriptors, stretches = reynolds_filter(sequences)
    seq_descriptors, seq_length = sequence_positions(sequences)
    comp_descriptors, comp_length = sequence_composition(sequences)
    acc_descriptors, acc_descriptors_length = sequence_acc(sequences)
    thermo_descriptors, thermo_length = thermodynamic(sequences)

    p_c_a_thermo_merged = { key: (seq_descriptors[key] + comp_descriptors[key] + acc_descriptors[key] + thermo_descriptors[key]) for key in sequences.keys() }
    length_descriptors = seq_length + comp_length + acc_descriptors_length + thermo_length

    files_to_write = (
        ("train_{}vars.csv", sequences.keys(), activity),
        ("PredictionTest_{}vars.csv", sequence_names, activity),
        # ("class_train_{}vars.csv", sequences.keys(), activity_class),
        # ("class_PredictionTest_{}vars.csv", sequence_names, activity_class),
    )

    for fname, keys, activity_to_use in files_to_write:
        with open(fname.format(length_descriptors), 'w') as f:
            column_names = ['var.{}'.format(n+1) for n in range(length_descriptors)] + ['activity']
            line = ','.join(column_names)
            f.write(line)
            f.write('\n')

            for key in keys:
                fields = [key] + p_c_a_thermo_merged[key] + [activity_to_use[key]]
                line = ','.join(map(str, fields))
                f.write(line)
                f.write('\n')

    # run_stats("4","regression")
    # run_stats("8","regression")
    csv_file = "train_{}vars.csv".format(length_descriptors)
    csv_file_ext = "PredictionTest_{}vars.csv".format(length_descriptors)
    with open(csv_file_ext, 'r') as f_in:
        header = f_in.readline().strip().split(',')

        names = []
        descriptors = dict()
        act = dict()

        for line in f_in:
            tokens = line.strip().split(',')
            key = tokens[0]
            names.append(key)
            # (original) exp value is not known
            act[key] = "0.00"
            descriptors[key] = tokens[1:-1]
    
    # mode == "4":
    # svm_regression(train,ext_pred_file,act,"predict")
    # FIXME: act is unused
    svm_results = svm_regression(csv_file, csv_file_ext, act, 'predict')

    # mode == "8":
    # pls_regression_varSelection_extValidation(csv_file_ext)
    pls_results = pls_regression_varSelection_extValidation(csv_file_ext)

    # siRNAActivityModel.sh script only consider the result of OuTpUt_ReSuLtS.csv
    # so I assume len(activity2predict_TAG) == 1 is always the case.
    # FIXME: grow up, whoever wrote the original code
    output_fname = "OuTpUt_ReSuLtS.csv" # I hate it
    
    with open(output_fname, 'w') as f:
        f.write(','.join(OUTPUT_COLUMN_NAMES))
        f.write('\n')
        for key in svm_results.keys():
            fields = list()
            
            fields.extend([key, sequences[key]])
            fields.extend([svm_results[key], pls_results[key]])
            fields.extend(stretches[key][:4])
            fields.extend(reynolds_score[key][1:3])
            fields.extend(reynolds_descriptors[key][1:8])
            fields.append(reynolds_score[key][0])
            fields.extend([thermo_descriptors[key][i] for i in THERMO_DESCRIPTORS_INDEX_ORDER])

            f.write(','.join(map(str, fields)))
            f.write('\n')

    # os.system("rm -f train_*vars.csv test_*vars.csv PredictionTest_*vars.csv class_train_*vars.csv class_test_*vars.csv class_PredictionTest_*vars.csv")
    os.remove(csv_file)
    os.remove(csv_file_ext)

if __name__ == "__main__":
    main()
