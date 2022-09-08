import pandas as pd
import sqlite3
import numpy as np
from pathlib import Path

from sklearn import preprocessing
import pickle

import re
from pymorphy2 import MorphAnalyzer
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import tensorflow as tf

from sklearn.model_selection import KFold
from sklearn import metrics
from sklearn import model_selection

from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow.keras import callbacks
from tensorflow.keras import utils
from tensorflow.keras import backend
from tensorflow.keras import metrics

from catboost import CatBoostRegressor


def result_for_network():
    con = sqlite3.connect("base.db")

    auto_data = pd.read_sql("SELECT * FROM Data ORDER BY id DESC LIMIT 1", con)

    # auto_data = pd.read_csv('info.csv')

    auto_data.dropna(axis=0, inplace=True)

    # auto_data['engineDisplacement'] = '4.0 LTR'

    # auto_data.drop('Unnamed: 0', axis = 1, inplace=True)
    auto_data.drop('id', axis=1, inplace=True)

    def change_params(value):
        if value == 'None':
            return 'Other'
        else:
            return value

    auto_data['model_info'] = auto_data['model_info'].apply(change_params)

    def engine(value):
        if value != 'undefined LTR':
            new_value = float(value[0:3])
        else:
            new_value = 0.0
        return new_value

    auto_data['engine_v'] = auto_data['engineDisplacement'].apply(engine)

    auto_data['engine_v'] = auto_data.engine_v.apply(lambda x: auto_data['engine_v'].mean() if x == 0.0 else x)

    auto_data.drop('engineDisplacement', axis=1, inplace=True)

    color_arr = ['чёрный', 'белый', 'серый', 'синий', 'серебристый']

    def change_cat(value):
        if value in color_arr:
            return value
        else:
            return 'другой цвет'

    auto_data['color'] = auto_data['color'].apply(change_cat)

    type_arr = ['седан', 'внедорожник 5 дв.', 'купе', 'хэтчбек 5 дв.', 'лифтбек']

    def change_cat(value):
        if value in type_arr:
            return value
        else:
            return 'другой кузов'

    auto_data['bodyType'] = auto_data['bodyType'].apply(change_cat)

    auto_data['гараж'] = auto_data.description.apply(lambda x: 1 if 'гараж' in x else 0)
    auto_data['подарок'] = auto_data.description.apply(lambda x: 1 if 'подарок' in x else 0)
    auto_data['торг'] = auto_data.description.apply(lambda x: 1 if 'торг' in x else 0)
    auto_data['шины'] = auto_data.description.apply(lambda x: 1 if ('шин' in x) or ('резин' in x) else 0)
    auto_data['дилер'] = auto_data.description.apply(lambda x: 1 if 'дилер' in x else 0)
    auto_data['подогрев'] = auto_data.description.apply(lambda x: 1 if 'подогрев' in x else 0)
    auto_data['обмен'] = auto_data.description.apply(lambda x: 1 if 'обмен' in x else 0)
    auto_data['обслуж'] = auto_data.description.apply(lambda x: 1 if 'обслуж' in x else 0)
    auto_data['срочн'] = auto_data.description.apply(lambda x: 1 if 'срочн' in x else 0)
    auto_data['полн'] = auto_data.description.apply(lambda x: 1 if 'полн' in x else 0)
    auto_data['скидк'] = auto_data.description.apply(lambda x: 1 if 'скидк' in x else 0)
    auto_data['диск'] = auto_data.description.apply(lambda x: 1 if 'диск' in x else 0)

    auto_data['4wd'] = auto_data['name'].apply(lambda x: 1 if '4WD' in x else 0)
    auto_data['xdrive'] = auto_data['name'].apply(lambda x: 1 if 'xDrive' in x else 0)

    auto_data.drop('name', axis=1, inplace=True)

    auto_data['Y_no_sale'] = auto_data.productionDate - auto_data.modelDate

    # print(auto_data['productionDate'].iloc[0])
    if auto_data['productionDate'].iloc[0] >= 2022:
        auto_data['m_per_y'] = auto_data.mileage
    else:
        auto_data['m_per_y'] = auto_data.mileage / (2022 - auto_data['productionDate'])

    auto_data['hard_usage'] = auto_data['m_per_y'].apply(lambda x: 1 if x >= 20000 else 0)
    auto_data['trash'] = auto_data.mileage.apply(lambda x: 1 if x >= 300000 else 0)

    def car_age(value):
        return 2022 - value

    auto_data['car_age'] = auto_data['productionDate'].apply(car_age)

    def model_age(value):
        return 2022 - value

    auto_data['modelAge'] = auto_data['modelDate'].apply(model_age)

    auto_data.drop('productionDate', axis=1, inplace=True)
    auto_data.drop('modelDate', axis=1, inplace=True)

    auto_data['mileage'] = np.log(auto_data['mileage'])
    auto_data['m_per_y'] = np.log(auto_data['m_per_y'])

    # auto_data_n = pd.read_csv('/neural_network/auto_data')
    path = Path(Path.cwd(), "neural_network", "auto_data")
    auto_data_n = pd.read_csv(path)

    auto_data = pd.concat([auto_data, auto_data_n], ignore_index=True)

    # print('rrrrrrrr', auto_data.loc[0])

    auto_data.drop('date', axis=1, inplace=True)

    auto_data.drop('Unnamed: 0', axis=1, inplace=True)

    # with open('/neural_network/data.pickle', 'rb') as handle:
    #     b = pickle.load(handle)
    path = Path(Path.cwd(), "neural_network", "data.pickle")
    with open(path, 'rb') as handle:
        b = pickle.load(handle)

    columns_to_change = ['bodyType', 'brand', 'color', 'fuelType',
                         'model_info', 'vehicleTransmission', 'owners',
                         'vehicle_passport', 'type_of_drive', 'wheel']

    set(auto_data_n.columns) - set(columns_to_change)

    data_onehot = b.transform(auto_data[columns_to_change]).toarray()
    column_names = b.get_feature_names_out(columns_to_change)

    # print('Shape of one hot data: {}'.format(data_onehot.shape))

    data_onehot = pd.DataFrame(data_onehot, columns=column_names)

    result_df = pd.concat([
        auto_data.drop(columns_to_change, axis=1),
        data_onehot
    ], axis=1)

    result_df.drop('price', axis=1, inplace=True)

    result_df.dropna(axis=0, inplace=True)

    result_df = result_df.loc[0:2]

    df = result_df['description']
    result_df.drop('description', inplace=True, axis=1)

    X = result_df

    # with open('/neural_network/scaler.pickle', 'rb') as handle:
    #     b = pickle.load(handle)
    path = Path(Path.cwd(), "neural_network", "scaler.pickle")
    with open(path, 'rb') as handle:
        b = pickle.load(handle)

    X_scaled = b.transform(X)

    patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
    stopwords_ru = stopwords.words("russian")
    morph = MorphAnalyzer()

    def lemmatize(doc, stopwords=stopwords_ru):
        # исключаем символы не подходящие под патерны
        doc = re.sub(patterns, ' ', doc)
        tokens = []
        for token in doc.split():
            if token and token not in stopwords:
                token = token.strip()
                token = morph.normal_forms(token)[0]
                tokens.append(token)
        return ' '.join(tokens)

    df.apply(lemmatize)

    vocab_size = 100000  # количество слов
    oov_tok = '<OOV>'  # OOV = Out of Vocabulary

    # with open('/neural_network/tokenizer.pickle', 'rb') as handle:
    #     b = pickle.load(handle)
    path = Path(Path.cwd(), "neural_network", "tokenizer.pickle")
    with open(path, 'rb') as handle:
        b = pickle.load(handle)

    df = b.texts_to_sequences(df)

    trunc_type = 'post'  # метод ограничения
    padding_type = 'post'  # метод дополнения
    embedding_dim = 64  # размер эмбединга
    max_length = 300  # максимальная длина последовательности

    # ограничиваем длину последовательностей

    test_padded = pad_sequences(
        df,
        maxlen=max_length,
        padding=padding_type,
        truncating=trunc_type
    )

    # model = tf.keras.models.load_model('/neural_network/model.h5')
    path = Path(Path.cwd(), "neural_network", "model.h5")
    model = tf.keras.models.load_model(path)

    predictions = model.predict([test_padded, X_scaled])

    # !pip install catboost

    from_file = CatBoostRegressor()

    # from_file.load_model("meta")
    path = Path(Path.cwd(), "neural_network", "meta")
    from_file.load_model(path)

    test_predict_catboost = np.exp(from_file.predict(X_scaled))

    def mape(y_true, y_pred):
        return np.mean(np.abs((y_pred - y_true) / y_true))

    all_predict = (test_predict_catboost + predictions.reshape(-1)) / 2
    # print(all_predict[0])

    return all_predict[0]

# print(result_for_network())
