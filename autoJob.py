from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
import http.client as httplib

url_signin = ''
url_welcome = ''
url_offer = ''
url_job = ''
login_email = ''
login_pwd = ''
cnt = 0
isHeadless = True
#startTimeout = 60000
#inJobTimeout = 10000

def run(playwright_elm):
    # initialize
    global cnt
    browser = playwright_elm.chromium.launch(headless=isHeadless)
    context = browser.new_context()    
    while checkNetwork():
        try:            
            page = context.new_page()        
            #page.set_default_navigation_timeout(startTimeout)
            page.goto(url_signin)
            page.wait_for_url(url_signin)
            login(page)
            checkOffer(page)
        except Exception as e:
            curr_t = datetime.now()
            print(curr_t, ", count:", cnt, ", Exception caught:", e)
            screenshotName = "ex-" + initLogFile() + ".png"
            page.screenshot(path=screenshotName, full_page=True)
        finally:
            page.close()    
            print("trying to restart...")
            
              

def login(page_elm):    
    #print("-----login() start-----")
    page_elm.get_by_role("button", name="Sign In", exact=True).wait_for()  
    page_elm.get_by_placeholder("E-mail address").fill(login_email)
    page_elm.get_by_placeholder("Password").fill(login_pwd)
    page_elm.get_by_role("button", name="Sign In", exact=True).click()
    page_elm.wait_for_url(url_job)
    loginTime = datetime.now()
    print(loginTime, "logged in")
    #page_elm.set_default_navigation_timeout(inJobTimeout)
    #print("-----login() end-----")
    #page.get_by_role("link", name="Job Offers").click()    


def checkOffer(page_elm):
    global cnt
    #print("-----checkOffer()-----")
    page_elm.goto(url_offer)
    page_elm.wait_for_url(url_offer)
    page_elm.get_by_role("heading", name="New Offers").wait_for()
    offerHeader = page_elm.get_by_role("heading", name="New Offers")
    noOffer = page_elm.get_by_role("heading", name="Sorry, there’s nothing here yet.")  
    #noOfferFlag =  noOffer.is_visible()
    page_elm.pause()
    while noOffer.is_visible():        
        cnt = cnt + 1
        calRunCnt()
        page_elm.reload()
        page_elm.wait_for_load_state("load")
        offerHeader.wait_for()
        if not noOffer.is_visible():
            offerTime = datetime.now()
            print(offerTime, "count:", cnt, ", Offer found") 
            #print(page_elm.content(), file=open("offer_" + initLogFile(), 'a', encoding='utf-8'))     
            page_elm.get_by_role("row").nth(2).get_by_role("cell").nth(0).click()   
            page_elm.wait_for_load_state()      
            page_elm.get_by_role("row").nth(2).click()    
            acceptOffer(page_elm)
            continue
    


def acceptOffer(page_elm):
    #print("-----acceptOffer() start-----")
    #print(page_elm.content(), file=open("accept_" + initLogFile(), 'a', encoding='utf-8'))
    acceptBtn = page_elm.get_by_role("button", name="Accept") 
    acceptBtn.click()
    page_elm.wait_for_load_state()    
    jobTime = datetime.now()
    print(jobTime, "Offer accepted.")  
    print(page_elm.content(), file=open("accepted_" + initLogFile(), 'a', encoding='utf-8'))       
    page_elm.goto(url_offer)
    page_elm.wait_for_url(url_offer)
    #print("-----acceptOffer() end-----")


def calRunCnt():
    global cnt
    if (cnt % 100 == 0):
        chkTime = datetime.now()
        print(chkTime, "run counts:", cnt, "times")


def initLogFile() -> str:
    fileName = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")[:-3]
    fileName = fileName + "_debug"
    return fileName
    

def checkNetwork() -> bool:
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        endTime = datetime.now()
        print(endTime, "No network connection, please check your network, programme will stop now.")
        return False
    finally:
        conn.close()

with sync_playwright() as playwright:  
    strTime = datetime.now()
    print(strTime, 'started programme...')
    run(playwright) 
        return False
    finally:
        conn.close()

with sync_playwright() as playwright:  
    strTime = datetime.now()
    print("start time:", strTime)
    run(playwright) 
