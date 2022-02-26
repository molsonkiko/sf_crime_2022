import pandas as pd

def make_infoframe(df: pd.DataFrame) -> pd.DataFrame:
    '''a DataFrame that contains useful info about all the columns in the
    DataFrame df.'''
    description = df.describe(include = 'all',
                              datetime_is_numeric=True).T.iloc[:, 2:]
    nancts = df.isna().sum(axis = 0)
    nanpct = nancts/df.shape[0]
    mydata = pd.DataFrame({'nanpct': nanpct,
                           'dtype': df.dtypes,
                           'nunique': df.nunique()})
    return pd.merge(mydata, description, left_index = True, right_index = True)