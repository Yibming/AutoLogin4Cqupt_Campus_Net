# AutoLogin4Cqupt_Campus_Net
This project logs into the CQUPT campus network by invoking the Google Chrome driver.
这个项目通过调用google chrome driver登陆重庆邮电大学校园网

本项目目前可以实现:
1.运行之后会循环检测是否有网络，没有网络就打开上网登陆页登陆


## requirements
目前用python3.10, 估计3.8等也可以运行,故对python版本不做要求

### selenium requests 工具安装
```bash
pip install selenium requests
```

### 安装ChromeDriver
先确认有没有安装Chrome 和 ChromeDriver（ChromeDriver版本要匹配Chrome）
```bash
google-chrome --version
```
比如显示：
```bash
Google Chrome 136.0.7103.113 
```
那就下载对应136的driver：
```bash
wget https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.113/linux64/chromedriver-linux64.zip
unzip chromedriver-linux64.zip
sudo mv chromedriver-linux64/chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```
如果wget显示连接错误直接复制粘贴下面地址到浏览器：
```bash
https://storage.googleapis.com/chrome-for-testing-public/136.0.7103.113/linux64/chromedriver-linux64.zip

```
下载好后继续运行上面的解压和移动的代码。

验证是否安装成功
```bash
chromedriver --version
```
成功会显示：
```bash
ChromeDriver 136.0.7103.113
```

没有对应的可以上下面网站找一找
https://chromedriver.chromium.org/downloads


### 运行
运行前要去autologin_ubuntu.py改自己的账户密码和运营商

```bash
cd Autologin4campus_cqupt_net
python scripts/autologin_ubuntu.py
```
