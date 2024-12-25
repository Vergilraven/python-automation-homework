import time,xlrd,socket
import pyautogui,pyperclip
import paramiko
import subprocess,os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from getpass import getpass
import win32api
# from pywin32_system32 import *
import datetime
import random
import requests,lxml
from bs4 import BeautifulSoup
from picscanner import scanner
from scanpic import baiduscanner
from getpass import getpass
from PIL import Image
import pytesseract
import re

class prefetch:
    def __init__(self):
        self.ipuri = 'https://www.ip138.com/'
        self.website = 'https://ip.tool.chinaz.com/'
        self.chromerui = 'https://chromedriver.storage.googleapis.com/index.html'
        # self.chromeoptions = Options()
        # self.chromeoptions.add_argument('--headless')
        # self.chromeoptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        # self.driverpath = r'C:\Program Files\Python310\Scripts\chromedriver.exe'
        # self.browser = webdriver.Chrome(executable_path=self.driverpath,options=self.chromeoptions)
        # self.browser = webdriver.Chrome()
        self.ipaddr = []
        self.versionlist = []
        self.chrome_download_path = 'chrome://downloads/'

    # @property
    # def getlocalip(self):
    #     print('请稍后正在获取本机的公网ip地址')
    #     self.browser.get(self.ipuri)
    #     input_ipaddr = self.browser.find_element(By.ID,'kw')
    #     input_ipaddr.send_keys('ip')
    #     input_ipaddr.send_keys(Keys.ENTER)
    #     wait_time = WebDriverWait(self.browser, 10)
    #     wait_time.until(EC.presence_of_all_elements_located((By.ID, 'content_left')))
    #     ip_class = self.browser.find_element(By.CLASS_NAME,'c-gap-right')
    #     convert_ip_class = ip_class.text
    #     ip_addr = convert_ip_class.split(':')[1]
    #     return ip_addr

    @property
    def get_external_ip(self):
        try:
            website_response = requests.get(url=self.website)
            website_soup = BeautifulSoup(website_response.text, 'lxml')
            ip_addr = website_soup.find("dd", class_="fz24").get_text()
            return ip_addr
        except:
            return None

    # def clean_chrome_download(self):
    #     self.browser.get(self.chrome_download_path)
    #     time.sleep(50)

