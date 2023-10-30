from nlp.sentiment import Sentiment_classification, Emotion_detection, Toxicity_detection
from nlp.dataset import VKPostsDataset
from nlp.preprocessing import clean, find_congratulation, emoji2text

#from deep_translator import GoogleTranslator
from translate import Translator
from tqdm import tqdm

import json
import pandas as pd
import requests
import re

tqdm.pandas()


def fill_result(clf, text):
    try:
        res = clf.classify_text(text)
    except:
        res = None

    return res

def process(data, with_entities = False, check_congrats = False, convert_emoji = False):
    df = pd.DataFrame.from_dict(data)

    df['text'] = df['text'].apply(clean)

    if convert_emoji == True:
        translator = Translator(to_lang="ru")
        df['text'] = df['text'].progress_apply(lambda x: emoji2text(x, emoji, translator))


    dataset = VKPostsDataset(data=df, with_entities=with_entities)

    clf = Sentiment_classification()
    emclf = Emotion_detection()
    toxclf = Toxicity_detection()

    df['sentiment'] = df['text'].progress_apply(lambda text : fill_result(clf=clf, text=text))  ## Анализ тональности
    df['emotion'] = df['text'].progress_apply(lambda text : fill_result(clf=emclf, text=text))  ## Выявление эмоций
    df['toxicity'] = df['text'].progress_apply(lambda text : fill_result(clf=toxclf, text=text))  ## Ввыявление токсичности

    if check_congrats == True:
        df['is_congratulation'] = df['text'].progress_apply(find_congratulation)  ## выявляет сообщения с поздравлениями

    return df.to_dict('records')