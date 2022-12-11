## 说明
本脚本实现的功能：
1. 自动把证书文件上传到qiniu服务器  
**注意：** qiniu服务器仅支持pem格式证书，如果是其他格式请自行转换
2. 更新证书到1到多个cdn域名上

## 运行环境
### python版本
- python3

### 依赖模块
- qiniu
- requests
- PyYAML

### 配置文件格式
参考`config.yaml.example`文件

## 安装
1. 首先安装`virtualenv`，  
`pip3 install virtualenv`
2. 创建名为`venv`的虚拟环境  
`virtualenv --python=python3 venv `
3. 激活并进入环境  
`source venv/bin/activate`
4. 安装依赖模块（只需运行一次）  
`pip install -r requirements.txt`
5. 根据`config.yaml.example`文件创建`config.yaml`配置文件，并根据说明进行正确配置  
`cp config.yaml.example config.yaml`
6. 运行`main.py`脚本进行证书上传和更新
7. 退出虚拟环境  
`deactivate`

## 加入bash脚本或者`acme.sh`等更新脚本
```shell
#!/bin/bash
source "<absolute_path_recommended_here>/venv/bin/activate"
python "<absolute_path_recommended_here>/main.py"
deactivate
```
注意：首先要安装依赖模块

## 引用
- [qiniu cdn api](https://developer.qiniu.com/fusion/4243/access-to-the)
- [qiniu python sdk](https://github.com/qiniu/python-sdk)