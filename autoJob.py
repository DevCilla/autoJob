from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from datetime import datetime
from threading import Event
import http.client as httplib

url = ''
url_offer = ''
url_job = ''
login_email = ''
login_pwd = ''
cnt = 0
isHeadless = False
#startTimeout = 60000
#inJobTimeout = 10000

def run(playwright_elm):
    # initialize
    browser = playwright_elm.chromium.launch(headless=isHeadless)
    context = browser.new_context()
    page = context.new_page()        
    #page.set_default_navigation_timeout(startTimeout)
    page_elm.goto(url)
    page_elm.wait_for_url(url)
    login(page_elm)

    while True:
        try:            
            #checkLogout(page)
            #page.set_default_navigation_timeout(inJobTimeout)
            checkOffer(page)
        except PlaywrightTimeoutError as timeout_e:
            print(timeout_e)
            endTime = datetime.now()
            print(endTime, ", TIMEOUT when trying the", cnt, "th times.")    
            #page.set_default_navigation_timeout(startTimeout)
            try:
                page.close()
            except:
                pass

            page = context.new_page()      
            restartJob(page)
        except Exception as e:
            curr_t = datetime.now()
            print(curr_t, ", Exception caught when trying the", cnt, "th times, job will be stopped now.")
            print("Reason:", e)
            #Event().wait(waitTime)
              

def login(page_elm):    
    print("-----login() start-----")     
    page_elm.get_by_placeholder("E-mail address").fill(login_email)
    page_elm.get_by_placeholder("Password").fill(login_pwd)
    page_elm.get_by_role("button", name="Sign In", exact=True).click()
    page_elm.wait_for_url(url_job)
    loginTime = datetime.now()
    print("finish login time:", loginTime)
    #page_elm.set_default_navigation_timeout(inJobTimeout)
    print("-----login() end-----")
    #page.get_by_role("link", name="Job Offers").click()    


def checkOffer(page_elm):
    global cnt
    print("-----checkOffer()-----")
    page_elm.goto(url_offer)
    page_elm.wait_for_url(url_offer)
    page_elm.get_by_role("heading", name="New Offers").wait_for()
    offerHeader = page_elm.get_by_role("heading", name="New Offers")
    noOffer = page_elm.get_by_role("heading", name="Sorry, there’s nothing here yet.")    
    while noOffer.is_visible():        
        cnt = cnt + 1
        calRunCnt()
        page_elm.reload()
        page_elm.wait_for_load_state("load")
        offerHeader.wait_for()
        if not noOffer.is_visible():
            offerTime = datetime.now()
            print(offerTime, ", Offer found when trying the", cnt, "th trial.") 
            print(page_elm.content(), file=open("offer_" + initLogFile(), 'a', encoding='utf-8'))     
            page_elm.get_by_role("row").nth(2).get_by_role("cell").nth(0).click()
            print(page_elm.content(), file=open("row_" + initLogFile(), 'a', encoding='utf-8'))
            acceptOffer(page_elm)
            #page_elm.pause()
            #Event().wait(waitTime) # wait for 1 hour
        #if acceptBtn.is_visible():
        #    acceptOffer(page_elm, acceptBtn)


def acceptOffer(page_elm):
    print("-----acceptOffer() start-----")
    acceptBtn = page_elm.get_by_role("button", name="Accept") 
    btn_elm.click()
    page_elm.wait_for_load_state()    
    jobTime = datetime.now()
    print(jobTime, " Job received at the", cnt, "th trial.")  
    print(page_elm.content(), file=open("btn_" + initLogFile(), 'a', encoding='utf-8'))       
    page_elm.goto(url_offer)
    page_elm.wait_for_url(url_offer)
    print("-----acceptOffer() end-----")


def calRunCnt():
    global cnt
    if cnt < 1:
        pass
    elif (cnt % 50 == 0):
        chkTime = datetime.now()
        print(chkTime, ", run counts:", cnt, "times")


def checkLogout(page_elm):
    print("-----checkLogout()-----")
    if (page_elm.url == url):
        logoutTime = datetime.now()
        print(logoutTime, ", logged out when trying the", cnt, "th times, will login again now.")
        login(page_elm)     
    else:
        pass
        

def restartJob(page_elm):
    print("-----restartJob() start-----")    
    if not(checkNetwork()): raise RuntimeError("No Internet connection. Please check your network.")

    page_elm.goto(url)
    page_elm.wait_for_url(url)
    page_elm.get_by_role("button", name="Sign In", exact=True).wait_for()
    signInBtn = page_elm.get_by_role("button", name="Sign In", exact=True)
    #checkLogout(page_elm)
    if ((page_elm.url == url) and (signInBtn.is_visible())):
        logoutTime = datetime.now()
        print(logoutTime, ", logged out when trying the", cnt, "th times, will login again now.")
        login(page_elm)     
    elif ((page_elm.url == url) and not(signInBtn.is_visible())):
        print("Cannot see the Sign In button, reload page...")
        page_elm.reload()
        restartJob(page_elm)
    else:
        pass
    print("-----restartJob() end-----")


def initLogFile():
    fileName = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    fileName = fileName + "_debug.txt"
    return fileName
    

def checkNetwork() -> bool:
    conn = httplib.HTTPSConnection("8.8.8.8", timeout=5)
    try:
        conn.request("HEAD", "/")
        return True
    except Exception:
        return False
    finally:
        conn.close()

with sync_playwright() as playwright:  
    strTime = datetime.now()
    print("start time:", strTime)
    run(playwright) 
