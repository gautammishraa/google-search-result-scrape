#Import all the necessary packages

import requests
import re
import pandas as pd
from bs4 import BeautifulSoup
from googlesearch import search


#Get Search Query from User
keyword = input("Search Query: ")
keyword = keyword.lower()
num = int(input('Number of Results:'))
stop = num


#Assign empty lists to hold the output
Keyword_Count = []
Page_Title = []
URL_List = []
Meta_Description = []

#Perform Google Search for the keyword

for url in search(keyword, tld='com', num = num, stop = stop, pause=3.0):
    URL_List.append(url)

#Create a dummy user-agent for HTTP header request

headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0 '}      


#Scrape all the URL in for loop
for url in URL_List:
    meta_flag = False
    response = requests.get(url, headers=headers)
    lower_response_text = response.text.lower()
    match = re.findall("%s" % keyword, lower_response_text)#Get Keyword Count
    count = (len(match))
    Keyword_Count.append(count)  
    #Page Title and Meta Description
    soup = BeautifulSoup(response.text, 'lxml')
    title_text = soup.title.text #Get Page Title
    Page_Title.append(title_text)
    metas = soup.find_all('meta') #Get Meta Description
    for m in metas:
        if m.get ('name') == 'description':
            desc = m.get('content')
            Meta_Description.append(desc)
            meta_flag = True
            continue
    if not meta_flag:
        desc = "Not Found"
        Meta_Description.append(desc)
        
d = {'Page URL': URL_List, 'Page Title':Page_Title, 'Keyword Count': Keyword_Count, 'Meta Description': Meta_Description}
result = pd.DataFrame(d)
result
