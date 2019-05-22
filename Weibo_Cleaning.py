import pandas as pd
import re
from datetime import datetime
now = datetime.now()

def weibo_cleaning(file):
    df = pd.read_csv(file, encoding='utf-8')

    def read_number(text):
        numbers = re.findall('\d+', text)
        numbers = map(int, numbers)
        numbers = max(numbers)
        return numbers

    df['read_number'] = df['line1_link'].apply(lambda x: read_number(x))

    import datetime
    from datetime import datetime
    now = datetime.now()

    def change_date(datestring):
        sep = ' 来自'
        datestring = datestring.split(sep, 1)[0]
        if "今天" not in datestring:
            dateint = datetime.strptime(datestring, '%m月%d日 %H:%M')
        else:
            dateint = datestring
        return dateint

    df['datetime'] = df['WB_detail'].apply(lambda x: change_date(x))
    df['datetime'] = pd.to_datetime(df['datetime'], format='%Y-%m-%d %H:%M:%S', errors='coerce')
    df['datetime'] = pd.to_datetime(df['datetime']).dt.date
    df['datetime'] = df['datetime'].apply(lambda x: x.replace(now.year))

    cols = ['line2', 'line3', 'line4']
    df[cols] = df[cols].apply(pd.to_numeric, downcast='integer', errors='coerce')

    df.to_csv("weibo.csv", index=False)