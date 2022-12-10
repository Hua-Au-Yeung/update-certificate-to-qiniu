## 说明
本脚本根据配置，自动把证书文件上传到qiniu cdn服务器，并更新到1到多个cdn域名上。

## 运行环境
### python版本
- python3

### 依赖模块
- qiniu
- requests
- PyYAML

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
