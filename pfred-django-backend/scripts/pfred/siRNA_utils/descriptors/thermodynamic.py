import itertools

import numpy as np

ENTHALPY = 0
ENTROPY = 1
GIBBS = 2
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
DG_3PRIME_DANGLING_U = {
    "AU": -0.6,
    "CU": -1.2,
    "GU": -0.6,
    "UU": -0.1,
}
COMPLEMENT_DICT = {
    'A': 'U',
    'U': 'A',
    'C': 'G',
    'G': 'C',
}
TOT_STRAND_CONCENTRATION_SELF = 0.0001 # M
TOT_STRAND_CONCENTRATION_NONSELF = 0.0002 # M

def get_duplet(s: str, i: int) -> str:
    "Return a duplet starting from string i"
    if (i < 0 or i >= len(s)):
        raise IndexError("Duplet index not in range.")
    
    return s[i:i+2]

def thermodynamic(sequences: dict[str, str]):
    thermo_descriptors = dict()

    for key in sequences.keys():
        seq = sequences[key]
        total_dHSG = np.zeros(shape=(3,), dtype=np.float64)

        if seq[-1] in "acgut":
            # (original) normally 3'-overhang are lowercase,
            # so here we just removed the last two nucleotides
            seq = seq[:-2]
    

        self_symmetric = True
        for i in range(len(seq) // 2 + 1):
            if seq[i] != COMPLEMENT_DICT[seq[-i - 1]]:
                self_symmetric = False
                break
        
        n_AU = 0
        test_AU = False
        as_AU_test = False
        ss_AU_test = False
        
        if (seq[0] in "AU"):
            n_AU += 1
            test_AU = True
            as_AU_test = True
        if (seq[-1] in "AU"):
            n_AU += 1
            test_AU = True
            ss_AU_test = True

        thermo_list = []
        temp_dHSG = []

        for i in range(len(seq) - 1):
            duplet = get_duplet(seq, i)

            dHSG = THERMOPARAMETER_SET[duplet]
            temp_dHSG.append(dHSG)

            total_dHSG += dHSG

        if (self_symmetric):
            dHSG_self = total_dHSG + THERMOPARAMETER_SET["Initiation"] + THERMOPARAMETER_SET["Symmetry_self"]
            if (test_AU):
                dHSG_self = n_AU * THERMOPARAMETER_SET["terminal_AU"]
            tm_self = (dHSG_self[ENTHALPY] * 1000) / (dHSG_self[ENTROPY] + (1.987 * np.log(TOT_STRAND_CONCENTRATION_SELF))) - 273.15

            thermo_list.extend(dHSG_self)
            thermo_list.append(tm_self)
        else:
            dHSG_nonself = total_dHSG + THERMOPARAMETER_SET["Initiation"] + THERMOPARAMETER_SET["Symmetry_nonSelf"]
            if (test_AU):
                dHSG_self = n_AU * THERMOPARAMETER_SET["terminal_AU"]
            tm_nonself = (dHSG_nonself[ENTHALPY] * 1000) / (dHSG_nonself[ENTROPY] + (1.987 * np.log(TOT_STRAND_CONCENTRATION_NONSELF / 4))) - 273.15

            thermo_list.extend(dHSG_nonself)
            thermo_list.append(tm_nonself)
            
        for i, j in itertools.product((-1, -2, -3), (0, 1, 2)):
            thermo_list.append(temp_dHSG[i][GIBBS] - temp_dHSG[j][GIBBS])
        thermo_list.append(sum([dHSG[GIBBS] for dHSG in temp_dHSG[-2:]]) - sum([dHSG[GIBBS] for dHSG in temp_dHSG[:2]]))
        thermo_list.append(sum([dHSG[GIBBS] for dHSG in temp_dHSG[-3:]]) - sum([dHSG[GIBBS] for dHSG in temp_dHSG[:3]]))
        thermo_list.append(temp_dHSG[-1][GIBBS] - temp_dHSG[9][GIBBS])
        thermo_list.append(temp_dHSG[0][GIBBS] - temp_dHSG[12][GIBBS])

        for dHSG in temp_dHSG:
            thermo_list.append(dHSG[GIBBS])
        

        
        LS_1_15 = [
            sum([THERMOPARAMETER_SET[get_duplet(seq, i + j)][GIBBS] for j in range(4)])
            for i in range(15)
        ]

        # # Like, why?
        # LS_16_19 = LS_1_15[-4:]

        if (as_AU_test):
            LS_1_15[0] += THERMOPARAMETER_SET["terminal_AU"][GIBBS]
        if (seq[0] in "ACGU"):
            LS_1_15[0] += DG_3PRIME_DANGLING_U["{}U".format(COMPLEMENT_DICT[seq[0]])]

        # unused
        # if (ss_AU_test):
        #     LS_16_19[-1] += THERMOPARAMETER_SET["terminal_AU"][GIBBS]
        # if (seq[-1] in "ACGU"):
        #     LS_16_19[-1] += DG_3PRIME_DANGLING_U["{}U".format(seq[-1])]

        thermo_list.append(sum(LS_1_15[8:14]) / 6)
        
        thermo_descriptors[key] = thermo_list

    thermo_length= len(thermo_descriptors[next(iter(thermo_descriptors.keys()))])

    return thermo_descriptors, thermo_length
