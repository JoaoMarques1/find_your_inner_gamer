import math
import pandas as pd

def encoding_ach(df):
    """
    binary encoder for achievemen†s

    Args:
        df (DataFrame):

    Returns:
        df: dataframe with binary encoded achievements
    """

    for i in df.index:
        df.at[i, 'achievement_cat'] = 0 if math.isnan(df.loc[i]['achievements']) == True else 1
    df = df.drop([ 'achievements'], axis = 1)
    return df


def encoding_lang(df, n):
    """
     encoder for languages - encode the n most used languages

    Args:
        df (DataFrame):

    Returns:
        df: dataframe
    """
    languages = {}
    for index, row in df.iterrows():
        languages_list= str(row['languages']).split(',')
        for language in languages_list:
            if not language in languages:
                languages[language] = 1
            else:
                languages[language] += 1

    languages_df = pd.DataFrame(list(languages.items()),columns = ['languages','count'])
    languages_df.sort_values('count', ascending =False)
    lang_list = [language for language in languages_df.sort_values('count', ascending =False).head(n)['languages']]

    for lang in lang_list:
        for i in df[df['languages'].isnull() == False].index:
            df.at[i, lang] = 1 if lang in df['languages'][i] else 0
    return df
