# /usr/bin/env python
# coding=utf8

import httplib
import md5
import urllib
import random
import json
import codecs
import traceback


class MyTranslator:
    appid_list = [
        ('20180116000115610', '_dSZB6V4NkvTzQPlAWKZ'),
        ('20180108000113096', '6SoGftc65GEs3GcQSRi7'),
        ('20180109000113451', '25Yc0E58yOOxIQFONkcO'),

        ('20180110000113705', 'hOsZSKq1Ya2vPJwBK6wN'),
        # ('20180118000116684', 'J0Drvmy9UGcNwNMrDvYK'),
        # ('20170226000039912', 'BwxN9UzG3yZbRQcJvc7d'),
        # ('', ''),
        # ('', ''),
    ]
    appid_index = 0
    error_count = 0

    def geturl(self, sentence):
        if self.error_count == 1000:
            self.error_count = 0
            self.appid_index += 1
        q = sentence
        appid = self.appid_list[self.appid_index][0]
        secretKey = self.appid_list[self.appid_index][1]
        fromLang = 'en'
        toLang = 'zh'
        salt = random.randint(32768, 65536)
        myurl = '/api/trans/vip/translate'
        sign = appid + q + str(salt) + secretKey
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(salt) + '&sign=' + sign
        return myurl

    def translate_sentence(self, sentence):
        rs = ''
        try:
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            myurl = self.geturl(sentence)
            httpClient.request('GET', myurl)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            obj = json.loads(response.read(), encoding='utf-8')
            trans_rs = obj['trans_result']
            if len(trans_rs) == 1:
                rs = trans_rs[0]['dst']
            else:
                for e in trans_rs:
                    rs += e['dst'] + ' '
        except Exception, e:
            print e, sentence
            traceback.print_exc()
            self.error_count += 1
        finally:
            if httpClient:
                httpClient.close()
            return rs

    def process_annotations(self, source_path, des_path):
        count = 0
        raw_data = json.load(codecs.open(source_path, 'r', 'utf-8'))
        annotations = raw_data['annotations']
        print('total sentence: ')
        print(len(annotations))
        for e in annotations:
            if e.has_key('caption_cn') and len(e['caption_cn']) > 0:
                continue
            caption_cn = self.translate_sentence(e['caption'])
            if len(caption_cn) > 0:
                e['caption_cn'] = caption_cn
                count += 1
            if count == 1000:
                count = 0
                json.dump(raw_data, codecs.open(des_path, 'w', 'utf-8'), ensure_ascii=False, indent=4)
        json.dump(raw_data, codecs.open(des_path, 'w', 'utf-8'), ensure_ascii=False, indent=4)


t = MyTranslator()
t.process_annotations('captions_train2014_formated.json', 'captions_train2014_formated.json')

print('\nend\n')
