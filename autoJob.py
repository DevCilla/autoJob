from playwright.sync_api import sync_playwright
from datetime import datetime

url = ''
url_offer = ''
url_job = ''
login_email = ''
login_pwd = ''

def checkOffer(page):
    newOfferHeader = page.get_by_role("heading", name="New Offers")
    failed = page.get_by_role("heading", name="Sorry, there’s nothing here yet.")
    acceptBtn = page.get_by_role("button", name="Accept")
    count = 0
    while (acceptBtn.is_visible() == False):
        page.reload()
        page.wait_for_load_state()
        count = count + 1
        if(count % 1000 == 0):
            chkTime = datetime.now()
            print(chkTime, ", tried ", count, " times")
            
        newOfferHeader.wait_for()
        if (acceptBtn.is_visible()):
            print(jobTime, " Job received at the ", count, "th trial")
            jobTime = datetime.now()
            acceptBtn.click()
            continue

def run(playwright_elm):
    browser = playwright_elm.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    page.wait_for_url(url)

    # login
    page.get_by_placeholder("E-mail address").fill(login_email)
    page.get_by_placeholder("Password").fill(login_pwd)
    page.get_by_role("button", name="Sign In", exact=True).click()
    page.wait_for_url(url_job)
    page.get_by_role("link", name="Job Offers").click()
    page.wait_for_url(url_offer)

    checkOffer(page)
    #page.pause()

def runJob(elm):
    strTime = datetime.now()
    print("start time:", strTime)
    run(elm)

def endJob(e):
    endTime = datetime.now()
    print('Exception occured')
    print(e)
    print("end time:", endTime)
    
with sync_playwright() as playwright:    
    try:
        runJob(playwright)
    except Exception as e:
        endJob(e)
        runJob(playwright)
