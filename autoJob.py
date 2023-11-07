from playwright.sync_api import sync_playwright
from datetime import datetime

url = ''
url_offer = ''
url_job = ''
login_email = ''
login_pwd = ''
cnt = 0
isHeadless = False
startTimeout = 60000
inJobTimeout = 10000

def run(playwright_elm):
    # initialize
    browser = playwright_elm.chromium.launch(headless=isHeadless)
    context = browser.new_context()
    page = context.new_page()        
    page.set_default_navigation_timeout(startTimeout)
    page.goto(url)
    page.wait_for_url(url)
    login(page)

    while cnt < 1000:
        try:            
            checkLogout(page)
            checkOffer(page)
        except Exception as e:
            restartJob(page, e)   


def login(page_elm):    
    print("-----login() start-----") 
    page_elm.get_by_placeholder("E-mail address").fill(login_email)
    page_elm.get_by_placeholder("Password").fill(login_pwd)
    page_elm.get_by_role("button", name="Sign In", exact=True).click()
    page_elm.wait_for_url(url_job)
    loginTime = datetime.now()
    print("finish login time:", loginTime)
    page_elm.set_default_navigation_timeout(inJobTimeout)
    print("-----login() end-----")
    #page.get_by_role("link", name="Job Offers").click()    


def checkOffer(page_elm):
    global cnt
    print("-----checkOffer() start-----")
    page_elm.goto(url_offer)
    page_elm.wait_for_url(url_offer)
    offerHeader = page_elm.get_by_role("heading", name="New Offers")
    noOffer = page_elm.get_by_role("heading", name="Sorry, there’s nothing here yet.")
    acceptBtn = page_elm.get_by_role("button", name="Accept")
    calRunCnt()
    while noOffer.is_visible():
        cnt = cnt + 1
        page_elm.reload()
        page_elm.wait_for_load_state("load")
        offerHeader.wait_for()
        if not noOffer.is_visible():
            page_elm.pause()
        #if acceptBtn.is_visible():
        #    acceptOffer(page_elm, acceptBtn)


def acceptOffer(page_elm, btn_elm):
    print("-----acceptOffer() start-----")
    jobTime = datetime.now()
    print(jobTime, " Job received at the ", cnt, "th trial") 
    btn_elm.click()
    page_elm.wait_for_load_state()
    page_elm.goto(url_offer)
    page_elm.wait_for_url(url_offer)
    print("-----acceptOffer() end-----")


def calRunCnt():
    if cnt < 1:
        pass
    elif (cnt % 50 == 0):
        chkTime = datetime.now()
        print(chkTime, ", tried ", cnt, " times")


def checkLogout(page_elm):
    print("-----checkLogout()-----")
    if not page_elm.url == url:
        pass                
    else:
        logoutTime = datetime.now()
        print(logoutTime, " Website logged out, will login again now.")
        login(page_elm)


def restartJob(page_elm, e):
    print("-----restartJob() start-----")
    endTime = datetime.now()
    print('Exception occured at ', endTime, ", the ", cnt, "th trial")
    print(e)
    page_elm.set_default_navigation_timeout(startTimeout)
    page_elm.goto(url)
    page_elm.wait_for_url(url)
    print("-----restartJob() end-----")
    

with sync_playwright() as playwright:  
    strTime = datetime.now()
    print("start time:", strTime)
    run(playwright) 
