# dress

[![Build Status](https://travis-ci.org/richard-ma/dress.svg?branch=master)](https://travis-ci.org/richard-ma/dress)

# 使用手册

## Host

### 添加Host
* STATUS                    主机状态
    * prepare   还没有网站运行
    * business  网站正在对外提供服务，可以访问
    * problem   网站正在对外服务，但出现故障无法访问
    * source    存放网站模板的主机
* IP                        主机IP地址
* SSH Port                  主机SSH对应的端口号，默认为22
* Root Password             主机root用户密码
* Domain                    主机域名（如果一台主机有多个域名，则需要添加多条不同域名的Host, 每个域名一条）
* Database Root Password    主机上mysql数据库的root用户密码
* Memo                      备注，可不填

## Clone

* Web Type                  克隆网站类型
* Web Source                源主机即模板存放的主机（只有主机STATUS*是source*的主机才会在这里列出）
* Target Host               目标主机即网站要放到的主机（主机STATUS*不是source*的主机都会在这里列出）
* Table Prefix              数据表前缀，一般使用默认值即可
* Initial order ID value    订单ID起始编号，每次自动增加10000
* SMTP host                 SMTP服务器IP地址或域名（不修改不填即可）
* SMTP username             SMTP服务器用户名（不修改不填即可）
* SMTP password             SMTP服务器密码（不修改不填即可）

### 克隆完成

* 可查看本工具所在目录下的dress.log日志文件
* 给目标主机添加screen会话，可以在目标主机查看克隆状态(TODO)
* 更新目标主机STATUS状态，提示克隆完成(TODO)

# INSTALL
* virtualenv -p python3 `directory`
* cd `directory`
* git clone git@github.com:richard-ma/dress.git
* pip install -r requirements.txt
* python seed.py

# TESTING
* ./test.sh

# RUN
* python manager.py runserver
* Browser: http://host-ip:5000
