from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

baseUrl="http://keeranrichardson.com/"

class WebPage:
    def __init__(self, url):
        self.url = url

    def findLinks(self):
        self.statusCode = Url(self.url).getStatus()
        if self.statusCode != 200:
            print("can't find the links for "+ self.url+ " because status code = "+ self.statusCode)

        self.urlsFound = []
        self.html = requests.get(self.url).text
        self.soup = BeautifulSoup(self.html, "html.parser")

        for link in self.soup.find_all('a'):
            href = link.get('href')
            if href is not None:
                self.urlsFound.append(href)
                print(href)

    def makeFullUrl(self, base, end):
        return urljoin(base, end)

    def getStatusCodes(self):
        for aUrl in self.urlsFound:
            fullUrl = self.makeFullUrl(self.url, aUrl)
            print("about to check "+fullUrl)

            print(Url(fullUrl).getStatus(), fullUrl)
            

   

class Url:
    def __init__(self, url):
        self.url = url
        self.response = None

    def getStatus(self):
        try:
            if self.response is None:
                self.response = requests.head(self.url)
            return self.response.status_code
        except:
            print("error reading "+ self.url)
            return -1
        
print(Url(baseUrl).getStatus())

link = WebPage(baseUrl)
link.findLinks()
link.getStatusCodes()
        


