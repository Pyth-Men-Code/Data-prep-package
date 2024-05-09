
def netteyer_nom(df):
    """Transform maj to num for Name column """
    df['Name'] = df['Name'].str.Upper()
    return df

def remove_duplicates(df):
    """Remove duplicate rows from a pandas DataFrame."""
    return df.drop_duplicates()

def remove_null_values(df):
    """Remove rows with null values from a pandas DataFrame."""
    return df.dropna()

