from selenium import webdriver ##使用chrome的工具
from selenium.webdriver.common.by import By ##找網站中物件的工具
from selenium.webdriver.support.ui import WebDriverWait, Select ##按鈕等待、下拉選單選擇的工具
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
import time #如果網站沒跑這麼快，可以用sleep去等待一下
# from datetime import datetime
start_time = time.perf_counter()
# 設定 WebDriver
options = webdriver.ChromeOptions()
#  防止 Selenium 被網站偵測
options.add_argument("--disable-blink-features=AutomationControlled")  
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
#  讓瀏覽器更像真實使用者
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")  # 最大化視窗
# options.add_argument("--disable-infobars")  # 隱藏「Chrome 正由自動測試軟體控制」的提示
# options.add_argument('--ignore-certificate-errors')  # 忽略 SSL 錯誤
# options.add_argument('--ignore-ssl-error')
options.add_argument("--incognito")  # 無痕模式
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
# KKTIX 活動網址  GD 7/11
# EVENT_URL = "https://kktix.com/events/813b9103/registrations/new"
EVENT_URL = "https://kktix.com/events/alanwalkermacau2025/registrations/new"
driver.get(EVENT_URL)

wait = WebDriverWait(driver, 10,0.5)
id_number = "F129335060"
refresh_attempts = 0
# 解決登陸KKTIX google帳號的方式
# driver.delete_all_cookies()
cookie_str = "_fbp=fb.1.1747643644978.785791603208408176; _hjSessionUser_1979059=eyJpZCI6ImY0NzlhOWMzLTAyNDItNTVkYi04MzU0LWRjYjRjMTQ1NjdjZiIsImNyZWF0ZWQiOjE3NDc2NDM2NDQ5NjYsImV4aXN0aW5nIjp0cnVlfQ==; mobileNotVerified=0; _ga_ZQT8HTN6RW=GS2.1.s1748308725$o3$g1$t1748308843$j0$l0$h0; _ga_VT8MP885DG=GS2.1.s1748319644$o4$g0$t1748319644$j60$l0$h592109000$dxREe2YY3-EYLCVMfIgzjcOwHdaNf1hJXaw; _gid=GA1.2.1848632772.1749528018; _ga_FY1FJ045WS=GS2.1.s1749531815$o1$g1$t1749532806$j60$l0$h0; personalInfoNotFinished=0; locale=en; _cfuvid=zEBRrXAQ_sNp405rdbvlZ3eizzWSDY_ohf1ptTMx4RQ-1749694333973-0.0.1.1-604800000; cf_clearance=XUJySyTc53s36xnbv3wBU1j2NM_2Nd87MX7WqpbBom8-1749694340-1.2.1.1-OzAdaR73HG_FzvQpOb2nC3gAAOKQtgB8lwsP8YNBNCLPtsrm9Ak4adWCeVX_fvkG161TJwgJKD6Ii_SNYMUKw8dEGOyUpt67q_oATZwqQMg70Kj7aI7sITRT0ktPZ.mm7iGTBsISZ7jzlM0OC4DZj3BJEw8KbQYKUxFVe8OLFpnPu3h3Yj1eT2r6SrhaCV5O6OhPfizvmgSVCnQZk.Fyv5UQ4CJXb._LSp58MIqGmKWD1FZ4QB0NDluXo7AoCtEk.mrqefgaeTXq5Z8WkPnGZJOipapU2LGi4IFF4CoJnWUadIEpsuO4FIsZV17EE7CsxPyjTiwCb7L2pMKd3IFM7ObnMtDH6IsJagmIZVEhSOqlsqzhT941.mKlVPldZ2jC; user_display_name_v2=%25E9%2598%25BF%25E5%25A8%2581; user_avatar_url_v2=https%3A%2F%2Fwww.gravatar.com%2Favatar%2F521bd44ec019f2dbe5fe6330a9568919.png; user_id_v2=5385468; user_path_v2=%2Fuser%2F5385468; user_time_zone_v2=Asia%2FTaipei; user_time_zone_offset_v2=28800; kktix_session_token_v2=1455bb9f91b59a662dc557eb0d0521b6; _ga_LWVPBSFGF6=GS2.1.s1749777965$o49$g0$t1749777965$j60$l0$h0; XSRF-TOKEN=VPanIh8oSrFBq79EW25yChFPLo%2Be6ncY4RqEU7cXHSrN6BMj2AW003E65KgnhxPi%2F0y8BY4M2PQ1ocPUUuaD6A%3D%3D; __cfwaitingroom=ChhSdExNM01IbVpDaGRaeFNSWDhWTFJnPT0SkAJ1cmZyRjNLMmp0T0dUeHAxdzVuQkNhSnlMc253aExHaGVoNXVTZ01vWTdhL1A4dUQ4Sk44STRQNFZXUHBVY01pOUJFMml2M1J3K0FHU2ZlcVZTd1ltWjU3b1p2ZHg1UGVvaFpsV3hmR0FyeGxoaWZIeVRTT3FOSjJ1ZnlzTXI3NzJtUjFOVUMwZ0VMWlVSbjFuWEQvRUo3aHdVbmFQeVp1OHlYTU15dFZUc1UxVWtyUThPa0paSjZNQlUrMzg0S09MbkRDbFgxOHh4akJ0dG53b0ZpYVR2RXdJSHlGYml1YkxmVXgwWVZuUFdMZXpySTYxOGRjVG0xS2VKR21FY2x4dWhXeTZ1NUxhL1dDVm1IKw%3D%3D; _clck=1i6jbx0%7C2%7Cfwq%7C0%7C1965; _hjSession_1979059=eyJpZCI6Ijc5YjQyZDJhLTVlMzAtNDMzYi04NmRmLWQ4MTA1YTA0NGUwYSIsImMiOjE3NDk3Nzc5NjU0MjMsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MH0=; _ga_SYRTJY65JB=GS2.1.s1749777965$o49$g0$t1749777965$j60$l0$h0; _ga=GA1.2.1709465145.1747643645; _dc_gtm_UA-44784359-1=1; _dc_gtm_null=1; _ga_WZBYP4N1ZG=GS2.2.s1749777965$o46$g0$t1749777965$j60$l0$h0; _clsk=q1wulk%7C1749777966275%7C1%7C1%7Cn.clarity.ms%2Fcollect; _gali=navbar"
cookies = []
for cookie in cookie_str.split("; "):
    name, value = cookie.split("=", 1)
    cookies.append({
        "name": name,
        "value": value,
        "domain": ".kktix.com",  # 根據實際網址修改
        "path": "/",
        "secure": True,
        "httpOnly": False
    })
