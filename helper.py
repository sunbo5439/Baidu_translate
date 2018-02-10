# coding=utf8

import httplib
import md5
import urllib
import random
import json
import codecs
import jieba


def validate(json_path):
    raw_data = json.load(codecs.open(json_path, 'r', 'utf-8'))
    annotations = raw_data['annotations']
    key = 'caption_cn_toked'
    for e in annotations:
        if not e.has_key(key):
            print e['image_id']
            print 'not has caption_cn\n'
            continue
        if len(e[key]) == 0:
            print e['image_id']
            print 'empty line\n'


def token_cn(json_path):
    raw_data = json.load(codecs.open(json_path, 'r', 'utf-8'))
    annotations = raw_data['annotations']
    for e in annotations:
        caption_cn = e['caption_cn']
        caption_cn_toked = ' '.join(jieba.cut(caption_cn))
        e['caption_cn_toked'] = caption_cn_toked
    json.dump(raw_data, codecs.open(json_path, 'w', 'utf-8'), ensure_ascii=False, indent=4)


token_cn('captions_train2014_formated.json')
token_cn('captions_val2014_format.json')


def doit(json_path):
    raw_data = json.load(codecs.open(json_path, 'r', 'utf-8'))
    annotations = raw_data['annotations']
    for e in annotations:
        caption_en = e['caption']
        caption_cn_toked = e['caption_cn_toked']
        e['caption_en'] = caption_en
        e['caption'] = caption_cn_toked
    json.dump(raw_data, codecs.open(json_path, 'w', 'utf-8'), ensure_ascii=False, indent=4)


doit('captions_train2014_formated.json')
doit('captions_val2014_format.json')

# validate('captions_train2014_formated.json')
# validate('captions_val2014_format.json')
