import pandas as pd
import re


def weibo_cleaning(file):
    df = pd.read_csv(file, encoding='utf-8')

    def read_number(text):
        numbers = re.findall('\d+', text)
        numbers = map(int, numbers)
        numbers = max(numbers)
        return numbers

    df['read_number'] = df['line1_link'].apply(lambda x: read_number(x))

    sep = ' 来自'
    df['WB_detail'] = df['WB_detail'].apply(lambda x: x.split(sep, 1)[0])
    if "今天" not in df['WB_detail']:
        df['datetime'] = pd.to_datetime(df['WB_detail'], format='%m月%d日 %H:%M', errors='coerce')
    else:
        df['datetime'] = df['WB_detail']

    df['datetime'] = df['datetime'].apply(lambda x: x.replace(year=2019))
    df['datetime'] = pd.to_datetime(df['datetime']).dt.date

    cols = ['line2', 'line3', 'line4']
    df[cols] = df[cols].apply(pd.to_numeric, downcast='integer', errors='coerce')

    df.to_csv("weibo.csv", index=False)