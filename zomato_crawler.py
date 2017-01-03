from urllib import urlopen
from bs4 import BeautifulSoup
import itertools
import re
import HTMLParser
import unicodedata
import ssl

try:
    #get the page here
    ld2=[]
    seedlink="https://www.zomato.com/madison-wi/restaurants"
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    seedpage_html=urlopen(seedlink,context=gcontext).read()
    
    #Need to Collect a few seed pages
    soupify=BeautifulSoup(seedpage_html)

    #empty list to hold candidate pages
    candidate_links=[]
    candidate_links_dict={}
    #a double dict to hold data of the form { {link1:{word1:TF word2:TF}} {link2:{word1:TF}} }
    dd={}
    print "Opening SeedURL and extracting links from it"
    #extracting all the links from a page
    for link in soupify.find_all('a'):
        try:
            if(link.get('href').startswith("http")):
                candidate_links.append(link.get('href'))
        except:
            pass

    candidate_links=list(set(candidate_links))

    for crawl_candidate in candidate_links:   
        if "https://www.zomato.com/madison-wi/restaurants" in crawl_candidate :
            print "\nFetched " + crawl_candidate


except Exception,e: 
    print str(e)
    print "\nCannot Open SeedURL\n"
