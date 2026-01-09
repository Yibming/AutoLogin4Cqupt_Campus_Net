import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys


CHECK_INTERVAL = 30* 60  # 每次check时间30分钟
LOGIN_URL = "http://192.168.200.2"  #校园网登陆页面

USERNAME = "12345678"   # 请替换为你的用户名
PASSWORD = "abcd"       # 请替换为你的密码

CARRIERS = {
    "cmcc": "@cmcc",      # 移动
    "telecom": "@telecom",# 电信
    "unicom": "@unicom",  # 联通
    "xyw": "@xyw",        # 教师
}

CARRIER = "telecom"   # <<< 这里改运营商


def has_internet():
    try:
        requests.get("https://www.baidu.com", timeout=5)
        return True
    except:
        return False


def do_login():
    print("🚨 断网，开始自动登录校园网...")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    carrier_value = CARRIERS.get(CARRIER)

    driver.get("http://192.168.200.2")
    time.sleep(3)  # 给足时间，Dr.COM JS 很慢

    try:
        # 1. 选择运营商
        if not carrier_value:
            raise Exception(f"❌ 未知运营商配置: {CARRIER}")
        
        # 找到所有 network radio，只点可见的那个
        radios = driver.find_elements(By.XPATH, f"//input[@name='network' and @value='{carrier_value}']")

        real_radio = None
        for r in radios:
            if r.is_displayed():
                real_radio = r
                break

        if real_radio is None:
            raise Exception(f"❌ 未找到可见的运营商选项: {carrier_value}")

        # 用 JS 方式点击（最稳）
        driver.execute_script("arguments[0].click();", real_radio)
        print(f"✅ 已选择运营商：{CARRIER} ({carrier_value})")

        time.sleep(1)

        # 2. 写账号 + 触发键盘事件
        driver.execute_script(f"""
            var inputs = document.querySelectorAll("input[name='DDDDD']");
            for (var i = 0; i < inputs.length; i++) {{
                if (inputs[i].offsetParent !== null) {{
                    var el = inputs[i];
                    el.removeAttribute('readonly');
                    el.focus();
                    el.value = "{USERNAME}";
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    el.dispatchEvent(new KeyboardEvent('keydown', {{ bubbles: true }}));
                    el.dispatchEvent(new KeyboardEvent('keyup', {{ bubbles: true }}));
                }}
            }}
        """)

        # 3. 写密码 + 触发键盘事件
        driver.execute_script(f"""
            var inputs = document.querySelectorAll("input[name='upass']");
            for (var i = 0; i < inputs.length; i++) {{
                if (inputs[i].offsetParent !== null) {{
                    var el = inputs[i];
                    el.removeAttribute('readonly');
                    el.focus();
                    el.value = "{PASSWORD}";
                    el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    el.dispatchEvent(new KeyboardEvent('keydown', {{ bubbles: true }}));
                    el.dispatchEvent(new KeyboardEvent('keyup', {{ bubbles: true }}));
                }}
            }}
        """)


        print("✅ 已通过 JS 注入账号密码")

        time.sleep(1)

        
        # # 4.
        # 找到可见的密码框
        pwd_inputs = driver.find_elements(By.NAME, "upass")
        real_pwd = None
        for p in pwd_inputs:
            if p.is_displayed():
                real_pwd = p
                break

        if real_pwd is None:
            raise Exception("❌ 没找到可见的密码框")

        real_pwd.send_keys(Keys.ENTER)
        print("🔥 已通过回车键触发登录")

    except Exception as e:
        print("❌ 自动登录过程出错：", e)


    # 等待几秒让登录完成
    time.sleep(1)

    if has_internet():
        print("✅ 自动登录成功，网络已恢复，准备关闭浏览器")

        # 再等 1 秒更稳一点
        time.sleep(1)

        driver.quit()   # 关闭整个浏览器
        print("🧹 浏览器已关闭")

    else:
        driver.quit()   # 关闭整个浏览器
        print("❌ 自动登录失败，仍无法上网，请手动检查")
        # 失败时不要关，方便你观察页面




def main_loop():
    while True:
        print("🔍 检测网络中...")
        if has_internet():
            print("🌐 网络正常")
        else:
            print("❌ 无网络")
            do_login()

        print(f"⏳ {CHECK_INTERVAL//60} 分钟后再次检测...\n")
        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main_loop()
