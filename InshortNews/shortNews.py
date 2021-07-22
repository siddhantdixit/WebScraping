from bs4 import BeautifulSoup
from collections import OrderedDict
import requests

class Inshorts:
    __catSoup = None
    __newsSoup = None

    categories = OrderedDict()
    userCat = None
    news = []

    def __init__(self):
        rqLink = "https://inshorts.com/en/read"
        r = requests.get(rqLink)
        content = r.content
        self.__catSoup = BeautifulSoup(content,"html.parser")
        self.__getCategories()
        

    def __getCategories(self):
        ele = self.__catSoup.find(class_="category-list").find_all("a")
        for i in ele:
            cat = i.li.text
            cat_Link = i["href"]
            self.categories[cat] = cat_Link

    def printCategories(self):
        ct = 1
        for cat in self.categories:
            print(ct,". ",cat,sep="")
            ct+=1

    def getNews(self,topic):
        if topic=='' or topic==None:
            topic = '1'
        self.userCat = topic
        newsLink = "https://inshorts.com"+list(self.categories.values())[int(self.userCat) - 1]
        r = requests.get(newsLink)
        content = r.content
        self.__newsSoup = BeautifulSoup(content,"html.parser")
        html_news = self.__newsSoup.find_all("div",class_="news-card z-depth-1")
        # one_news = {}
        ct=1
        for i in html_news:
            sr_no = ct
            headline = i.find("span",{"itemprop":"headline"}).text

            paragraph = i.find("div",{"itemprop":"articleBody"}).text

            source_name = None
            source_link = None
            a_element = i.find("a",class_="source")
            if a_element!=None:
                source_name = a_element.text
                source_link = a_element["href"]
            

            author = None
            Time = None
            Date = None

            info = i.find(class_="news-card-author-time news-card-author-time-in-title")
            det = info.find_all("span")
            author = det[1].text
            Time  = det[2].text
            Date = det[3].text


            image_url = None
            tag = i.find(class_="news-card-image")["style"]
            image_url = self.__fetchImageUrlFromTag(tag)

            one_news = {
                "no":sr_no,
                "headline":headline,
                "paragraph":paragraph,
                "source_name":source_name,
                "source_link":source_link,
                "author":author,
                "time":Time,
                "date":Date,
                "image_url":image_url
            }

            self.news.append(one_news)
            ct+=1

        return self.news

    def __fetchImageUrlFromTag(self,tagcontent):
        pos1 = tagcontent.find('(')
        pos2 = tagcontent.rfind(')')
        return tagcontent[(pos1+2):(pos2-1)]




def main():
    ''' Printing News (Structurally) '''
    
    ''' Accesing Program '''
    # Printing Cateogories
    Inshorts().printCategories()
    inp_cat = input("Enter Category (Name) or Hit Enter (Default: All News): ")
    newsobj = Inshorts().getNews(inp_cat)
    for n in newsobj:
        print(n["no"])
        print("HEADING:")
        print("~",n["headline"],"~")
        print(n["paragraph"])
        print()
        print("SOURCE:")
        print(n["source_name"])
        print(n["source_link"])
        print()
        print("DETAILS:")
        print(n["author"])
        print(n["time"])
        print(n["date"])
        print()
        print("IMAGE URL:")
        print(n["image_url"])
        print("\n\n\n")

if __name__=="__main__":
    main()