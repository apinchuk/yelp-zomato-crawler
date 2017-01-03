from urllib import urlopen
from bs4 import BeautifulSoup
import itertools
import re
import HTMLParser
import unicodedata
import ssl
import io
import os

candidate_links=[]
crawl_count=0

def crawl(link) :
    global candidate_links
    global crawl_count
    if("contact" in link or "career" in link or "review" in link or "user" in link or "mobile" in link or "cashless" in link) :
        print "Skipping "+link
        return

    print "Crawling "+link+"\n"
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    seedpage_html=urlopen(link,context=gcontext).read()
    crawl_count+=1;
    
    soupify=BeautifulSoup(seedpage_html)

    for linkURL in soupify.find_all('a'):
        try:
            if(linkURL.get('href').startswith("http")):
                linkStr = linkURL.get('href')
                if("contact" in linkStr or "career" in linkStr or "review" in linkStr or "user" in linkStr or "mobile" in linkStr or "cashless" in linkStr) :
                    print "Skipping appending of "+linkStr
                elif(linkURL.get('href') not in candidate_links) :
                    print "Appending "+linkURL.get('href')
                    candidate_links.append(linkURL.get('href'))
                else :
                    print linkURL.get('href') + " already in the list"
            elif(linkURL.get('href').startswith("/")):
                print "Pagination test : "+linkURL+linkURL.get('href')
        except:
            pass
    phone_number = []
    phone_number = soupify.find("div",{"aria-label" : "Phone number"})
    review_string = []
    review_string = soupify.find("div",{"class" : "resmap pos-relative mt5 mb5"})
    if not phone_number or not review_string:
        try:
            mydivs = soupify.find("div", { "class" : "col-l-3 mtop0 alpha tmargin pagination-number" })["aria-label"]
            print "Got pagination here\n"
            print mydivs
        except :
            print ""
    else :
        restaurant_city= str(link).rsplit('/',1)[1]
        city = str(restaurant_city).rsplit('-',1)[1]
        restaurant = str(restaurant_city).rsplit('-',1)[0]
        filename = ''+city+'/'+restaurant+'/'+restaurant
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        f = io.open(filename, 'wb')
        print "Restaurant : "+restaurant+" City : "+city
        f.write(seedpage_html)

    candidate_links=list(set(candidate_links))
    return

try:
    global candidate_links
    global crawl_count
    #get the page here
    ld2=[]
    seedlink="https://www.zomato.com/madison-wi"
    crawl(seedlink)
    indexCount=0;
    while len(candidate_links)!=0 :
        print len(candidate_links)
        print "Index "+str(indexCount)
        #print candidate_links
        seedLink = candidate_links[indexCount]
        indexCount+=1
        print "Popped seedLink : "+seedLink+"\n"
        if(crawl_count>=10000) :
            print "Crawled 30 links. Stopping here before I get banned!"
            break;
        else :
            crawl(seedLink)

except Exception,e: 
    print str(e)
    print candidate_links
