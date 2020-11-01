# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 10:59:17 2020

@author: alborsa1
"""
# %% Import Libraries
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn import preprocessing
import sklearn.metrics as metrics


# %% Function for Features Engineering

# -----------------------------------------------------------------------------
# Function for getting mapping from Encoding function
def get_integer_mapping(le):
    '''
    Return a dict mapping labels to their integer values
    from an SKlearn LabelEncoder
    le = a fitted SKlearn LabelEncoder
    '''
    res = {}
    for cl in le.classes_:
        res.update({cl: le.transform([cl])[0]})

    return res


def Encode_fields(PandasDF, fields):
    '''
    Return the dataframe with the fields encoded and the mapping infos
        INPUT:
            - PandasDF  : Dataframe
            - fields    : List of fields
    '''
    Mapping = []
    for field in fields:
        print("Encoding.. :", field)
        TempDF = PandasDF.loc[:, field].copy()
        TempDF.loc[TempDF.isnull() == True] = '-99'
        Encoder = preprocessing.LabelEncoder()
        Fitted_Encoder = Encoder.fit(TempDF)
        Encoded_label = Fitted_Encoder.transform(TempDF)
        Mapping.append([field, get_integer_mapping(Encoder)])
        PandasDF.loc[:, field] = Encoded_label

    return PandasDF, Mapping


# -----------------------------------------------------------------------------

# Function for scaling features 
def scaleFeaturesDF(data_train):
    ''' Feature scaling is a type of transformation that only changes the
        scale, but not number of features. Because of this, we can still
        use the original dataset's column names... so long as we keep in
        mind that the _units_ have been altered:
        
        Method: preprocessing.StandardScaler()
            
        INPUT:
            - df : Pandas dataframe for training scaling features
        
        OUTPUT:
            - data_train : data_train transformed
            - transf     : model used for scaling variable of Training Dataset
        
    '''
    X = data_train.columns

    transf = preprocessing.StandardScaler(with_mean=True).fit(data_train)
    data_train = transf.transform(data_train)
    data_train = pd.DataFrame(data=data_train, columns=X)

    return data_train, transf


# -----------------------------------------------------------------------------

# %% Function for Training Classification

# Split in train and test datasest
def split(split_dataset, X, y, perc_testing):
    '''
        Input:
            - split_dataset   : True or False
            - X               : Features Dataset
            - y               : Label Dataset
            - perc_testing    : dataset percentage to assign to testing phase
        Output:
            - data_train      : dataset to train model
            - data_test       : dataset to test model
            - label_train     : label of train dataset
            - label_test      : labelt of test dataset
    '''
    if split_dataset:
        data_train, data_test, label_train, label_test = train_test_split(X, y, test_size=perc_testing, random_state=7)
        print("##--**: Complete to Split Dataset")
        print("Testing dataset dimension equal to", perc_testing * 100, "% of the initial dataset")
    else:
        data_train, data_test, label_train, label_test = X, X, y, y
        print("##--**: Dataset no splitted")

    return data_train, data_test, label_train, label_test


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Function for computing classification evaluation 
def compute_evaluation_stats(label_test, prediction_test):
    '''
        
    '''
    y_true = label_test.values
    y_pred = prediction_test
    columns = ['Closed', 'Open']
    confusion = metrics.confusion_matrix(y_true, y_pred)
    plt.imshow(confusion, cmap=plt.cm.Blues, interpolation='nearest')
    plt.xticks([0, 1], columns, rotation='vertical')
    plt.yticks([0, 1], columns)
    plt.colorbar()
    plt.show()

    tn, fp, fn, tp = metrics.confusion_matrix(y_true, y_pred).ravel()
    print("True Positive:", tp)
    print("True Negative:", tn)
    print("False Positive:", fp)
    print("False Negative:", fn)

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    print("Precision:", precision)
    print("Recall:", recall)

    return precision, recall


# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Function for K-Neighbors
def kneigh(df_train, df_test, label_train, label_test):
    '''
        Function for Training a K-Neighbors Classifier
        Input:
            - df_train      : Features dataset for training model
            - df_test       : Features dataset for testing model
            - label_train   : Label training dataset
            - label_test    : Label testing dataset
            
        Output:
            - knmodel       : Model 
            - knmodel_stats : Statistics about the model
    '''
    # Set model parameters
    print("##--**: Computing K-Neighbors classifier..")
    neighbors = 5
    print("##--**: N-Neighbors:", neighbors)

    # Define model 
    knmodel = KNeighborsClassifier(n_neighbors=neighbors, weights='uniform')

    # Train model
    print("##--**.a: Train KNeighborsClassifier model..")
    knmodel = knmodel.fit(df_train, label_train)

    # Calculate and display the accuracy of the training set
    accuracy_training_knmodel = knmodel.score(df_train, label_train)
    print("Scoring model (accuracy), on training dataset:", accuracy_training_knmodel)

    # Compute Prediction on testing dataset
    prediction_test = knmodel.predict(df_test)

    # Calculate and display the accuracy of the testing set
    accuracy_testing__knmodel = knmodel.score(df_test, label_test)
    print("Scoring model (accuracy), on testing dataset:", accuracy_testing__knmodel)

    # Calculate Evaluation Statistics
    precision_knmodel, recall_knmodel = compute_evaluation_stats(label_test, prediction_test)

    knmodel_stats = ['KNeighborsClassifier', accuracy_training_knmodel, accuracy_testing__knmodel, precision_knmodel,
                     recall_knmodel]

    return knmodel, knmodel_stats

# -----------------------------------------------------------------------------
