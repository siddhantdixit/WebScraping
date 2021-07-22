from bs4 import BeautifulSoup
import requests


class WorldoMeter:
    soup = None
    countries_Url = {}

    # Country
    country = None
    country_Url = None
    country_soup = None

    # Demographics
    life_expectancy = None
    infant_mortality = None
    deaths_under5 = None

    # CountryInfo
    total_population = None
    country_rank = None
    world_share = None
    population_density = None
    total_land_area = None
    median_age = {}


    #MainCities
    main_cities = {}

    def __init__(self, country=''):
        # Soup Initialization
        self.country = country
        r = requests.get(
            "https://www.worldometers.info/world-population/population-by-country/")
        content = r.content
        self.soup = BeautifulSoup(content, "html.parser")

        # Getting Country Names and URLs
        countries_name_data = self.soup.find('tbody').find_all('a')
        countries_name = [ct.text for ct in countries_name_data]

        for ct in countries_name_data:
            self.countries_Url[ct.text] = ct['href']

        # Checking if country parameter is passed or not. If passed then initializing country url and Loading Data
        if country != '':
            # Loading URL
            self.country_Url = "https://www.worldometers.info" + self.countries_Url[country]

            # Generating Country Soup
            self.__createCountrySoup()
            # Loading Demographics
            self.__getDemographics()
            # Loading Country Info
            self.__getCountryInfo()
            # Loading Cities Info
            self.__maincitiesPopulation()


    def printCountries(self):
        # Printing Country Names so that user can enter it correctly!
        counter = 1
        for cnt_names in self.countries_Url:
            print(str(counter)+".",cnt_names)
            counter+=1

    def __createCountrySoup(self):
        r = requests.get(self.country_Url)
        content = r.content
        self.country_soup = BeautifulSoup(content, 'html.parser')

    def __getDemographics(self):
        data = self.country_soup.find_all(class_='panel-body')
        self.life_expectancy = data[0].span.text
        self.infant_mortality = data[1].span.text
        self.deaths_under5 = data[2].span.text

    def __getCountryInfo(self):
        # Getting Country Rank
        self.country_rank = list(self.countries_Url.keys()).index(self.country) + 1

        # Getting Additional Info
        country_data = self.country_soup.find("div", "country-pop-description").find_all("li")
        for i in country_data:
            all_tokens = i.find_all(string=True)
            words = "".join(all_tokens)
            if "current population" in words:
                self.total_population = i.find_all("strong")[1].text.strip(' .').replace(',','')

            # "equivalent" is present in world population share string
            elif "equivalent" in words:
                self.world_share = i.find_all("strong")[0].text.strip(' .')

            elif "population density" in words:
                self.population_density = words[words.find(" is ")+3:].strip(' .')

            elif "land area" in words:
                self.total_land_area = words[words.find(" is ")+3:].strip(' .').replace(',','')

            elif "median age" in words:
                self.median_age = words[words.find(" is ")+3:].strip(" .")

    def __maincitiesPopulation(self):
        city_tb = self.country_soup.find(class_="table table-hover table-condensed table-list").tbody.find_all("tr")
        for i in city_tb:
            city_data = i.find_all("td")
            self.main_cities[city_data[1].string] = city_data[2].string.replace(",","")

    


# Using WorldoMeterClass
def main():
    print("Names of countries")
    WorldoMeter().printCountries()
    print()

    inp_cnt = input("Enter the name of country: ")
    print("-------------------------")
    print(inp_cnt)
    wod = WorldoMeter(inp_cnt)
    print("Current Population : ",wod.total_population)
    print("Country Rank : ",wod.country_rank)
    print("World % Share : ",wod.world_share)
    print("Total Land Area : ",wod.total_land_area)
    print("Population Density : ",wod.population_density)
    print("Median Age : ",wod.median_age)
    print("Life Expectancy : ",wod.life_expectancy)
    print("Infant Mortality : ",wod.infant_mortality)
    print("Deaths Under Age 5 : ",wod.deaths_under5)

    print("------Main City Population-----")
    for city,popu in wod.main_cities.items():
        print(city,popu)

if __name__=="__main__":
    main()