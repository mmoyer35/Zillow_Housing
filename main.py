from selenium import webdriver
import time
from bs4 import BeautifulSoup
import requests

#Update with your email and password
EMAIL_ADDRESS = 'YOUR_EMAIL@gmail.com'
PASSWORD = 'YOURPASSWORD'
#Zillow.com address for the location of your choice, this is in San Francisco
ZILLOW_ADDRESS = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22" \
                 "usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A" \
                 "-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%" \
                 "22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22" \
                 "%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22" \
                 "%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C" \
                 "%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B" \
                 "%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D" \
                 "%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D "
#Make sure chromdriver version and your version of Chrome match
chrome_driver_path = "C:\Development\chromedriver.exe"
price_list = []
address_list = []
website_list = []

# Send a get request to Zillow, at the specified address 
response = requests.get(ZILLOW_ADDRESS,
    headers={"User-Agent": "THIS NEEDS TO BE TAKEN FROM THE ZILLOW PAGE, UNIQUE FOR EACH USER",
             "Accept-Language": "en-US,en;q=0.9"})
all_listings = response.text
soup = BeautifulSoup(all_listings, "html.parser")

# Pulls the result list photo-card class from the soup, which is each individual listing
result_list = soup.find(name="ul", class_='photo-cards photo-cards_wow photo-cards_short')
for listing in result_list:
    try:
        #Find the price and split it to an int, add to price list
        price = listing.find(class_="list-card-price").text
        final_price = price.split(" ")[0][1:6]
        price_list.append(final_price)
        #Find listing address and add it to the address list
        listing_address = listing.find(class_="list-card-addr").text
        address_list.append(listing_address)
        #Find the anchor tag and get href
        url_address = listing.find("a")
        url_text = url_address.get('href')
        # Some listings don't have a full URL, just the /b/, this handles that issue
        if url_text[:3] == '/b/':
            website_list.append(f"https://www.zillow.com{url_address.get('href')}")
        else:
            website_list.append(url_address.get('href'))
    except (TypeError, AttributeError):
        pass

# Debugging purposes only
# print(price_list)
# print(website_list)
# print(address_list)

# Pull a google docs form which and populate the data tabs. If recreating, visit this google doc page and make your own to access listing information. 
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(
    'https://docs.google.com/forms/d/e/1FAIpQLSeYDPYjgGkmHfhC_TewWCzyjjVWGllxN2-8ITxFjvtH3LY9vQ/viewform?usp=sf_link')
time.sleep(2)

for item in address_list:
    #Index                            
    index = address_list.index(item)
    #Input the address information                             
    address_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(address_list[index])
    time.sleep(1)
    #Input the price information  
    price_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input.send_keys(price_list[index])
    time.sleep(1)
    #Input the url for the property listing                                  
    url_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    url_input.send_keys(website_list[index])
    time.sleep(1)
    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')
    submit_button.click()
    time.sleep(2)
    submit_another = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another.click()
    time.sleep(2)

driver.close()
