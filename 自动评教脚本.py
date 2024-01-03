import subprocess
import string


# 运行前请关闭所有的chrome浏览器。
# 使用前请在python环境下请安装好selenium,编写时使用的是4.16.0
# 对老师说的话可以统一在text_i.send_keys("无，老师很好")修改

'''
第一部分获取chrome位置
时间较久可选择跳过

'''
def find_chrome_exe():
    # 常见的盘符从 C 到 Z
    for drive in string.ascii_uppercase[2:]:
        try:
            # 构建并执行 dir 命令
            command = f"dir {drive}:\\chrome.exe /s /b"
            result = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL)
            if result:
                # 返回找到的第一个路径
                return result.decode().split('\n')[0].strip()
                break
        except subprocess.CalledProcessError:
            # 当 dir 命令在某个盘符上找不到文件时，会抛出异常
            continue
    return None

chrome_path = find_chrome_exe()
if chrome_path:
    print(f"Found Chrome at: {chrome_path}")
else:
    print("Chrome.exe not found.")



'''
 第二部分：启动 Chrome 浏览器
'''
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re
import subprocess
import string

def start_chrome(debug_port=9999,chrome_path=None):
    if chrome_path:
        subprocess.Popen(f"\"{chrome_path}\" --remote-debugging-port={debug_port}", shell=True)
    else:
        print("Chrome path not found. Please ensure Google Chrome is installed.")


start_chrome(chrome_path=chrome_path)
# 等待一小段时间以确保 Chrome 启动
'''
第三部分：接管启动的chrome浏览器，
并且确保相对应网址启动成功
'''
time.sleep(5)
#接管浏览器
options = Options()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9999")
driver = webdriver.Chrome(options=options)
driver.get(r'http://jxzlpj.chd.edu.cn/xssy')
input('请先登录http://jxzlpj.chd.edu.cn/login，登录后随意输入一个数字')



'''
第四部分开始自动评教
'''
# 访问网页
driver.get(r'http://jxzlpj.chd.edu.cn/xssy')
time.sleep(3)
#进行第一次点击
try:
    # 使用 XPath 定位元素
    element = driver.find_element(By.XPATH, "//a[.//span[contains(text(), '2023-2024学年第一学期学生网上评教')]]")
    element.click()
except Exception as e:
    print(f"Error: {e}")


# 使用正则表达式查找 data-v 属性
time.sleep(3)    #等待加载
page_source = driver.page_source
# data_v_pattern = re.compile(r'data-v-\w+')

data_v_pattern = re.compile(r'<a\s+(data-v-\w+)=["\'][^"\']*["\']\s+href=["\']javascript:;["\']\s+class=["\']btn_theme["\']>')
match = data_v_pattern.search(page_source)
import random
if match:
    #获取data_v具体值
    data_v = match.group(1)

    # 构建 XPath 表达式
    comment_xpath = f"//a[@{data_v} and @href='javascript:;' and @class='btn_theme' and text()='评价']"
    input_xpath = f"//input[@{data_v}]"
    textarea_xpath = f"//textarea[@{data_v} and @rows='3']"
    hand_in_xpath = f"//button[@{data_v} and @type='button' and @class='el-button theme_color btn el-button--default']/span[text()='提交']"

    # 查找并操作元素

    #反白屏标记，试验功能可能代码有误，不过完成评测没什么问题
    flag_refresh = 30 
    while (flag_refresh > 0):
        try :
            comments = driver.find_elements(By.XPATH, comment_xpath)
            if comments == []:
                flag_refresh = 0;
                print('flag = 0 now')
                break;
            
            for i in comments:
                i.click()
                randomtime = random.uniform(3,5)
                time.sleep(randomtime)
                inputs = driver.find_elements(By.XPATH, input_xpath)
                for input_i in inputs:
                    input_i.send_keys("10")
                textareas = driver.find_elements(By.XPATH, textarea_xpath)
                for text_i in textareas:
                    text_i.clear()
                    text_i.send_keys("无，老师很好")
                hand_in = driver.find_element(By.XPATH, hand_in_xpath)
                hand_in.click()
                time.sleep(randomtime)
                flag_refresh -= 1
        except:
            #如果出现白屏就刷新
            driver.refresh()
            print('刷新一次')
            time.sleep(3)
else:
    print("未找到匹配的 data-v 属性")

'''下学期更新到只需要输入账号和密码就全自动运行的操作'''