# install beautifulsoup4 
# pip install beautifulsoup4
from bs4 import BeautifulSoup 
import requests
import contextlib

# Get: communicate with the server and say "Hey I want this page please"
req = requests.get("https://www.corriere.it")
# check the status code
print(req.status_code) 
# show headers and cookies
# exactly as on a website 200: OK, 404: NOT FOUND, 503: SERVER PROBLEMS, 400: DENIED
# now we have raw data, let's parse them in BS
soup = BeautifulSoup(req.text, "html.parser")
# simple things 
# BS on the fly
print(soup.title)
print(soup.p)
print(soup.h4)
# getting more info
# we want to scrape all the news' titles
# we can see that all the titles are in h4s so 
# CURIOSITY: now findAll or find_all? 
# BeautifulSoup version 4, the methods are exactly the same; 
# the mixed-case versions (findAll, findAllNext, nextSibling, etc.) 
# have all been renamed to conform to the Python style guide,
h4s = soup.find_all("h4")
# we can then easily grab all the titles
for h4 in h4s:
    print(h4.attr) # attribute
    print(h4.content) # this is the content as a list
    print(h4.get_text()) # this is the real text, namely the headline
    # we want to grap the href link how can we do?
    all_vals = h4.find_all("a", href=True)
    for all_val in all_vals: # <-- type b4.element.Tag
        # here we can retrieve the link and the text 
        href_link = all_val['href']
        href_text = all_val.get_text()

# SINGLE ARTICLE SCRAPING
# now let's try to work out with a single article 
# https://corrieredibologna.corriere.it/bologna/cronaca/22_aprile_06/strage-bologna-sentenza-ergastolo-paolo-bellini-48030864-b59a-11ec-a5bb-947bbaae054b.shtml 
req2 = requests.get("https://corrieredibologna.corriere.it/bologna/cronaca/22_aprile_06/strage-bologna-sentenza-ergastolo-paolo-bellini-48030864-b59a-11ec-a5bb-947bbaae054b.shtml")
print(req2.status_code)
soup2 = BeautifulSoup(req2.text, "html.parser")
# with prettify we can see how an article is coded
# the main container is <div class="chapter clearfix"> 
# then we have the paragraphs <p class="chapter-paragraph" style="">
# <h5 class="chapter-title"> denotes the paragraphs' titles
# so we can scrape all the <p class="chapter-paragraph" style=""> to get the text 
article_text = ""
for p_val in soup2.find_all("p", attrs={"class":"chapter-paragraph"}):
    article_text+= p_val.get_text()
    # we could even get images 
    imgs = p_val.find_all("img")
    for img in imgs:
        alt_info = img['alt'] # or title
        image_name = f"{alt_info[0:3]}.png" # take the first 3 letters of the image
        # url
        url_info = f"https://corrieredibologna.corriere.it/{img['content']}"
        # we can save this to a file 
        # optionally read the content from requests.get(url_info, stream=True)
        # so the image is not loaded in memory
        with contextlib.closing(requests.get(url_info)) as image:
            with open(image_name,"wb") as dest_file:
                for block in image.iter_content(1024):
                    if block:
                        dest_file.write(block)
        #
        dest_file.close()     
#
print(article_text)
# outcome: scraping news
# important --> NLP text entity --> graph knowledge --> ground truth dataset