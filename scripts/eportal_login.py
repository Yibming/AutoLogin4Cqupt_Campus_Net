"""
基于 eportal 接口的校园网登录脚本
使用 requests 直接登录
"""

import requests
import time
import json
import urllib.parse

# 配置信息
BASE_URL = "http://192.168.200.2"
LOGIN_PORT = 801  # 从页面配置中获取
LOGIN_PATH = "/eportal/?c=ACSetting&a=Login"
USERNAME = "abcd"
PASSWORD = "12345678"

# 运营商配置（从页面 carrier 配置中获取）
CARRIERS = {
    "cmcc": "@cmcc",    # 移动（如果支持）
    "telecom": "@telecom",
    "unicom": "@unicom",
}

CARRIER = "cmcc"  #根据实际情况修改
CHECK_INTERVAL = 30 * 60  # 30分钟


def has_internet():
    """检查是否有网络"""
    try:
        response = requests.get("https://www.baidu.com", timeout=5)
        return response.status_code == 200
    except:
        return False


def login_eportal():
    """使用 eportal 接口登录"""
    print("🚀 开始登录校园网...")
    
    carrier_suffix = CARRIERS.get(CARRIER, "")
    full_username = USERNAME + carrier_suffix
    
    # 构造完整登录 URL（注意端口 801）
    login_url = f"{BASE_URL}:{LOGIN_PORT}{LOGIN_PATH}"
    
    print(f"📍 登录地址: {login_url}")
    print(f"👤 用户名: {full_username}")
    print(f"🔐 密码: {'*' * len(PASSWORD)}\n")
    
    session = requests.Session()
    
    try:
        # 方法1: POST 请求（常见方式）
        print("📤 尝试 POST 请求...")
        
        # 构造表单数据
        data = {
            'DDDDD': full_username,
            'upass': PASSWORD,
            '0MKKey': '123456',  # 常见验证码字段
        }
        
        response = session.post(
            login_url,
            data=data,
            timeout=10,
            allow_redirects=True
        )
        
        print(f"✅ 响应状态: {response.status_code}")
        print(f"📄 响应内容: {response.text[:200]}...\n")
        
        # 检查响应中是否包含成功标志
        if 'Dr.COMWebLoginID_3.htm' in response.text or 'success' in response.text.lower():
            print("✅ 响应包含成功标志")
        
        # 等待一下让系统处理
        time.sleep(2)
        
        # 验证是否真的登录成功
        if has_internet():
            print("✅ 登录成功！网络已连接")
            return True
        else:
            print("⚠️  响应正常但仍无网络，尝试 GET 方法...")
            
            # 方法2: GET 请求
            params = {
                'DDDDD': full_username,
                'upass': PASSWORD,
                '0MKKey': '123456',
            }
            
            response = session.get(
                login_url,
                params=params,
                timeout=10
            )
            
            print(f"✅ GET 响应状态: {response.status_code}")
            time.sleep(2)
            
            if has_internet():
                print("✅ GET 方法登录成功！")
                return True
            else:
                print("❌ 两种方法都失败")
                print("\n🔍 调试信息:")
                print(f"   - 确认运营商设置: {CARRIER} -> {carrier_suffix}")
                print(f"   - 完整用户名: {full_username}")
                print(f"   - 检查密码是否正确")
                print(f"   - 响应内容:\n{response.text[:500]}\n")
                return False
                
    except Exception as e:
        print(f"❌ 登录出错: {e}")
        return False


def main_loop():
    """主循环：定期检测网络并自动登录"""
    print("🔄 开始网络监控...\n")
    
    while True:
        print("🔍 检测网络状态...")
        
        if has_internet():
            print("✅ 网络正常\n")
        else:
            print("❌ 无网络连接")
            login_eportal()
            print()
        
        print(f"⏳ {CHECK_INTERVAL // 60} 分钟后再次检测...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    print("="*60)
    print("校园网自动登录脚本 (eportal 版本)")
    print("="*60)
    print()
    
    # 先检查当前网络状态
    if has_internet():
        print("✅ 当前网络正常")
        choice = input("\n是否启动监控模式？(y/n): ")
        if choice.lower() == 'y':
            main_loop()
    else:
        print("❌ 当前无网络连接，开始登录...\n")
        if login_eportal():
            print("\n启动监控模式...")
            main_loop()
        else:
            print("\n登录失败，请检查配置或手动抓包分析")
            print("\n💡 建议:")
            print("1. 检查 CARRIER 设置是否正确")
            print("2. 用浏览器 F12 抓包查看真实的登录请求")
            print("3. 检查用户名、密码是否正确")
