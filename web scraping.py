import pandas as pd
import requests
from bs4 import BeautifulSoup
import time 
import random
from datetime import date, datetime


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc


zillow= "https://www.zillow.com/albany-ny/rentals/"

headers = {
    'authority': 'www.zillow.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    # 'cookie': 'zguid=24|%24f6aada11-79eb-45c7-9cfa-8e0a4794020d; zjs_anonymous_id=%22f6aada11-79eb-45c7-9cfa-8e0a4794020d%22; zjs_user_id=null; zg_anonymous_id=%2281be5998-db50-41c4-b35d-cb719128e552%22; _ga=GA1.2.232218203.1698712699; _gcl_au=1.1.818970189.1698712703; __pdst=4924d4960ca04dd495a136b82aa064ea; _pin_unauth=dWlkPU56STBZekUwTmpBdFl6UTROQzAwT0dFMExXSm1NVGN0TW1VMFpUQm1PVE5tTnpVeQ; _pxvid=87277140-7786-11ee-9edb-b39882ae8023; JSESSIONID=FE6B8A0A1D22AFA257E8ED44F316E63E; zgsession=1|7a1277ae-50dc-4f24-b54c-2f6501a7be4f; pxcts=81f0453a-791f-11ee-aa56-df30d33f401a; _gid=GA1.2.948038133.1698888676; DoubleClickSession=true; _clck=1e8ghil|2|fgd|0|1399; _derived_epik=dj0yJnU9Sl9iNVNkbDNlRHhzSnU2WG1xWmtMY295VWJNLW1vV1cmbj1hSXRmVlhLNmVtZDljSXdjN2plSzBnJm09MSZ0PUFBQUFBR1ZDLS1RJnJtPTEmcnQ9QUFBQUFHVkMtLVEmc3A9NQ; g_state={"i_p":1698975081257,"i_l":2}; _uetsid=86397ca0791f11eebdb42100ba2d4bdd; _uetvid=d38310909c2f11edacc9a3f54322a165; AWSALB=GiAYOJMfxKVUvQxNr2EaJqZpiFvjlOR1ih3y2/a/K281DIRxc55G5SBWBa+P0FIElYMc7tkBYrHdO9Wjl7o7rpX0G/oaobNYuF1Qg/m/8+FoogXGeZGzqqFsnQnl; AWSALBCORS=GiAYOJMfxKVUvQxNr2EaJqZpiFvjlOR1ih3y2/a/K281DIRxc55G5SBWBa+P0FIElYMc7tkBYrHdO9Wjl7o7rpX0G/oaobNYuF1Qg/m/8+FoogXGeZGzqqFsnQnl; _px3=5b1a0225e959064ae80388b82a860a1d818e1830c9ca7f558f2214df6c222d4f:kb/Bb+tlZ3dZLrWULK0GNcickWWwUqFDsVkCzIKhcFL1ND31C/C1dayqmPArZOLAO7Pbe6HDH160GoRvPWmfkw==:1000:2OUO+634/civsQJjRlsZ5idA7+kKrEO3XJzO7EXxTTU82nM6ZqqHD8FzPVT9WpLNAUGwrup0yysMg1ws5wKEOeNfSvekx3G6qEdawAyxqELz50XsbBI69Eo+WQIxyzsuRXly+hT23GYD6LwpRCNuwvjHY5zDZMbVH93sq9Vk7kVL2tBzf//qyPCFotB6xqVeNom+CyzNIppiwOikxWdZMqgHVa5UVWR80MeQqKUGdiA=; _gat=1; search=6|1701482069489%7Crect%3D42.675817593954456%2C-73.719328633213%2C42.62316758615123%2C-73.81975053873057%26crid%3D5937665405X1-CR1n5j0wqkpuw1x_1745vt%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26z%3D1%26listPriceActive%3D1%26baths%3D1.0-%26beds%3D3-3%26fs%3D0%26fr%3D1%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26featuredMultiFamilyBuilding%3D0%26excludeNullAvailabilityDates%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%09%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; _clsk=12um4f2|1698890073522|25|0|o.clarity.ms/collect',
    'origin': 'https://www.zillow.com',
    'referer': 'https://www.zillow.com/homes/for_rent/?searchQueryState=%7B%22isMapVisible%22%3Atrue%2C%22mapBounds%22%3A%7B%22west%22%3A-73.79593252267833%2C%22east%22%3A-73.74314664926524%2C%22south%22%3A42.62316758615125%2C%22north%22%3A42.675817593954456%7D%2C%22mapZoom%22%3A14%2C%22customRegionId%22%3A%225937665405X1-CR1n5j0wqkpuw1x_1745vt%22%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22beds%22%3A%7B%22min%22%3A3%2C%22max%22%3A3%7D%2C%22baths%22%3A%7B%22min%22%3A1%2C%22max%22%3Anull%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%7D',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'

options = uc.ChromeOptions()
options.add_argument("--headless")
options.add_argument(f"user-agent={my_user_agent}")


driver = webdriver.Chrome(options = options)


driver.get(zillow)




html = driver.find_element(By.TAG_NAME, 'html')
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
#driver.implicitly_wait(2)
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
html.send_keys(Keys.END)
time.sleep(20)
html = driver.page_source


# encod = response.encoding
# contents = response.content.decode(encod)

soup = BeautifulSoup(html, "html.parser")
table1 = pd.DataFrame()

data = soup.find_all('div', {'class' : "StyledPropertyCardDataWrapper-c11n-8-84-3__sc-1omp4c3-0 bKpguY property-card-data"})
address = soup.find_all("address", {"data-test":"property-card-addr"})
price = soup.find_all("span", {"data-test":"property-card-price" })

table1['price'] = price
table1['data'] = data


driver.close()
print(table1)
