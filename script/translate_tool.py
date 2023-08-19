import re
import threading
from hashlib import md5
import random
import time
import requests
import json

class Translator:
    def __init__(self, from_lang, to_lang, appid, secretKey):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.appid = appid
        self.secretKey = secretKey
        self.url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    # def make_md5(s, encoding='utf-8'):
    #     return md5(s.encode(encoding)).hexdigest()
    def translate(self, text):
        if self.from_lang == self.to_lang:
            return text
        salt = random.randint(32768, 65536)
        s = self.appid + text + str(salt) + self.secretKey
        sign = md5(s.encode('utf-8')).hexdigest()
        payload = {'appid': self.appid, 'q': text, 'from': self.from_lang, 'to': self.to_lang, 'salt': salt, 'sign': sign}# Build request
        response = requests.post(self.url, params=payload, headers=self.headers)# Send request
        result_all = response.json()
        time.sleep(0.1)
        return result_all["trans_result"][0]["dst"]

def __translate(translator, text, n):
    if text == "" or text == '\n':
        return text

    text = text.rstrip('\n')
    if re.match(r"^[0-9]+$", text):
        return add_newline_if_missing(text)

    if re.match(r"\d{2}:\d{2}:\d{2},\d{3}\s-->\s\d{2}:\d{2}:\d{2},\d{3}", text):
        return add_newline_if_missing(text)

    return add_newline_if_missing(translator.translate(text))


def add_newline_if_missing(s):
    if not s.endswith('\n'):
        s += '\n'
    return s


def translate_task(lines, translator_fun, result_map, i, translator):
    print("thread id: ", i, "lines num: ", len(lines))
    result_map[i] = [translator_fun(translator, line, n) for n, line in enumerate(lines)]


def translate_file(translator_fun, file1, file2, thread_nums, translator=None):
    with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'w', encoding='utf-8') as f2:
        lines = f1.readlines()
        print("translate file total lines: ", len(lines))
        result = get_translate_result(lines, thread_nums, translator, translator_fun)
        f2.writelines(result)
        print("\ntranslate write file done")


def get_translate_result(lines, thread_nums, translator, translator_fun):
    result_map = get_translate_threads_result(lines, thread_nums, translator, translator_fun)
    result = []
    for key in sorted(result_map):
        result.extend(result_map.get(key))
    return result


def get_translate_threads_result(lines, thread_nums, translator, translator_fun):
    result_map = {}
    threads = []
    n = len(lines) // thread_nums
    for i in range(1, thread_nums + 1):
        threads.append(
            threading.Thread(target=translate_task, args=(
                get_split_lines(i, lines, n, thread_nums), translator_fun, result_map, i, translator)))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return result_map


def get_split_lines(i, lines, n, thread_nums):
    if n * i <= len(lines):
        split_line = lines[(i - 1) * n:i * n]
    else:
        split_line = lines[(i - 1) * n:]
    if i == thread_nums and n * i < len(lines):
        split_line = lines[(i - 1) * n:]
    return split_line


def do_translate(file1, file2, from_lang, to_lang, thread_nums, appid, secretKey):
    translator = Translator(from_lang, to_lang, str(appid), secretKey)
    translate_file(__translate, file1, file2, thread_nums, translator)


if __name__ == '__main__':
    do_translate('test.srt', 'test1.srt', 'ja', 'zh')
