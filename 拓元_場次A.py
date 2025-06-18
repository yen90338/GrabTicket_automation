from selenium import webdriver # 使用chrome的工具
from selenium.webdriver.common.by import By # 找網站中物件的工具
from selenium.webdriver.support.ui import WebDriverWait, Select # 按鈕等待、下拉選單選擇的工具
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time # 如果網站沒跑這麼快，可以用sleep去等待一下

start_time = time.perf_counter()
# 設定 WebDriver
options = webdriver.ChromeOptions()
# 防止 Selenium 被網站偵測
options.add_argument("--disable-blink-features=AutomationControlled")  
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
#  讓瀏覽器更像真實使用者
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")  # 最大化視窗
options.add_argument("--incognito")
# prefs = {"profile.managed_default_content_settings.images": 2} # 拓元不能用不載圖片，因為驗證碼會跑不出來
# options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
refresh_attempts = 0  # 記錄重整次數
wait = WebDriverWait(driver, 10,0.5)
# Tixcraft_活動網址 
EVENT_URL = "Tixcraft_活動網址"
# EVENT_URL = "https://tixcraft.com/ticket/area/25_maydaytp_c/19583"
# EVENT_URL = "https://tixcraft.com/ticket/area/25_maydaytp/19568"
driver.get(EVENT_URL)

# 將 Cookies 字串分割成單個鍵值對
cookie_str = "OptanonAlertBoxClosed=2025-02-27T09:00:31.098Z; __lt__cid=bd30e340-e496-4537-95ec-97a59a27ab1f; _fbp=fb.1.1741916374527.684160686733299275; _ga_P19DY9KTP5=GS1.1.1744789659.1.1.1744789800.60.0.0; _ga_EH3SD80SVC=GS2.1.s1749088044$o1$g1$t1749088133$j41$l0$h0; _gid=GA1.2.1592918486.1749440406; SID=c7ui9lf4qkfv3d26voelhqst4e; _csrf=fb9070ad4de622168b830d4ce15ab4380812003e069170191bb62592672eaa42a%3A2%3A%7Bi%3A0%3Bs%3A5%3A%22_csrf%22%3Bi%3A1%3Bs%3A32%3A%22rz-8UmDpk15cvzrAx_aft_Hann8v0489%22%3B%7D; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jun+12+2025+10%3A32%3A36+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202408.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=f15ff134-a526-4061-aa08-4814040aa754&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&intType=1&geolocation=TW%3BTPE&AwaitingReconsent=false; _ga=GA1.2.1450443288.1740646827; _dc_gtm_UA-51347908-1=1; _ga_C3KRPGTSF6=GS2.1.s1749695556$o61$g1$t1749695556$j60$l0$h0; __gads=ID=c12d05b30b8fa38f:T=1728983409:RT=1749695572:S=ALNI_MYt6SRF1IlYyilNuUnTUsoFVPb-cQ; __gpi=UID=00000f437954bbbb:T=1728983409:RT=1749695572:S=ALNI_MZiPW5ZOoRcndclRApHPwgXxPGVUA; __eoi=ID=e507228201e5365f:T=1744607694:RT=1749695572:S=AA-AfjYDX63VZe1tTXiyl34kYctl"
cookies = []
for cookie in cookie_str.split("; "):
    name, value = cookie.split("=", 1)
    cookies.append({
        "name": name,
        "value": value,
        "domain": "tixcraft.com",  # 根據實際網址修改
        "path": "/",
        "secure": True,
        "httpOnly": False
    })
driver.execute_cdp_cmd("Network.setCookies", {"cookies": cookies})
driver.execute_cdp_cmd("Page.reload", {}) # 用reload原因是tixcraft不會偵測是否登入