driver.execute_cdp_cmd("Network.setCookies", {"cookies": cookies})
driver.execute_cdp_cmd("Page.reload", {}) ##不重新刷新頁面，僅更新cookie  KKTIX不登入就無法購票
# driver.refresh()

# ticket_ids = ["ticket_849427","ticket_849429", "ticket_849430", "ticket_849431","ticket_849432","ticket_849433"]
# ticket_ids = ["ticket_874692","ticket_874693"]
ticket_ids = [f"ticket_{i}" for i in range(874692, 874697)] #有可能有很多區域用迴圈方式列出
# ticket_ids = [f"ticket_{i}" for i in range(849438, 849449)]
# print(f"搶票ID: {ticket_ids}")
def purchase_ticket(wait, id_number):
    try:
        # 第二個頁面，等待按鈕可點擊
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-primary.btn-lg.ng-binding.ng-isolate-scope")))
        button.click()
        print("請完成付款!")

#         # 第三個頁面，找到身分證輸入框屬性
        input_number = wait.until(EC.element_to_be_clickable((By.NAME, "idNumber")))
#         # 點選ATM付款
        atm_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="radio"][value="ATM"]')))
        atm_button.click()       
#         # 點選輸入框並輸入身分證號碼
        input_number.click()
        input_number.send_keys(id_number)      
        print("身分證輸入完成！")

#         #點選 credit card 付款
#         driver.find_element(By.NAME, "cardNumberInput").send_keys("信用卡號") ##指定信用卡
#         select_month = Select(driver.find_element(By.NAME, "CardMonth"))
#         select_year = Select(driver.find_element(By.NAME, "CardYear"))
#         select_month.select_by_visible_text("05")
# #         select_month.select_by_value("number:5")
#         select_year.select_by_visible_text("2031")
# #         # select_month.select_by_value("number:2031")
#         driver.find_element(By.NAME, "CVC2").send_keys("358")
#         print("信用卡資料輸入完成!")
    except Exception as e:
        print(f"發生錯誤: {e}")
        
while True:
    success = False  # 記錄是否成功搶票
    # 重整頁面
    if refresh_attempts > 0:
        print(f"第 {refresh_attempts} 次重整頁面...")
        driver.refresh()
        time.sleep(1.5)
    # 同意條款
    agree = wait.until(EC.presence_of_element_located((By.ID, "person_agree_terms")))
    # agree = driver.find_element(By.ID, "person_agree_terms")
    # agree.click()
    driver.execute_script("arguments[0].click();",agree)
    next_set = driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.ng-isolate-scope.btn-primary")
    for ticket_id in ticket_ids: 
        try:
            span_xpath =f'//*[@id="{ticket_id}"]/div/span[4]'
            span_element  = driver.find_element(By.XPATH, span_xpath)
            try:
                input_field = span_element.find_element(By.TAG_NAME, "input")
                if  input_field.is_enabled():#判斷span裡是否有input
                    input_field.clear()  # 先清除文字框內的內容
                    input_field.send_keys("2")  # 輸入張數
                    # driver.find_element(By.CSS_SELECTOR, ".btn.btn-lg.ng-isolate-scope.btn-primary").click()#下一步
                    next_set.click()
                    print(f"✅成功選擇第 {ticket_id} 位置的票")
                    success = True
                    break                
                else:
                    print(f"❌第 {ticket_id} 的位置無<input>，嘗試下一個...")
            except Exception:
                print(f"❌第 {ticket_id} 的位置已售完，嘗試下一個...")    
        except Exception as e:
            print(f"❌第 {ticket_id} 的位置無法選擇，錯誤: {str(e)}")
    print("迴圈已結束，執行下一步...")
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"程式執行時間: {elapsed_time:.4f} 秒")
    if success:
        print("搶票成功！請確認資訊。")
        # purchase_ticket(wait, id_number)
        input("程式執行完畢，請手動關閉瀏覽器。")      
        break  # 成功搶票後，結束迴圈
    else:
        print("所有位置都已售完，重新整理頁面繼續嘗試...")
        refresh_attempts += 1  # 記錄重整次數

   
