from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
from flask import Flask
from flask import render_template
from flask import request


baseUrl="http://keeranrichardson.com/"

class WebPage:
    def __init__(self, url):
        self.url = url

    def findLinks(self):
        self.statusCode = Url(self.url).getStatus()
        if self.statusCode != 200:
            print("can't find the links for "+ self.url+ " because status code = "+ str(self.statusCode))

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
        for fullUrl in self.getFullUrls():
            print("about to check "+fullUrl)
            print(Url(fullUrl).getStatus(), fullUrl)

    def getFullUrls(self):
        fullUrls = []
        for aUrl in self.urlsFound:
            fullUrl = self.makeFullUrl(self.url, aUrl)
            fullUrls.append(fullUrl)
        return fullUrls
        
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
        
class UrlQueue:
    def __init__(self, urlsFound):
        self.urlsToFollow = []
        self.urlsToFollow.extend(urlsFound)

    def isEmpty(self):
        return (len(self.urlsToFollow) == 0)

    def getNextLink(self):
        return self.urlsToFollow.pop(0)

    def addToQueue(self, listOfUrls):
        self.urlsToFollow.extend(listOfUrls)



class Scanner:
    def __init__(self, url):
        self.baseUrl = url
        self.queueToScan = UrlQueue([])

    def addWebPageLinksToQueue(self, aLink):
        page = WebPage(aLink)    
        page.findLinks()
        self.queueToScan.addToQueue(page.getFullUrls())


    def scan(self):
        if self.queueToScan.isEmpty():
            self.addWebPageLinksToQueue(self.baseUrl)
        
        while not self.queueToScan.isEmpty():
            link = self.queueToScan.getNextLink()
            print("about to check "+link)

            aUrl = Url(link)
            statusCode  = aUrl.getStatus()
            print(statusCode, link)

            if statusCode == 200:
                self.addWebPageLinksToQueue(link)


queueOfUrls = UrlQueue([])

print(Url(baseUrl).getStatus())

#link = WebPage(baseUrl)
#link.findLinks()
#link.getStatusCodes()

#scanner = Scanner(baseUrl) 
#scanner.scan()      

app = Flask(__name__)

@app.route('/')
def listPageLinks():
    baseUrl = request.args.get('url', '')
    if baseUrl == "":
        return "add a url parameter"
    link = WebPage(baseUrl)
    link.findLinks()
    fullUrls = link.getFullUrls() 
   
    return render_template('urlList.html', title="linkchecker", urls = fullUrls)
        
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)

    
'''
todos:

- [x] follow links in site
- configure whether to follow external links or not
- doesnt follow duplicate links
- add a list of followed links
- handle 30x redirections
- [x] treat the url list as a queue
- allow restarting
- check for missing images
- check for errors in metadata links
- better reporting
- passing url in as parameter
'''

