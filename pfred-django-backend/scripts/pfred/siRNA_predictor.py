import logging
import sys

from load_dataset import novartis_data
from load_dataset import seq_to_predict
from siRNA_descriptors import reynolds_filter
from siRNA_descriptors import sequence_positions
from siRNA_descriptors import sequence_composition
from siRNA_descriptors import sequence_acc
from siRNA_descriptors import thermodynamic

logger = logging.getLogger("pfred.scripts.siRNA_predictor")

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
    reynolds_filter(sequences)
    sequence_positions(sequences)
    sequence_composition(sequences)
    sequence_acc(sequences)
    thermodynamic(sequences)


if __name__ == "__main__":
    main()
