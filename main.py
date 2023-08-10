#!/usr/bin/env python3
# https://developer.qiniu.com/fusion/8593/interface-related-certificate

import json
from os.path import abspath, dirname

from qiniu import Auth
import requests
import yaml

with open(dirname(abspath(__file__)) + '/config.yaml', 'r') as f:
    configYamlString = f.read()
config = yaml.safe_load(configYamlString)


# 七牛云相关信息
AK = config['AK']
SK = config['SK']
apiUrlPrefix = 'https://api.qiniu.com'
apiUrl = f'{apiUrlPrefix}/sslcert'


# 需要上传到七牛云的信息，具体可以查看config.yaml.example
keyFilePath = config['keyFilePath']
crtFilePath = config['crtFilePath']
crtName = config['crtName']
crtCommonName = config['crtCommonName']
cdnDomains = config['cdnDomains']


with open(keyFilePath, 'r') as f:
    key = f.read()
with open(crtFilePath, 'r') as f:
    crt = f.read()


# 实例化qiniu Auth对象，获得access token
authObject = Auth(AK, SK)
postData = {'name': crtName, 'common_name': crtCommonName, 'pri': key, 'ca': crt}
accessToken = authObject.token_of_request(apiUrl, postData)
print(accessToken)


# 获取七牛云上所有证书ID，方便后面的更新提交
headers = {'Authorization': "QBox {0}".format(accessToken), 'Content-Type': 'application/json'}
resp = json.loads(requests.post(apiUrl, json=postData, headers=headers).text)
print(resp)
if resp['code'] != 200:
    raise Exception(resp['error'])
certId = resp['certID']


# 开始循环更新证书到CDN域名
for domain in cdnDomains:
    apiUrlForDomain = f'{apiUrlPrefix}/domain/{domain["name"]}/httpsconf'
    putData = {
        'certId': certId,
        'forceHttps': domain['forceHttps'],
        'http2Enable': domain['http2Enable']
    }

    accessToken = authObject.token_of_request(apiUrlForDomain, putData)
    print(accessToken)

    headers = {
        'Authorization': "QBox {0}".format(accessToken),
        'Content-Type': 'application/json'
    }

    print(json.loads(
        requests.put(apiUrlForDomain, json=putData, headers=headers).text
    ))

