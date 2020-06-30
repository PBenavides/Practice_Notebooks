import os
from nltk.corpus import stopwords
import unidecode 
import re 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


#Config
agg_stopword = ['s', '2018','31','diciembre','financieros','000','2019','nota','grupo','valor','2017','resultados','compania','1',
 'total','consolidados','consolidado','razonable','gerencia','ciento','c','activos','cuentas','neto','us','efectivo','fecha','peru',
 'inretail','2','3','importe', 'aproximadamente','b','respectivamente','ver','ano','si','vida','anos','4','d','5','i','www','com',
 'aa', 'aaa', 'aaahipotecario', 'aaatat', 'aamnto', 'ab','ir','email','mes','niif','fmiv','bbb','ok','mzo','inc']

stopwords_espaniol = stopwords.words('spanish')
stopwords_espaniol.extend(agg_stopword)

def remove_stopword(x, lista_stopwords):
    return [y for y in x if y not in lista_stopwords]

def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers. Also, we added the unicode line for accent marks'''
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text) #Punctuations...
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = unidecode.unidecode(text)
    return text

def make_clean_dataframe(stopwords_espaniol, path_textos):
    #Accedo al path y jalo toda la info
    dicc={}
    for nombre_doc in os.listdir(path_textos):
        text_string = open(path_textos+'/'+nombre_doc).read()
        dicc[nombre_doc[:-4]] = text_string
    
    #Limpio y transformo el texto.
    dataframe = pd.DataFrame(dicc,index=[0]).T.rename(columns={0:'texto'}).reset_index()
    dataframe['temp_list'] = dataframe['texto'].apply(lambda x: clean_text(x))
    dataframe['temp_list'] = dataframe['temp_list'].apply(lambda x: str(x).split())
    dataframe['texto_limpio'] = dataframe['temp_list'].apply(lambda x: remove_stopword(x, stopwords_espaniol))
    dataframe = dataframe.rename(columns={'index':'nombre_doc'})

    for k,v in dataframe['texto_limpio'].items():
        dataframe.loc[k,'raw_clean_text'] = ' '.join(dataframe.loc[k,'texto_limpio'])
    
    return dataframe

def analisis_sentimientos(path_excel, dataframe,method='count'):
    
    positive_words = pd.read_excel(path_excel, sheet_name='Positive',header=None,names=['positivas','pos_traducidas'])
    negative_words = pd.read_excel(path_excel, sheet_name='Negative',header=None,names=['negativas','neg_traducidas'])
    #limpio las palabras
    positive_words['pos_traducidas'] = positive_words['pos_traducidas'].str.lower().apply(lambda x: clean_text(x))
    negative_words['neg_traducidas'] = negative_words['neg_traducidas'].str.lower().apply(lambda x: clean_text(x))
    
    #Hare una lista de palabras malas y buenas. A esta lista la desplegaré en strings grandes separados por |
    bad_words = negative_words['neg_traducidas'].dropna().tolist()
    good_words = positive_words['pos_traducidas'].dropna(axis=0).tolist()

    bad_words_str_one = '|'.join(bad_words[:1750])
    bad_words_str_two = '|'.join(bad_words[1750:])
    good_words_str = '|'.join(good_words)
    if method == 'count':
        dicc_empresas = {}
        for nombre_doc in dataframe['nombre_doc'].values:
            lista_nombre = nombre_doc.split('_')
            dicc_empresas[lista_nombre[1]+'_'+lista_nombre[2]+ '_'+lista_nombre[3]] = {'good':dataframe.loc[dataframe['nombre_doc'] == nombre_doc, 'raw_clean_text'].str.count(good_words_str).values[0],
                                                        'bad':dataframe.loc[dataframe['nombre_doc'] == nombre_doc, 'raw_clean_text'].str.count(bad_words_str_one).values[0] +
                                                    dataframe.loc[dataframe['nombre_doc'] == nombre_doc, 'raw_clean_text'].str.count(bad_words_str_two).values[0]}
        return pd.DataFrame(dicc_empresas)

    elif method == 'tfidf':
        vectorizer = TfidfVectorizer(ngram_range=(1,3))
        tfidf = vectorizer.fit_transform(dataframe['raw_clean_text']) #

        index_value = {i[1]:i[0] for i in vectorizer.vocabulary_.items()}

        #Fully_indexed son todos los indices con su respectivo valor 
        fully_indexed = []
        for row in tfidf:
            fully_indexed.append({index_value[column]:value for (column,value) in zip(row.indices, row.data)})
        
        tfidf_df = pd.DataFrame(tfidf.toarray(), columns=vectorizer.get_feature_names()).T
        tfidf_df = tfidf_df.reset_index().rename(columns={'index':'palabras'})
        
        return tfidf_df

    else:
        raise NotImplementedError