def Verify():
    try:        
        input_creditcard = driver.find_element(By.NAME, "checkCode")
        driver.execute_script("arguments[0].value = '524255';", input_creditcard)  # 使用 JavaScript 設定值
        # input_creditcard.send_keys("524255")
        # driver.execute_script("document.getElementsByName('checkCode')[0].value = '524255'")
        # driver.execute_script("document.querySelector('input[name=\"checkCode\"]')?.value = '524255'")  
        # print("點擊送出按鈕...")
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        driver.execute_script("arguments[0].click();", submit_button) # 使用 JavaScript 點擊按鈕
        # submit_button.click()  
        # driver.execute_script("document.querySelector('button[type=\"submit\"]')?.click();")
        # 等JS視窗跳出
        wait.until(EC.alert_is_present())
        alert = Alert(driver)
        # print("彈窗文字:", alert.text)  # 印出提示內容
        alert.accept()  # 點選「確定」
    except Exception as e:
        print(f"Verify發生錯誤: {e}")

def Numconfirm():
    print('選擇區域成功，開始選擇張數和點擊同意...')
    select_element =wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'select[id^="TicketForm_ticketPrice_"]')))
    select = Select(select_element)
    try:
        select.select_by_visible_text("2")
    except:
        last_option_text = select.options[-1].text
        select.select_by_visible_text(last_option_text)
    # print("選擇張數成功...")
    # 等待同意按鈕出現
    # driver.find_element(By.ID,"TicketForm_agree").click() #點確認checkbox
    agree = wait.until(EC.element_to_be_clickable((By.ID, 'TicketForm_agree')))  # 點確認checkbox
    # agree.click()
    driver.execute_script("arguments[0].click();", agree)
    # print("同意點擊成功...")
    verifyCode_element = driver.find_element(By.ID, "TicketForm_verifyCode") # 驗證碼
    verifyCode_element.click() # 點選驗證碼輸入框

print("載入驗證頁面...")
Verify()

# 找到所有 data-id 以 group_ 開頭的 div 元素
group_elements = wait.until(lambda d: d.find_elements(By.CSS_SELECTOR, 'div[data-id^="group_"]'))
group_count = len(group_elements)  # 找到的話是list屬性 需要轉成int，就需要用len()來計算
print(f"共有 {group_count} 個 'group_x' 區塊")

while True:
    success = False  # 記錄是否成功搶票
    # 重整頁面
    if refresh_attempts > 0:
        print(f"所有位置都已售完，第 {refresh_attempts} 次重整頁面...")
        driver.refresh()
        time.sleep(1)
    print("開始選擇區域...")
    for i in range(1, group_count):  # 用fullxpath才能選擇區域（可視實際數量調整）
        ul_xpath = f"/html/body/div[2]/div[1]/div[3]/div/div/div/div[2]/div[2]/ul[{i}]"
        try:
            ul = wait.until(EC.presence_of_element_located((By.XPATH, ul_xpath)))
            li_elements = ul.find_elements(By.TAG_NAME, "li")
            for j, li in enumerate(li_elements):
                try:
                    a_tag = li.find_element(By.TAG_NAME, "a")
                    if a_tag.is_enabled():
                        a_tag.click()
                        print(f"✅ 找到可點擊的區域：ul[{i}] → li[{j+1}]")
                        success = True
                        break
                except:
                    # print(f"❌ ul[{i}] → li[{j+1}] 無 <a>，跳過")
                    continue
            if success:
                break # 成功點擊後，不再嘗試其他 group，直接跳出 i 的迴圈
        except Exception as e:
            # 若ul不存在就跳出外層迴圈
            print(f"無座位ul: {i}，準備Refresh...，錯誤: {str(e)}")
            break  # 若ul不存在就跳出外層迴圈
    if success:
        try:
            Numconfirm()
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f"程式執行時間: {elapsed_time:.4f} 秒")
            input("程式執行完畢，請手動關閉瀏覽器。")      
            break  # 成功搶票後，結束迴圈
        except Exception as e:
            print(f"發生錯誤: {e}")
            input("發生錯誤❌，請手動關閉瀏覽器")
            break
    else:
        # print("所有位置都已售完，重新整理頁面繼續嘗試...")
        refresh_attempts += 1  # 記錄重整次數