class automation(prefetch):
    def __init__(self,devops,username,password):
        self.filepath = r'D:\Files\own.xlsx'
        self.xlbook = xlrd.open_workbook(self.filepath)
        self.secretdic = {}
        self.devops = devops
        self.username = username
        self.password = password
        self.jumpserver = 'XXX.XXX.XXX.XXX'
        self.aliyunurl = 'https://account.aliyun.com/'
        self.driverpath = r'C:\Program Files\Python310\Scripts\chromedriver.exe'

        self.runner = {
            'jenkins': self.jenkinslogin,
            'github': self.githublogin,
            'aliyun': self.aliyunlogin,
            'aws': self.awslogin
        }
        self.left = None
        self.top = None
        self.width = None
        self.height = None
        self.feature_list = []
        self.chromepath = r'C:\Program Files\Google\Chrome\Application'
        self.chromexcute = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        self.google_endpoint = 'https://chromedriver.storage.googleapis.com'
        self.google_webpath = '/index.html'
        self.checkuri = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_'
        self.chrome_version_list = []
        self.picture_save = r'D:\Scripts\python\scanpicture\aliyun_webpage'
        self.header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"}
        self.chrome_download_path = 'chrome://downloads/'
        self.tag_flag = '>'

    def main(self):
        # self.checkchrome()
        # self.cleantrash()
        run = self.runner.get(self.devops)
        if run:
            run()
        else:
            print(f"{run} 任务有错误")
            import sys
            sys.exit()

    def cleantrash(self):
        # parameter = '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like GeSjtu@1997cko) Chrome/111.0.0.0 Safari/537.36"'
        win32api.ShellExecute(0,'open',self.chromexcute,self.chrome_download_path,'',1)
        clean_button_coordinate = (2490,195)
        clean_all_button_coordinate = (2299,204)
        pyautogui.leftClick(x=clean_button_coordinate[0],y=clean_button_coordinate[1],duration=3)
        pyautogui.leftClick(x=clean_all_button_coordinate[0],y=clean_all_button_coordinate[1],duration=3)


    def checkchrome(self):
        import requests,json,re,lxml
        from bs4 import BeautifulSoup
        webdriver_version = webdriver.__version__
        print('webdriver的版本为: ',webdriver_version)
        os.chdir(self.chromepath)
        dir_result = os.listdir()
        dir_loop = len(dir_result)

        try:
            gooogle_response = requests.get(self.google_endpoint)
            google_status_code = gooogle_response.status_code
        except (ConnectionError,ConnectionRefusedError) as e:
            raise e

        if google_status_code == 200:
            chrome_version_list = ['70','72','73','74','75','76','77','78','79','80','81','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112']
            while True:
                last_num_version = str(chrome_version_list[-1])
                convert_uri = self.checkuri + last_num_version
                page_text = requests.get(url=convert_uri, headers=self.header).text
                if len(page_text) <= 13:
                    print('这个版本已经存在还不是最新的',page_text,'正在更新本地列表')
                    local_version_list = int(last_num_version) + 1
                    chrome_version_list.append(str(local_version_list))
                    print('更新完成之后的列表为:',chrome_version_list)
                elif len(page_text) >= 13:
                    print('删除末尾版本')
                    chrome_version_list.remove(str(local_version_list))
                    print('正确的版本信息为:',chrome_version_list)
                    break
                else:
                    break

        elif google_status_code == 400:
            print('谷歌的状态码出现4XX,正在启动架构师的分析策略')

        else:
            print('出现了5XX,意料之外的情况,现在还搞不定......')

        loop_inital = 0
        chrome_version_list = ['2','70','72','73','74','75','76','77','78','79','80','81','83','84','85','86','87','88','89','90','91','92','93','94','95','96','97','98','99','100','101','102','103','104','105','106','107','108','109','110','111','112','113']
        while loop_inital < dir_loop:
            convert_res = dir_result[loop_inital]
            inital_split_res = convert_res.split(".")[0]
            convert_version_res = convert_res.split(".")[0:4]
            if inital_split_res in chrome_version_list:
                current_version = str(convert_version_res[0]) + "." +str(convert_version_res[1]) + "." + str(convert_version_res[2]) + "." + str(convert_version_res[3])
                print('当前Chrome浏览器的版本为: ',current_version)
            else:
                pass
            loop_inital += 1

    def jenkinslogin(self):
        vpn_result = os.popen('tasklist | findstr "openvpn"')
        con_vpn = vpn_result.readlines()
        vpn_result.close()

        if con_vpn == []:
            subprocess.run(r'C:\Program Files\OpenVPN\bin\openvpn-gui.exe')
        else:
            pass

        pic_path = r'D:\Lynmax\Workspace\Daily\Scripts\python\scanpicture'
        os.chdir(pic_path)
        ip = super().getlocalip
        print(ip)
        pic_result = os.listdir()

        # 双击终端
        pic_first = pic_result[0]
        x1,y1 = pyautogui.locateCenterOnScreen(pic_first,confidence=0.9)
        pyautogui.click(x=x1,y=y1,button="left")
        time.sleep(1)

        pic_second = pic_result[1]
        x2,y2 = pyautogui.locateCenterOnScreen(pic_second,confidence=0.9)
        pyautogui.doubleClick(x=x2,y=y2,button="left")
        time.sleep(1)

        # 单击用户名 传递参数
        pyautogui.click(x=1289,y=712,button="left")
        pyperclip.copy('')
        pyautogui.hotkey('ctrl','v')
        time.sleep(1)

        # 单击密码 传递参数
        pyautogui.click(x=1304,y=772,button="left")
        pyperclip.copy('')
        pyautogui.hotkey('ctrl','v')
        time.sleep(1)

        pic_third = pic_result[2]
        x3,y3 = pyautogui.locateCenterOnScreen(pic_third,confidence=0.9)
        pyautogui.click(x=x3,y=y3,button="left")
        time.sleep(1)

        pic_fourth = pic_result[3]
        x4,y4 = pyautogui.locateCenterOnScreen(pic_fourth,confidence=0.9)
        pyautogui.click(x=x4,y=y4,button="left")
        time.sleep(1)


        sheetname = self.xlbook.sheets()[0]
        self.secretdic = {}
        username = sheetname.col_values(4)[7]
        password = sheetname.col_values(5)[7]

        initalip = sheetname.col_values(1)[7]
        convertip = str(initalip).split("(")[0]

        initalport = sheetname.col_values(3)[7]
        convertport = str(initalport).split(":")[1]

        finalip = "http://" + convertip + ":" + convertport
        self.secretdic['ip'] = finalip
        self.secretdic['username'] = username
        self.secretdic['passwd'] = password
        self.jenkinstask()

    def jenkinstask(self):
        ipaddr = self.secretdic['ip']
        username = self.secretdic['username']
        passwd = self.secretdic['passwd']
        print('当前地址为: ',ipaddr)
        self.browser.implicitly_wait(10)
        self.browser.get(ipaddr)
        input_username = self.browser.find_element(By.ID,'j_username')
        input_username.send_keys(username)
        input_passwd = self.browser.find_element(By.XPATH,'//input[@name="j_password"]')
        input_passwd.send_keys(passwd)
        self.browser.find_element(By.XPATH,"//button[@name='Submit']").click()
        print('目前上线任务功能还在持续开发中.....')
        time.sleep(10)

    def githublogin(self):
        username = '691267837@qq.com'
        password = getpass('请输入您的密码: ')
        self.secretdic['ip'] = 'https://www.github.com/login'
        self.secretdic['username'] = username
        self.secretdic['passwd'] = password
        repositry_uri = input('Enter the repos uri: ')
        self.githubtask()

    def githubtask(self):
        ipaddr = self.secretdic['ip']
        username = self.secretdic['username']
        passwd = self.secretdic['passwd']
        self.browser.implicitly_wait(10)
        self.browser.get(ipaddr)
        input_username = self.browser.find_element(By.ID,'login_field')
        input_username.send_keys(username)
        input_passwd = self.browser.find_element(By.ID,'password')
        input_passwd.send_keys(passwd)
        self.browser.find_element(By.CSS_SELECTOR,"input[value='Sign in']").click()

    def aliyunlogin(self):
        # 这段代码是读取公司的excel账密时候运行的
        # sheetname = self.xlbook.sheets()[0]
        # self.secretdic = {}
        # id = sheetname.col_values(2)[47]
        # secret_key = sheetname.col_values(2)[48]
        # self.secretdic['username'] = id
        # self.secretdic['passwd'] = secret_key

        # 这段代码是自己登录时候用到的
        self.secretdic['username'] = self.username
        self.secretdic['passwd'] = self.password
        self.aliyuntask()

    def aliyuntask(self):
        # current_month = datetime.datetime.now().strftime('%Y-%m-%d')
        parameter = '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like GeSjtu@1997cko) Chrome/111.0.0.0 Safari/537.36"'
        final_parameter = parameter + ' ' + self.aliyunurl
        win32api.ShellExecute(0,'open',self.chromexcute,final_parameter,'',1)
        time.sleep(1)
        controller = {
            'login': self.aliyunwebpage,
            'console': self.aliyunconsole,
            'billing': self.aliyunbilling,
            'import': self.aliyunimport,
            'check': self.aliyuncheck,
            'refresh': self.aliyunrefresh
        }
        controller_keys = controller.keys()
        convert_controller_keys = list(controller_keys)
        count = 0
        while count < len(convert_controller_keys):
            controller_result = controller.get(convert_controller_keys[count])
            if controller_result:
                controller_result()
            else:
                print(f"{controller_result} 无法运行程序")
                import sys
                sys.exit()
            count += 1

    def printscreencheck(self):
        # 用于检查截图的函数
        # 保持每一次检测都是干净的目录
        clean_dir_res = os.listdir(self.picture_save)
        if clean_dir_res == []:
            pass
        else:
            count_clean = 0
            while count_clean < len(clean_dir_res):
                convert_clean_file_name = os.path.join(self.picture_save,str(clean_dir_res[count_clean]))
                os.remove(convert_clean_file_name)
                count_clean += 1
        # 传两个坐标进来自动做运算
        current_path = os.getcwd()
        print('当前路径在:',current_path)
        if current_path != self.picture_save:
            os.chdir(self.picture_save)
            print('正在切换路径',self.picture_save)
        else:
            pass
        number_pattern = r'^[-+]?[0-9]+(\.[0-9]+)?$'
        while True:
            print('接受到的四个参数为:',self.left,self.top,self.width,self.height)
            current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            laptop_screen_check = pyautogui.screenshot(region=(self.left,self.top,self.width,self.height))
            print('正在检查页面截图...','将文件保存至',self.picture_save)
            laptop_screen_picture = current_time + '.png'
            laptop_screen_check.save(laptop_screen_picture)
            print('检测图片名称:',laptop_screen_check)
            instance = baiduscanner(self.picture_save)
            scan_value = instance.get_picture_result
            convert_scan_value = [y for y in scan_value]
            convert_executable_res = [x for x in convert_scan_value if x in self.feature_list]
            if convert_executable_res == []:
                os.remove(laptop_screen_picture)
                time.sleep(1)
                continue
            else:
                os.remove(laptop_screen_picture)
                break

    def aliyunwebpage(self):
        # (1661,655) (1765,692)
        print('正在识别是否网页加载出来')
        self.left = 1661
        self.top = 655
        self.width = 104
        self.height = 37
        self.feature_list.append('登')
        self.feature_list.append('录')
        print(self.feature_list)
        self.printscreencheck()

        print(self.tag_flag * 88)
        print('正在输入用户名')
        x1 = 1548
        y1 = 441
        time.sleep(3)
        pyautogui.moveTo(x=x1,y=y1)
        pyautogui.click(button="left")
        time.sleep(1)
        pyperclip.copy(self.secretdic['username'])
        pyautogui.hotkey('ctrl','v')
        time.sleep(1)

        print(self.tag_flag * 88)
        print('正在输入密码')
        x2 = 1521
        y2 = 517
        pyautogui.moveTo(x=x2,y=y2)
        pyautogui.click(button="left")
        pyperclip.copy(self.secretdic['passwd'])
        pyautogui.hotkey('ctrl','v')
        time.sleep(3)

        print('正在点击登录按钮')
        x3 = 1671
        y3 = 670
        pyautogui.moveTo(x=x3,y=y3)
        pyautogui.click(button="left")
        time.sleep(3)

        left = 1450
        top = 581
        width = 482
        height = 51

        '''
        (1450,581) (1932,632)
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        所包含得左上角坐标 以及宽度和高度
        '''
        aliyun_pass_check = pyautogui.screenshot(region=(left,top,width,height))
        print('正在获取阿里云登录页面截图...','将文件保存至',self.picture_save)

        current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        # screen_picture = current_time + '.jpg'
        screen_picture = current_time + '.png'
        aliyun_pass_check.save(self.picture_save + '\\' + screen_picture)
        aliyun_pass_check_image_path = self.picture_save + '\\' + screen_picture
        print('滑动条检测图片存放位置:',aliyun_pass_check_image_path)

        feature_value = ['请','按','住','滑','块','拖','动','到','最','右','边']
        aliyun_pass_check_image = scanner(self.picture_save,screen_picture)
        aliyun_pass_check_text = aliyun_pass_check_image.cv2_convert_text
        action_result = [y for y in aliyun_pass_check_text if y in feature_value]
        print('识别结果为',action_result)

        if action_result == []:
            print('这次没有验证条')
        else:
            print('进度条拉起来')
            print('=>'*68)
            slide_windows_x1 = 1478
            slide_windows_y = 605
            slide_windows_x2 = 1604
            slide_windows_max = 1931
            pyautogui.leftClick(x=slide_windows_x1,y=slide_windows_y)
            # time.sleep(0.5)
            pyautogui.dragTo(x=slide_windows_x2,y=slide_windows_y,duration=3,button='left')
            time.sleep(0.5)
            pyautogui.leftClick(x=slide_windows_x1,y=slide_windows_y)
            pyautogui.dragTo(x=slide_windows_max,y=slide_windows_y,duration=3,button='left')
            time.sleep(0.5)
            print('正在点击登录按钮')
            x3 = 1678
            y3 = 665
            pyautogui.moveTo(x=x3,y=y3)
            pyautogui.click(button="left")
            time.sleep(3)

    def aliyunconsole(self):
        print('正在登录控制台')
        controller_pic_path = r'D:\Scripts\python\scanpicture\aliyunlogin'
        os.chdir(controller_pic_path)
        controller_pic_name = 'controller.png'
        controller_x,controller_y = pyautogui.locateCenterOnScreen(controller_pic_name,confidence=0.9)
        pyautogui.click(x=controller_x,y=controller_y,button="left")

        print('正在识别是否网页加载出来')
        self.left = 1215
        self.top = 128
        self.width = 38 #1257
        self.height = 28 #156
        self.feature_list.append('费')
        self.feature_list.append('用')
        print(self.feature_list)
        self.printscreencheck()

        print(self.tag_flag * 88)
        print('正在点击至费用')
        bill_x2 = 1227
        bill_y2 = 143
        pyautogui.click(x=bill_x2,y=bill_y2,button="left")

    def aliyunbilling(self):
        time.sleep(3)
        print('正在向下移动网页')
        pyautogui.hotkey('down')

        time.sleep(0.5)
        print('正在点击我的订单')
        # 可以选择账单详情 或者 我的订单
        #(92,1350)
        bill_list_x = 94
        bill_list_y = 1298
        pyautogui.moveTo(x=bill_list_x,y=bill_list_y)
        pyautogui.leftClick()

        print('正在点击时间范围')
        time_range_x = 1702
        time_range_y = 405
        pyautogui.moveTo(x=time_range_x,y=time_range_y,duration=3)
        pyautogui.leftClick()
        time.sleep(0.5)

        print('正在传入时间参数')
        current_date = datetime.date.today()
        # 可以选择时间节点,当前计算半年的时间范围
        half_year = datetime.timedelta(days=365/2)
        last_month = datetime.timedelta(days=31)
        half_year_before = current_date - half_year
        last_month_before = current_date - last_month
        start_day_num = '-01'
        convert_last_year = str(half_year_before).split('-')[0:2]

        print('正在键入去年的数据')
        last_year_final_date = "-".join(convert_last_year) + start_day_num
        time_range_x1 = 1237
        time_range_y1 = 414
        pyautogui.moveTo(x=time_range_x1,y=time_range_y1,duration=3)
        pyautogui.leftClick()
        pyperclip.copy(last_year_final_date)
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','v')
        time.sleep(0.1)
        print('正在键入上个月的日期')
        '''
        1718 416
        '''
        time_range_x1 = 1718
        time_range_y1 = 416
        pyautogui.moveTo(x=time_range_x1,y=time_range_y1,duration=3)
        pyautogui.leftClick()
        pyperclip.copy(str(last_month_before))
        pyautogui.hotkey('ctrl','a')
        pyautogui.hotkey('ctrl','v')
        time.sleep(0.5)

        '''
        2001 863
        '''
        print('正在点击确定按钮')
        makesure_x = 2001
        makesure_y = 863
        pyautogui.moveTo(x=makesure_x,y=makesure_y,duration=3)
        pyautogui.leftClick()

        '''
        1180 502
        '''
        # 搜索按钮点击
        print('正在点击搜索按钮')
        search_x = 1181
        search_y = 466
        pyautogui.moveTo(x=search_x,y=search_y,duration=3)
        pyautogui.leftClick()

    def aliyunimport(self):
        # 导出收费项目统计
        print('正在为您导出阿里云我的订单数据统计')
        # 选择导出按钮
        print('正在点击导出按钮')
        picture_path = r'D:\Scripts\python\scanpicture\aliyunlogin'
        os.chdir(picture_path)
        import_button_pic = 'import.png'
        import_button_x, import_button_y =  pyautogui.locateCenterOnScreen(import_button_pic,confidence=0.9)
        pyautogui.leftClick(x=import_button_x,y=import_button_y,duration=3)
        time.sleep(1)

        # 暂时无法分析得到网页元素的判断条件
        print('正在截屏识别对应导出验证码,现在未知阿里云官方是否会调整网页Ui,坐标写死')
        # (876,718) (1024,770)
        import_code_coordinate_list = [(998,713),(1207,806)]
        import_code_left = 876 # 1045  # 1064
        import_code_top =  718 # 743  # 794
        import_code_width = 148 # 163 # 140
        import_code_height = 52 # 59 # 58

        import_code_pic = pyautogui.screenshot(region=(import_code_left,import_code_top,import_code_width,import_code_height))
        screen_current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        import_code_screen_pic = 'verification' + screen_current_time + '.png'
        import_code_pic.save(self.picture_save + '/' + import_code_screen_pic)
        verification_pass_check_image = baiduscanner(self.picture_save)
        verification_pass_check_text = verification_pass_check_image.get_picture_result
        print('验证码识别结果为:',verification_pass_check_text)


        if verification_pass_check_text == ' ':
            # 1288 828
            while True:
                print('正在不停地点击看不清楚,是真的看不清楚')
                have_no_idea_result_x = 1288
                have_no_idea_result_y = 828
                pyautogui.click(x=have_no_idea_result_x,y=have_no_idea_result_y,button="left")
                import_code_pic = pyautogui.screenshot(region=(import_code_left,import_code_top,import_code_width,import_code_height))
                screen_current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                import_code_screen_pic = 'verification' + screen_current_time + '.png'
                import_code_pic.save(self.picture_save + '/' + import_code_screen_pic)
                verification_pass_check_image = scanner(self.picture_save,import_code_screen_pic)
                verification_pass_check_text = verification_pass_check_image.cv2_convert_text

                if verification_pass_check_text != []:
                    print('正在传递验证码')
                    verify_code_list = [(784,736)]
                    verify_code_window_x = verify_code_list[0][0]
                    verify_code_window_y = verify_code_list[0][1]
                    pyautogui.leftClick(x=verify_code_window_x,y=verify_code_window_y,duration=3)
                    pyperclip.copy(verification_pass_check_text)
                    pyautogui.hotkey('ctrl','v')
                    break

                else:
                    print('启动无限循环大法')
                    continue
        elif verification_pass_check_text == []:
            # 1288 828
            while True:
                print('正在不停地点击看不清楚,是真的看不清楚')
                have_no_idea_result_x = 1288
                have_no_idea_result_y = 828
                pyautogui.click(x=have_no_idea_result_x,y=have_no_idea_result_y,button="left")
                import_code_pic = pyautogui.screenshot(region=(import_code_left,import_code_top,import_code_width,import_code_height))
                screen_current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                import_code_screen_pic = 'verification' + screen_current_time + '.png'
                import_code_pic.save(self.picture_save + '/' + import_code_screen_pic)
                verification_pass_check_image = scanner(self.picture_save,import_code_screen_pic)
                verification_pass_check_text = verification_pass_check_image.cv2_convert_text

                if verification_pass_check_text != []:
                    print('正在传递验证码')
                    verify_code_list = [(784,736)]
                    verify_code_window_x = verify_code_list[0][0]
                    verify_code_window_y = verify_code_list[0][1]
                    pyautogui.leftClick(x=verify_code_window_x,y=verify_code_window_y,duration=3)
                    pyperclip.copy(verification_pass_check_text)
                    pyautogui.hotkey('ctrl','v')
                    break
                else:
                    print('启动无限循环大法')
                    continue
        else:
            print('正在传递验证码')
            verify_code_list = [(784,736)]
            verify_code_window_x = verify_code_list[0][0]
            verify_code_window_y = verify_code_list[0][1]
            pyautogui.leftClick(x=verify_code_window_x,y=verify_code_window_y,duration=3)
            pyperclip.copy(verification_pass_check_text)
            pyautogui.hotkey('ctrl','v')

        print('正在点击确定')
        print('正在点击确定按钮为您导出阿里云我的订单账单')
        ding_pic_path = r'D:\Scripts\python\scanpicture\aliyunlogin'
        os.chdir(ding_pic_path)
        ding_button_pic = 'dingpic.png'
        ding_button_x,ding_button_y = pyautogui.locateCenterOnScreen(ding_button_pic,confidence=0.9)
        pyautogui.click(x=ding_button_x,y=ding_button_y,button="left")

    def aliyuncheck(self):
        picture_path = r'D:\Scripts\python\scanpicture\aliyunlogin'
        if os.getcwd() != picture_path:
            os.chdir(picture_path)
        else:
            pass
        while True:
            print('正在检测验证码正确与否')
            time.sleep(0.5)
            result_code_left = 706
            result_code_top = 676
            result_code_width = 114
            result_code_height = 38
            result_code_check = pyautogui.screenshot(region=(result_code_left,result_code_top,result_code_width,result_code_height))
            check_current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            result_code_screen_pic = 'verification' + check_current_time + '.png'
            result_code_check.save(self.picture_save + '/' + result_code_screen_pic)
            verification_result_check_image = baiduscanner(self.picture_save)
            verification_result_check_text = verification_result_check_image.get_picture_result
            print(verification_result_check_text)
            print('*'*88)
            verification_result_list = ['验','证','码','错','误']
            # 下面这段代码有点小BUG
            final_check_result = [z for z in verification_result_check_text if z in verification_result_list]
            print(final_check_result)
            print('*'*88)
            if final_check_result == []:
                break
            else:
                print('正在点击关闭')
                # (1404,845) 关闭
                turn_off_x = 1404
                turn_off_y = 838
                pyautogui.leftClick(x=turn_off_x,y=turn_off_y,duration=3)
                time.sleep(0.2)

                print('再次点击导出订单数据按钮')
                import_code_left = 2059
                import_code_top =  498
                pyautogui.leftClick(x=import_code_left,y=import_code_top,duration=3)
                import_code_left = 876 # 1045  # 1064
                import_code_top =  718 # 743  # 794
                import_code_width = 148 # 163 # 140
                import_code_height = 52 # 59 # 58
                print('正在截取验证码是否正确的截图')
                import_code_pic = pyautogui.screenshot(region=(import_code_left,import_code_top,import_code_width,import_code_height))
                screen_current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                import_code_screen_pic = 'verification' + screen_current_time + '.png'
                import_code_pic.save(self.picture_save + '/' + import_code_screen_pic)
                verification_pass_check_image = baiduscanner(self.picture_save)
                verification_pass_check_text = verification_pass_check_image.get_picture_result
                print('验证码识别结果为:',verification_pass_check_text)
                verification_result_list = ['验','证','码','错','误']
                # 下面这段代码有点小BUG
                final_check_result = [z for z in verification_result_check_text if z in verification_result_list]
                print(final_check_result)
                if final_check_result == []:
                    print('正在点击确定按钮为您导出阿里云我的订单账单')
                    ding_button_pic = 'dingpic.png'
                    ding_button_x,ding_button_y = pyautogui.locateCenterOnScreen(ding_button_pic,confidence=0.9)
                    pyautogui.click(x=ding_button_x,y=ding_button_y,button="left")
                    break
                else:
                    import_code_left = 876 # 1045  # 1064
                    import_code_top =  718 # 743  # 794
                    import_code_width = 148 # 163 # 140
                    import_code_height = 52 # 59 # 58
                    import_code_pic = pyautogui.screenshot(region=(import_code_left,import_code_top,import_code_width,import_code_height))
                    screen_current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                    import_code_screen_pic = 'verification' + screen_current_time + '.png'
                    import_code_pic.save(self.picture_save + '/' + import_code_screen_pic)
                    verification_pass_check_image = baiduscanner(self.picture_save)
                    verification_pass_check_text = verification_pass_check_image.get_picture_result
                    print('验证码识别结果为:',verification_pass_check_text)
                    pass
                print('正在传递验证码')
                verify_code_window_x = 792 #891 #890  # 883
                verify_code_window_y = 737 #773 #826  # 824
                pyautogui.leftClick(x=verify_code_window_x,y=verify_code_window_y,duration=3)
                pyperclip.copy(verification_pass_check_text)
                pyautogui.hotkey('ctrl','v')
                '''
                1218,848
                '''
                print('正在点击确定按钮为您导出阿里云我的订单账单')
                ding_button_x = 1218
                ding_button_y = 848
                pyautogui.click(x=ding_button_x,y=ding_button_y,button="left")

    def aliyunrefresh(self):
        print('开始截取生成状态的动作')
        #往左是变小
        while True:
            time.sleep(1)
            coordinate_list = []
            coordinate_left_top = (1452,463)
            coordinate_right_low = (1591,510)
            coordinate_list.append(coordinate_left_top)
            coordinate_list.append(coordinate_right_low)
            # 元组方法精准匹配直接切片的
            status_feature_tuple = ('文件生成中')
            # 综上所述列表推导式判断是最为*偷懒*的办法，分情况而定元组判断较为精准因为是做切片的,是所有字都匹配时候
            status_feature_list = [status_feature_tuple[0],status_feature_tuple[1:5],status_feature_tuple[1:4],status_feature_tuple[1:3],status_feature_tuple[0:4]]

            check_tag = '-'
            print(f'{check_tag*88}')
            file_status_left = coordinate_list[0][0]
            print('生成状态的最左坐标点为:',str(file_status_left))
            file_status_top =  coordinate_list[0][1]
            print('生成状态的最高坐标点为:',str(file_status_top))
            file_status_width =  coordinate_list[1][0] - coordinate_list[0][0]
            print('生成状态的宽度为:',str(file_status_width))
            file_status_height = coordinate_list[1][1] - coordinate_list[0][1]
            print('生成状态的高度为:',str(file_status_height))
            print(f'{check_tag*88}')
            clean_path = r'D:\Scripts\python\scanpicture\aliyun_webpage'
            clean_dir_res = os.listdir(clean_path)
            count_clean = 0
            while count_clean < len(clean_dir_res):
                convert_clean_file_name = os.path.join(clean_path,str(clean_dir_res[count_clean]))
                os.remove(convert_clean_file_name)
                count_clean += 1
            file_status_pic = pyautogui.screenshot(region=(file_status_left,file_status_top,file_status_width,file_status_height))
            file_status_current_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
            file_status_screen_pic = 'status' + file_status_current_time + '.png'
            file_status_pic.save(self.picture_save + '/' + file_status_screen_pic)
            file_status_check_image = baiduscanner(self.picture_save)
            file_status_check_text = file_status_check_image.get_picture_result
            print('百度api返回的结果为:',file_status_check_text,type(file_status_check_text))
            check_tag = '+'
            print(f'{check_tag*88}')

            print('元组特征值为:',status_feature_tuple[0:5])
            # print('列表推导式特征值为:',str(convert_status_feature_list))
            convert_status_feature_list = [z for z in file_status_check_text if z in status_feature_list]
            if convert_status_feature_list != []:
            # if file_status_check_text == status_feature_tuple[0:5]:
                print('还在生成')
                time.sleep(0.1)
                print('开始执行点击刷新动作')
                static_coordinate = (1939,248)
                pyautogui.moveTo(x=static_coordinate[0],y=static_coordinate[1])
                pyautogui.leftClick()
                pass
            else:
                print('已经生成')
                print('正在为您传入坐标矩阵')
                download_button_coordinate = (2011,476)
                print('正在点击下载按钮')
                pyautogui.moveTo(x=download_button_coordinate[0],y=download_button_coordinate[1])
                pyautogui.leftClick()
                break

    def aliyundetailsbill(self):
        print('正在点击收支明细')
        print('正在为您分析账单详情,统计月收费量情况')
        print('导入模板中......,全自动分析账单中......')

    def awslogin(self):
        print('还在开发...')

    def awstask(self):
        print('还在开发...')

if __name__ == '__main__':
    '''上线任务
    拉取代码任务
    回滚任务
    '''
    # prefetch自测
    # chromedriver = prefetch()
    # chromedriver.clean_chrome_download()
    # automation类的自测
    login_account = ""
    print('当前登录用户名为:',login_account)
    login_passwd = getpass("请输入您的账号密码: ")
    # devops_command = 'jenkins'
    devops_command = 'aliyun'
    #task_name = '上线'
    aliyunbill = automation(devops_command,login_account,login_passwd)
    aliyunbill.main()
