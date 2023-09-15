from io import StringIO
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup as bs
from property_scrapper.utils.mongo_db_Integration import MongoUtil
from django.conf import settings

class Command(BaseCommand):
    def __init__(self):
        self.cities_list = ['delhi', 'pune', 'mumbai', 'lucknow', 'agra', 'ahmedabad', 'kolkata', 'jaipur', 'chennai', 'bengaluru']

    def handle(self, *args, **options):
        scrapper = Scrapper()
        scrapper.run_scrapper(self.cities_list)
    

class Scrapper:
    def __init__(self) -> None:
        pass

    def get_page_url(self, city_name):
        page_url = f"https://www.99acres.com/search/property/buy/{city_name}?keyword={city_name}&preference=S&area_unit=1&budget_min=0&res_com=R&isPreLeased=N"
        return page_url
    
    def run_scrapper(self, list_of_cities):
        headers = self.get_headers()
        mongo_utils = MongoUtil(settings.MONGO_URI)
        cursor = mongo_utils.get_cursor_for_properties_collection()

        for name in list_of_cities:
            page_url = self.get_page_url(name)
            response = requests.get(page_url, headers=headers)

            if response.status_code == 200:
                print(f"Starting scrapping data for page: {name}")
                web_page = bs(response.content, "html.parser")
                property_divs = web_page.find_all("div", attrs={"class":"pageComponent projectTuple__coWorkingTuple projectTuple__noUspWithLandmark projectTuple__cardWrapPremium srp"})
                
                properties_list = list()
                try:
                    for property_div in property_divs:
                        property_tag = property_div.find("a", attrs={"class": "projectTuple__projectName projectTuple__pdWrap20 ellipsis"})

                        property_name = property_tag.text
                        property_link = property_tag.get("href")

                        locality = property_div.find("h2", attrs={"class": "projectTuple__subHeadingWrap body_med ellipsis"}).text
                        locality = locality[locality.index('in') + 2:].strip()

                        label = property_div.find_all("span", attrs={"class": "list_header_semiBold configurationCards__configBandLabel"})
                        price = property_div.find_all("span", attrs={"class": "list_header_semiBold configurationCards__cardPriceHeading"})
                        area = property_div.find_all("span", attrs={"class": "caption_subdued_medium configurationCards__cardAreaSubHeadingTwo ellipsis"})
                        available_properties_list = list()

                        for i in range(len(label)):
                            dic = {}
                            dic.update({"property_type": self.remove_comment_character(label[i].text)})
                            dic.update({"property_cost": self.remove_comment_character(price[i].text)})
                            dic.update({"property_area": self.remove_comment_character(area[i].text)})
                            available_properties_list.append(dic)

                        property = dict()
                        property.update({"name": property_name})
                        property.update({"link": property_link})
                        property.update({"locality": locality})
                        property.update({"available_properties": available_properties_list})
                        property.update({"city": name})

                        properties_list.append(property)
                except Exception as e:
                    print(f"An error occurred: {str(e)}")

                if(properties_list):                
                    try:
                        query_response = cursor.insert_many(properties_list)
                        print(f"Inserted {len(query_response.inserted_ids)} docs for city : {name}")
                    except Exception as e:
                        print(f"Exception occurred in inserting docs for {name} : {e}")

            else:
                print(f"Got status_code for {response.status_code} for city : {name}")


    def remove_comment_character(self, string):
        string = string.replace("<!--","")
        string = string.replace("-->","")
        string = string.replace("(","")
        string = string.replace(")","")

        return string


    def get_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding":"gzip, deflate, br"
        }
