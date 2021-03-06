import dataframe_image as dfi
import pandas as pd
import requests
import io

url_fund = 'http://hq.sinajs.cn/list=f_%s'

fund_codes = [
    '040046',
    '000834',
    '161130',
    '161128',
    '161725',
    '502056',
    '398051',
    '260108',
]

head = ['名字', '代码', '单位净值', '累计净值', '昨日净值', '跌/涨', '日期', '份额规模']


def style_negative(v):
    if '%' in v:
        if '-' in v:
            return 'color:darkgreen;'
        else:
            return 'color:red'
    else:
        return None


def data2buffer():
    data_list = []
    for i in fund_codes:
        response = requests.get(url_fund % i).text
        name, today_nav, history_nav, yesterday_nav, date, scale = response.split('"')[1].split(',')
        rate = str(round((float(today_nav) - float(yesterday_nav)) / float(yesterday_nav) * 100, 2)) + '%'
        scale = str(round(float(scale), 2)) + '亿'
        data_list.append([str(i) for i in [name, i, today_nav, history_nav, yesterday_nav, rate, date, scale]])

    df = pd.DataFrame(data=data_list, columns=head)
    s = df.style.applymap(style_negative, subset="跌/涨")

    # 用dataframe_image把dataframe的数据写入内存
    f = io.BytesIO()
    dfi.export(s, f)
    f.seek(0)  # 从头开始读，不然数据不完整
    return f
    # 展示用
    # im = Image.open(f)
    # im.show()

    # 关闭buffer
    # f.close()


# if __name__ == '__main__':
#     data2buffer()
