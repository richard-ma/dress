# dress

[![Build Status](https://travis-ci.org/richard-ma/dress.svg?branch=master)](https://travis-ci.org/richard-ma/dress)

# 系统概述

## 系统结构图

![系统结构图](https://raw.githubusercontent.com/richard-ma/dress/master/doc/DressArchitecture.jpeg)

## 工作过程

在主控网站(a.a.a.a)上运行Web界面，用户可以通过这个网站发布命令。命令目的是将模板网站(y.y.y.y)中的网站模板复制到目标网站(x.x.x.x)上，并成功运行，实现网站的自动复制和配置过程。

# 使用手册

## Host

### 添加Host
* STATUS:                   主机状态（必填）
    * prepare:  还没有网站运行
    * business: 网站正在对外提供服务，可以访问
    * problem:  网站正在对外服务，但出现故障无法访问
    * source:   存放网站模板的主机
* IP:                       主机IP地址（必填）
* SSH Port:                 主机SSH对应的端口号（必填，默认为22）
* Root Password:            主机root用户密码（必填）
* Domain:                   主机域名（必填）
* Database Root Password:   主机上mysql数据库的root用户密码（必填，source类型主机可以不填）
* Memo:                     备注（可选）

## 任务Task

### 网站克隆

* Web Type:                 克隆网站类型（必填）
* Web Source:               源主机即模板存放的主机（必填，只有主机STATUS`是source`的主机才会在这里列出）
* Target Host:              目标主机即网站要放到的主机（必填，主机STATUS`不是source`的主机都会在这里列出）
* Table Prefix:             数据表前缀（必填，可使用默认值）
* Initial order ID value:   订单ID起始编号（必填，可使用默认值，默认值每次自动增加10000）
* SMTP host:                SMTP服务器IP地址或域名（可选）
* SMTP username:            SMTP服务器用户名（可选）
* SMTP password:            SMTP服务器密码（可选）

### 克隆完成

* 可查看本工具所在目录下的dress.log日志文件
* 给目标主机添加screen会话，可以在目标主机查看克隆状态
* 更新目标主机STATUS状态，提示克隆完成(TODO)

# 安装

## 在线安装
* yum install python3 git
* pip install virtualenv
* virtualenv -p python3 dress-virtualenv
* cd dress-virtualenv
* git clone git@github.com:richard-ma/dress.git
* pip install -r requirements.txt
* python manager.py db upgrade
* python manager.py seed

## 上传安装
* yum install python3
* pip install virtualenv
* virtualenv -p python3 dress-virtualenv
* cd dress-virtualenv
* 上传压缩包并解压，使用cd命令进入解压后的目录
* pip install -r requirements.txt
* python manager.py db upgrade
* python manager.py seed

# 基本操作

## 启动
* screen -S dress\_master
* python manager.py runserver
* Ctrl-a d
* 浏览器访问: http://主机ip:5000

## 停止 
* screen -r dress\_master
* Ctrl-c
* exit

## 重新启动
* 参照上述操作先停止再启动

## 导入source主机信息
* 将所有source主机信息写入sourcehost.csv文件中并保存到本程序根目录下
* python manager.py importsource
* 重新启动

## 运行功能测试（可选）
* python manager.py test
