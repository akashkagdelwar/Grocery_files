import time
import requests
import json
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
import pandas as pd
from datetime import datetime
import re
from apscheduler.schedulers.background import BackgroundScheduler
from onedrive import upload_file,ctx
# from pytz import 
# Define the list of items to check
items_to_check = ['crv', 'oz', 'fz', 'count', 'ounce', 'fl',
                  'gallon', 'ct', 'lb', 'liter', 'lt', 'pound', 'kg', 'ml']

items_to_check = [item[::-1] for item in items_to_check]

print(items_to_check)

# Create a regex pattern to match any number followed by an element from the list in reverse
pattern = r'(' + '|'.join(re.escape(item)
                          for item in items_to_check) + r')\s*(\d+(?:\.\d+)?)'


def find_matches_reverse(text):
    reversed_text = text[::-1]  # Reverse the input string
    matches = re.findall(pattern, reversed_text, re.IGNORECASE)
    return matches


headers_dict = {
    "authority": "www.jewelosco.com",
    "method": "GET",
    "path": "/shop/aisles.3441.html",
    "scheme": "https",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "max-age=0",
    "Referer": "https://www.jewelosco.com/",
    "Sec-Ch-Ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}


def trim_and_pad(number):
    # Convert the number to a string and remove the last character
    if number:
        number = int(number)
        trimmed_number = str(number)
        # Calculate how many zeros to add at the start
        zeros_to_add = 13 - len(trimmed_number)
        # Add the required number of zeros at the start
        modified_number = str('0' * zeros_to_add) + str(trimmed_number)
        return str(modified_number)
    else:
        return None


# coo = '''visid_incap_1990338=FgRtofFoQEeAhZHQPiU143JN52QAAAAAQUIPAAAAAAAkHWC8ue2j7fIRfzGZ9v1A; absVisitorId=ed6d4075-ba33-4e2c-bc93-28ebab679e5d; OptanonAlertBoxClosed=2023-08-24T12:33:33.078Z; SWY_SHARED_SESSION_INFO=%7B%22info%22%3A%7B%22COMMON%22%3A%7B%22userType%22%3A%22G%22%2C%22zipcode%22%3A%2260657%22%2C%22banner%22%3A%22jewelosco%22%2C%22preference%22%3A%22J4U%22%2C%22Selection%22%3A%22default%22%2C%22userData%22%3A%7B%7D%2C%22grsSessionId%22%3A%22f45068a8-aa1f-414e-9b3e-5103ab503b9a%22%7D%2C%22J4U%22%3A%7B%22storeId%22%3A%223441%22%2C%22zipcode%22%3A%2260657%22%2C%22userData%22%3A%7B%7D%7D%2C%22SHOP%22%3A%7B%22storeId%22%3A%223441%22%2C%22zipcode%22%3A%2260657%22%2C%22userData%22%3A%7B%7D%7D%7D%7D; nlbi_1990338=z1r+aZmwBEOjLfq/zoaznQAAAADiuC4uAVdoAgxa7fFEQy+0; incap_ses_738_1990338=/3AKDsEN9hfYEzPelOg9Ch1D7GQAAAAA6/jr1z8VuRB2E+hDSoly0w==; ECommBanner=jewelosco; ECommSignInCount=0; AMCVS_A7BF3BC75245ADF20A490D4D%40AdobeOrg=1; AMCV_A7BF3BC75245ADF20A490D4D%40AdobeOrg=179643557%7CMCIDTS%7C19598%7CMCMID%7C62433100481079567243421093039203366277%7CMCAAMLH-1693810077%7C12%7CMCAAMB-1693810077%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1693212477s%7CNONE%7CvVersion%7C5.5.0; SAFEWAY_MODAL_LINK=; s_ivc=true; reese84=3:usefM23TvBFLT+CG+48niQ==:NITBcKzumAoiDw0zLhyPFyGgCD6r44ffaKORTXS2vWJtbvOMG0Zji4Xi962TxtNFLwoDudKMQV7mgaFmu1WGQ88APT3dn1K+3YHp39PAM7polPh75oBtgxIkolt5HFbeKlC33c8XSA2ifCBxDIK6wWZHkjAczmaKyLvzzbHK3b0Pfw49Go0hzCzUKnlPk/fdLtXvHulIuQYh9NfZ4CtIx76/czipDPM2rJfH6yGO0Hz4XB9T+H9tHtIMRQrNJ8C+VJB1LLiTiDzCnGrVxJqnEq/4eJs1KUMxN7uQBo5IpWgJGwz9WO7epKBAkC+lzmWrMqlw2mf42Kxrt7mn17k02vK5w3mVx7D4Np5nDzSs4Mtdo5/e/JVHez8/GzmKvc4/GNOJePiwqgfoEa0lRd3hQ1KHkZh8NIpU7Koy4NqNSpF1l8FCLrwRb+b6MMZWTYP8efa/dIcPrc7nzYzfKWjgktXBX0dxES4bI/ZWyACD3ZDjqxZH/1r3IFqQCfXMpv6wDIxkrxctZfYTFXFkDJfKesdzpYaMy+l0PX81XFpZS1bSARv8Vj6rWPuHJ/TYS+Ut:NkOhxijSpPcPGn0xGEaZgfMC5l1ow0QzdulqJ609EFw=; OptanonConsent=isGpcEnabled=0&datestamp=Mon+Aug+28+2023+12%3A19%3A26+GMT%2B0530+(India+Standard+Time)&version=202306.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=d9b3e4ba-3f32-40f8-8755-b0523d33636d&interactionCount=2&landingPath=NotLandingPage&AwaitingReconsent=false&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1&geolocation=IN%3B; s_sq=%5B%5BB%5D%5D; nlbi_1990338_2147483392=/EmMDdA8mBoV0RL7zoaznQAAAABFCwkb40vtM2E4U10xudXQ'''

# a = coo.split(";")
# c = {}
# for i in a:
#     key, value = i.split("=",1)
#     c[key.strip()] = value.strip()
def cat_links():
    dataset = []
    r = requests.get("https://www.jewelosco.com/shop/aisles.3441.html",headers=headers_dict)
    s = BeautifulSoup(r.text,"html.parser")
    a = s.find_all("a")
    for i in a:
        if "View All" in i.text:
            r1 = requests.get("https://www.jewelosco.com/"+i["href"])
            s1 = BeautifulSoup(r1.text,"html.parser")
            cat = s1.select('.categories-item.aisle-item')
            print(len(cat))
            for q in cat:
                if "/shop/aisles/" in q.select_one(".sbc-link")["href"]:
                    hr = q.select_one(".sbc-link")["href"]
                    id_ = q.select_one(".sbc-link")["id"].replace("dynamic_tile_aisle_","").replace("?","")
                    if "sbc_custom" in id_:
                        id_ = q.select_one(".category-image__default")["data-src"].split("/")[-1].split("$")[0].replace("L3_","").replace("?","").replace("_safeway","")
                    dataset.append([hr,id_])
    print(len(dataset))
    df = pd.DataFrame(dataset,columns=["links","cat_id"])
    df.to_excel("Category_links_new.xlsx")


def product_details():
    dataset = []
    df = pd.read_excel('Category_links_new.xlsx')["cat_id"].to_list()

    header = {
        "Ocp-Apim-Subscription-Key": "e914eec9448c4d5eb672debf5011cf8f"
    }
    ip = {
        "proxy": {
            'http': 'http://geonode_SxA5BnHLFX:6aaed733-56f0-4ffc-9b44-b7cc64c5ca87@rotating-residential.geonode.com:9000',
                    'https': 'http://geonode_SxA5BnHLFX:6aaed733-56f0-4ffc-9b44-b7cc64c5ca87@rotating-residential.geonode.com:9000'
        }
    }
    for cat in df:
        print(cat)
        for pg in range(0, 10000, 30):
            while True:
                try:
                    r = requests.get(
                        f"https://www.jewelosco.com/abs/pub/xapi/v1/aisles/products?request-id=8051693209727041826&url=https://www.jewelosco.com&pageurl=https://www.jewelosco.com&pagename=aisles&rows=30&start={pg}&search-type=category&storeid=3405&featured=true&search-uid=&q=&sort=&userid=&featuredsessionid=&screenwidth=1366,320&dvid=web-4.1aisles&category-id={cat}&pp=none&channel=instore&banner=jewelosco", headers=header,proxies={'http':'http://geonode_SxA5BnHLFX:6aaed733-56f0-4ffc-9b44-b7cc64c5ca87@rotating-residential.geonode.com:9000'})
                    break
                except:
                    print("error")
                    time.sleep(120)
            try:
                j = r.json()['response']['docs']
                if pg > int(r.json()['response']['numFound']):
                    break
            except:
                print(f"wrong cat {cat}")
                j = []
            for pr in j:
                today = datetime.today().date()
                formatted_today = today.strftime('%Y-%m-%d')
                upc = trim_and_pad(pr['upc'])
                matched_items = find_matches_reverse(pr["name"])
                matched = ''
                if matched_items:
                    for match in matched_items:
                        matched = match[1][::-1] + ' ' + match[0][::-1]
                else:
                    matched = ''
                reg = float(pr["basePrice"])
                sal = float(pr['price'])
                if reg == sal:
                    sal = ""
                try:    
                    data = {
                        "zipcode": "60031",
                        "store_name": "Jewel-Osco Grand & Hunt Club Rd",
                        "store_location": "6509 W Grand Avenue, Gurnee, IL 60031",
                        "store_logo": "https://www.jewelosco.com/content/dam/safeway/images/logos/JewelOsco_Vert_Oval_RGB.svg",
                        "category": pr["departmentName"].strip(),
                        "sub_category": pr["aisleName"].split("|")[0].strip(),
                        "product_title": pr["name"].strip(),
                        "weight": matched,
                        "regular_price": reg,
                        "sale_price":  sal,
                        "image_url": f"https://images.albertsons-media.com/is/image/ABS/{pr['pid']}?$ng-ecom-pdp-desktop$&defaultImage=Not_Available",
                        "url": f"https://www.jewelosco.com/shop/product-details.{pr['pid']}.html",
                        "upc": upc,
                        "crawl_date": formatted_today
                    }
                    dataset.append(data)
                except:
                    pass    
                
    print(len(dataset))
    today = datetime.today().date()
    formatted_today = today.strftime('%Y-%m-%d')
    with open(f"jewel_{formatted_today}.json", 'w') as json_file:
        json.dump(dataset, json_file, indent=4)
    upload_file(ctx, local_file_path=f"jewel_{formatted_today}.json", folder_relative_url="/sites/DataTeam420-GroceryData/Shared Documents/GRC - Grocery Data/jewel_uploads")    


def main():
    cat_links()
    product_details()

main()
# # # Set the timezone to Indian Standard Time (IST)
# # india_timezone = timezone('Asia/Kolkata')

# # Create a scheduler with IST timezone
# scheduler = BackgroundScheduler(timezone='asia/kolkata')

# # Schedule the job for Monday at 6 PM IST
# scheduler.add_job(main, 'cron', day_of_week='mon', hour=18, id='monday_main_process')

# # Schedule the job for Wednesday at 6 PM IST
# scheduler.add_job(main, 'cron', day_of_week='wed', hour=18, id='wednesday_main_process')

# # Start the scheduler in the background
# scheduler.start()

# while True:
#     # next_run_time_monday = scheduler.get_job('monday_main_process').next_run_time
#     # next_run_time_wednesday = scheduler.get_job('wednesday_main_process').next_run_time
#     # print("Scheduled time for Monday (IST): ", next_run_time_monday)
#     # print("Scheduled time for Wednesday (IST): ", next_run_time_wednesday)
    
#     # Sleep for 6 hours
#     time.sleep(1)