
import numpy as np
import pandas as pd

from sklearn import svm
from sklearn import pipeline
from sklearn import preprocessing

# (original) first value is the intercept, remaining values are the 313 descriptor's coefficients
LV3_COEFFICIENTS = (63.63,0.5271,-5.398,-3.395,0,1.884,-0.3211,-0.6358,-1.15,2.34,0.5226,-1.227,-1.556,1.61,-1.489,1.421,-2.157,0,2.468,0,-1.727,0,-3.201,-0.3761,2.883,-1.702,-1.356,0,2.215,0,-1.814,0,1.442,-2.619,3.076,1.603,-2.082,2.797,-2.666,-1.023,0,0,0.2344,2.781,-2.123,-1.777,-1.106,0.05582,2.422,0,0,1.354,-1.196,3.741,-4.291,0,0.1678,-3.848,3.794,0.7811,0,1.322,0,-0.629,0.729,0,0,-1.015,0,-0.8461,2.267,-1.624,-0.6412,-5.065,2.074,-4.133,4.747,1.032,4.006,-3.841,-0.9858,0,0,0,2.823,-0.05147,0.1729,-0.11,-0.09794,0.055,-0.0421,0.5175,0.7696,0.0006497,-0.2065,-0.8756,0.1386,0.1913,0.5242,-0.6247,-0.224,0.5665,0.3697,0.5626,-0.764,-0.4865,-0.03976,-0.6843,1.539,-0.7842,-1.046,-3.407,3.421,3.687,0,1.745,1.621,1.06,0.2596,0.7939,0.1448,-1.677,-0.1947,0.2598,-0.6906,-0.1139,-1.01,-0.7949,-1.058,-1.857,2.827,-0.5307,-0.8922,0.4929,-2.242,-0.00786,0,-0.2106,0.8451,0,0.4082,2.496,0.4999,2.34,-6.114,-1.656,1.83,-3.881,0,0.8127,0.2629,-1.072,-0.7517,2.689,-1.409,7.272,0.746,-1.708,1.223,-1.321,2.664,-0.2414,0.3553,-1.39,-1.663,0,-0.3207,1.381,-1.548,-1.383,0,-2.447,-7.108,-0.8358,-0.2735,3.246,4.215,1.234,-2.646,0.01932,-6.069,0,-7.22,-2.693,0.5493,3.189,-0.9048,0,10.36,0,-1.943,0,-1.527,0,0,0,0,5.497,0,-1.088,-0.9825,-3.075,0,-2.899,0,-1.098,0,2.483,-3.626,5.56,3.85,-3.892,3.094,0,-0.9136,5.246,2.571,0.9065,1.093,2.135,1.349,1.75,0,1.715,2.617,1.637,0,4.374,4.793,0,0,3.571,0,-2.331,3.625,-2.996,0,0,-2.871,3.572,2.604,0,0,-5.943,3.314,-1.887,-1.518,-2.124,0,-3.589,-2.524,-1.006,0,0,-4.316,-5.065,0,4.195,0,0,0.9646,2.063,2.803,0,-1.421,0,0,4.286,0,2.854,0,-0.8618,1.569,-0.8474,0,0,0,0,0.01875,0.006392,0.08018,-0.04263,-0.4131,-0.1849,-0.364,-0.5908,-0.3863,-0.5638,0.2958,0.4941,0.3497,-0.2772,-0.09434,-0.08914,-0.6914,0.7254,0.2053,0.585,-1.34,0.7788,1.825,0.6545,-1.79,-0.7297,-0.003391,-0.7586,0.84,1.81,-0.3274,-0.8272,1.146,-0.5551,-0.1966,0.2549)

def svm_regression(train, test, activity_dict, output_type):
    """
    """

    if output_type == 'build':
        raise NotImplementedError()

    train_df = pd.read_csv(train)
    # train_keys = train_df.index
    train_x = train_df[train_df.columns[:-1]]
    train_y = train_df[train_df.columns[-1]]

    test_df = pd.read_csv(test)
    test_keys = test_df.index
    test_x = test_df[test_df.columns[:-1]]
    # test_y = test_df[test_df[-1]]

    results = dict()

    # original code scales data into svm, which is not per default in sklearn
    # so we have to build explicit scaler
    regr = pipeline.make_pipeline(
        preprocessing.StandardScaler(),
        # original code use default r svm, which uses radial basis
        # so we cannot use linearSVR here
        svm.SVR(
            # r default does not use variance
            gamma='auto',
            # defaults
            # kernel='rbf',
            # degree=3,
            # tol=0.001,
            # C=1.0,
            # shrinking=True,
        ),
    )
    
    regr.fit(train_x, train_y)
    test_y_pred = regr.predict(test_x)

    for key, pred in zip(test_keys, test_y_pred):
        results[key] = pred

    return results


def pls_regression_varSelection_extValidation(TESTpls):
    """
    """
    pls_regression_varSelection_results = dict()
    
    with open(TESTpls,"r") as test_set_file:
        # presumably to skip header?
        test_set_file.readline()

        for line in test_set_file:
            tokens = line.strip().split(",")

            key = tokens[0]
            # 1 for intercept
            features = np.array([1] + list(map(lambda x: float(x), tokens[1:-1])))
            y_pred = LV3_COEFFICIENTS @ features

            pls_regression_varSelection_results[key] = y_pred

    return pls_regression_varSelection_results
