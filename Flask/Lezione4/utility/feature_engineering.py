import pandas as pd
from sklearn import preprocessing

# Function for getting mapping from Encoding function
def get_integer_mapping(le):
    '''
    Return a dict mapping labels to their integer values
    from an SKlearn LabelEncoder
    le = a fitted SKlearn LabelEncoder
    '''
    res = {}
    for cl in le.classes_:
        res.update({cl:le.transform([cl])[0]})

    return res

def encode_fields(PandasDF, fields):
    '''
    Return the dataframe with the fields encoded and the mapping infos
        INPUT:
            - PandasDF  : Dataframe
            - fields    : List of fields
    '''
    Mapping = []
    for field in fields:
        print("Encoding.. :",field)
        TempDF = PandasDF.loc[:, field].copy()
        TempDF.loc[TempDF.isnull()==True] = '-99'
        Encoder = preprocessing.LabelEncoder()
        Fitted_Encoder = Encoder.fit(TempDF)
        Encoded_label = Fitted_Encoder.transform(TempDF)
        Mapping.append([field, get_integer_mapping(Encoder)])
        PandasDF.loc[:, field] = Encoded_label
    
    return PandasDF, Mapping

# Function for scaling features 
def scale_features(data_train, data_test=None):
    ''' Feature scaling is a type of transformation that only changes the
        scale, but not number of features. Because of this, we can still
        use the original dataset's column names... so long as we keep in
        mind that the _units_ have been altered:
        
        Method: preprocessing.StandardScaler()
            
        INPUT:
            - data_train = Pandas dataframe for training scaling features
            - data_test = Pandas dataframe to transform
        
        OUTPUT:
            - data_train = data_train transformed
            - data_test = data_test transformed
        
    '''

    X = data_train.columns
    transf = preprocessing.StandardScaler(with_mean=True).fit(data_train)
    data_train = transf.transform(data_train)
    data_train = pd.DataFrame(data=data_train, columns = X)
    
    if data_test is not None:
        Y = data_test.columns
        data_test = transf.transform(data_test)
        data_test = pd.DataFrame(data=data_test, columns = Y)
    else:
        data_test = pd.DataFrame()

    return data_train, data_test, transf   