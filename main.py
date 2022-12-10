#!/usr/bin/env python3
# https://developer.qiniu.com/fusion/8593/interface-related-certificate

import json
import requests
import yaml
from qiniu import Auth

with open('config.yaml', 'r') as f:
    configYamlString = f.read()
config = yaml.safe_load(configYamlString)

AK = config['AK']
SK = config['SK']

# 需要把下面的公钥/私钥更新到下面的cdn域名中去
keyFilePath = config['keyFilePath']
crtFilePath = config['crtFilePath']
crtName = config['crtName']
crtCommonName = config['crtCommonName']
cdnDomains = config['cdnDomains']

# 七牛cdn的api接口url前缀
apiUrlPrefix = 'https://api.qiniu.com'

with open(keyFilePath, 'r') as f:
    key = f.read()
with open(crtFilePath, 'r') as f:
    crt = f.read()

# 实例化qiniu Auth对象，方便获得access token
q = Auth(AK, SK)

# 更新证书
apiUrl = '{0}/sslcert'.format(apiUrlPrefix)

postData = {
    'name': crtName,
    'common_name': crtCommonName,
    'pri': key,
    'ca': crt
}

accessToken = q.token_of_request(apiUrl, postData)
print(accessToken)

headers = {
    'Authorization': "QBox {0}".format(accessToken),
    'Content-Type': 'application/json'
}

resp = json.loads(
    requests.post(apiUrl, json=postData, headers=headers).text
)
print(resp)
if resp['code'] != 200:
    raise Exception(resp['error'])

# 获取证书ID
certId = resp['certID']

# 更新证书到域名
apiUrl = '{0}/domain/{1}/httpsconf'
for domain in cdnDomains:
    apiUrlForDomain = apiUrl.format(apiUrlPrefix, domain['name'])
    putData = {
        'certId': certId,
        'forceHttps': domain['forceHttps'],
        'http2Enable': domain['http2Enable']
    }

    accessToken = q.token_of_request(apiUrlForDomain, putData)
    print(accessToken)

    headers = {
        'Authorization': "QBox {0}".format(accessToken),
        'Content-Type': 'application/json'
    }

    resp2 = json.loads(
        requests.put(apiUrlForDomain, json=putData, headers=headers).text
    )
    print(resp2)
