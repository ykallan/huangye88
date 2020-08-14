# -*- coding: utf-8 -*-#
# FileName:         字体加密破解
# Description:  
# Author:       Thor
# Date:         2020/6/3 20:46
from fontTools.ttLib import TTFont
import re
import requests
import io
import sys

import base64

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
# 通过查看xml可以发现他得就是通过英文数字然后变成正常得数字
english_2_num = {'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8,
                 'nine': 9}


def get_map_url(font_name):
    # 把字体文件读取为python能理解的对象
    base_font = TTFont(font_name)
    base_font.saveXML('font.xml')
    # 你可以自行查看xml文件，下得cmap 里面有对应得编码关系
    font_set = base_font.getBestCmap()
    print('font_set:->', font_set)
    # 打印看font_set 这步可以直接用遍历字典做
    print(type(font_set), font_set.keys(), type(font_set.keys()))
    # 从第五个开始取，是因为第五个后才是跟数字有关系
    new_keys_1 = [(str(chr(i))) for i in list(font_set.keys())[5:]]

    # 针对编码问题，先进行unicode编码在进行decode解码
    new_keys = [i.encode('unicode_escape').decode().replace('\\U000', '&#x') for i in new_keys_1]
    print(new_keys)
    new_values = []
    # 得到相对应得字体所对应得数字
    for i in list(font_set.values())[5:]:
        new_values.append(english_2_num[i])
    print('new_values:->', new_values)
    # 设置字字体与数字得对应关系:
    new_font_set_1 = {}
    if len(new_values) == len(new_keys):
        for i in range(len(new_values)):
            new_font_set_1[new_keys[i]] = new_values[i]
    print(new_font_set_1)
    return new_font_set_1

# 拿到字体加密得文件
url = 'http://b2b.huangye88.com/gongsi/company44m4c2kf24bc/'
response = requests.get(url)
response.encoding = response.apparent_encoding
# 拿到字体加密连接 我这里正则匹配有点问题因为匹配到了 " 所有我没取他
# base_str = re.findall('url\("data:font/ttf;charset=utf-8;base64,(.*?)\)', response.text)[0][:-1]

base_str = re.findall('url\("data:font/ttf;charset=utf-8;base64,(.*?)"\) format\("truetype"\);', response.text)[0]
print(base_str[0][:-1])
# base64解密以下 写入woff 文件
bin_data = base64.decodebytes(base_str.encode())
with open('text.woff', 'wb') as f:
    f.write(bin_data)
# 通过函数返回真正的编码跟数字对应的关系
new_font_set_1 = get_map_url('text.woff')
# 通过报错html 进行验证
with open('替换之前.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

content = response.text

with open('替换之前.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(new_font_set_1.keys())
# 进行替换
for k, v in new_font_set_1.items():
    # print(k, v)
    content = content.replace(k + ';', str(v))

with open('替换之后.html', 'w', encoding='utf-8') as f:
    f.write(content)
