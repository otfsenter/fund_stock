import dataframe_image as dfi
import pandas as pd
import requests

ji_code = [
    '040046',
    '000834',
    '161130',
    '161128',
    '161725',
    '502056',
    '398051',
]

head = ['名字', '代码', '单位净值', '累计净值', '昨日净值', '跌/涨', '日期', '份额规模']

data_list = []
for i in ji_code:
    jijin_jin = requests.get('http://hq.sinajs.cn/list=f_' + i)
    a = jijin_jin.text
    name, today_nav, history_nav, yesterday_nav, date, scale = a.split('"')[1].split(',')
    rate = str(round((float(today_nav) - float(yesterday_nav)) / float(yesterday_nav) * 100, 2)) + '%'
    scale = str(round(float(scale), 2)) + '亿'
    data_list.append([str(i) for i in [name, i, today_nav, history_nav, yesterday_nav, rate, date, scale]])

df = pd.DataFrame(data=data_list, columns=head)


def style_negative(v):
    if '%' in v:
        if '-' in v:
            return 'color:darkgreen;'
        else:
            return 'color:red'
    else:
        return None


s = df.style.applymap(style_negative, subset="跌/涨")

dfi.export(s, "mytable.png")
