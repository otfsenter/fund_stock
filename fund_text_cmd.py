# encoding: utf-8
import requests
from colorama import Fore
from tabulate import tabulate


class Colored:
    # 前景色:红色  背景色:默认
    def red(self, s):
        return Fore.LIGHTRED_EX + s + Fore.RESET

    #  前景色:绿色  背景色:默认
    def green(self, s):
        return Fore.LIGHTGREEN_EX + s + Fore.RESET

    def yellow(self, s):
        return Fore.LIGHTYELLOW_EX + s + Fore.RESET

    def white(self, s):
        return Fore.LIGHTWHITE_EX + s + Fore.RESET

    def blue(self, s):
        return Fore.LIGHTBLUE_EX + s + Fore.RESET


color = Colored()

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
    if rate.startswith('-'):
        rate = color.green(rate)
    else:
        rate = color.red(rate)
    scale = str(round(float(scale), 2)) + '亿'

    data_list.append([str(i) for i in [name, i, today_nav, history_nav, yesterday_nav, rate, date, scale]])

print(tabulate(data_list, head, "grid", stralign='center'))
