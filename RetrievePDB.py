import urllib
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
import urllib.parse

import datetime
import re
import sys
import pymysql
import logging
import pymysql.cursors
import requests as rq
from SQLConnection import DBHelper
import linecache
import webbrowser
import numpy as np

# Now, let’s use requests_html to run the JavaScript code in order to render the HTML we’re looking for.
# import HTMLSession from requests_html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import chromedriver_binary  # Adds chromedriver binary to path
from webdriver_manager.chrome import ChromeDriverManager

#from autotest_lib.client.common_lib.cros import chromedriver

try:
    from requests_html import HTMLSession
except ImportError:
    try:
        import requests_html
    except ImportError:
        print ("Te system can't find requests_html. BLAST search results will not" 
            + " be parse without this module.")
try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        import BeautifulSoup
    except ImportError:
        print ("Te system can't find BeautifulSoup. BLAST search results will not" 
            + " be parse without this module.")


def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def store(title, content, url):
    print(title, content, url)
    cur.execute("INSERT INTO pdb.pages (title, content, url) VALUES (\"%s\", \"%s\", \"%s\")", (title,content,url,))
    cur.connection.commit()


def getLinks(articleUrl):
    html = urlopen(articleUrl)
    bsObj = BeautifulSoup(html, 'lxml')
    try :
        title = bsObj.find("h1").get_text()
        print(title)
    except :
        PrintException()
    try :
        content = bsObj.find("div", {"id":"mw-content-text"}).find("p").get_text()
        print(content)
    except :
        PrintException()


# Open database connection
connection = pymysql.connect(host='localhost', port=int(5000) , user='root', password='xxxx', db='mysql', charset='utf8')

# prepare a cursor object using cursor() method
cur = connection.cursor()
# Drop table if it already eist using execute() method.
cur.execute("DROP TABLE IF EXISTS pages;")
print(cur.fetchone())
from string import ascii_lowercase

# CREATE TABLE as per requirement
sql = """CREATE TABLE pages (
    id
    BIGINT(7) not NULL AUTO_INCREMENT,
    title VARCHAR(200),
    content VARCHAR(10000),
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);"""

try:
    cur.execute(sql)
    connection.commit()
    cur.execute("SELECT * FROM pdb.pages")
    print(cur.fetchone())
except:
    # Rollback in case there is any error
    PrintException()
    connection.rollback()


def xpath_soup(element):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        """
        @type parent: bs4.element.Tag
        """
        previous = itertools.islice(parent.children, 0,parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)

def get_pdb_page(link):
    """
    Generate xpath of soup element
    :param element: bs4 text or node
    :return: xpath as string
    """
    browser = webdriver.Chrome(ChromeDriverManager().install())

    try :
        test = urllib.parse.urljoin("http://www.rcsb.org/",link)
        
        link = urlopen(test)
        bsObj = BeautifulSoup(link, 'lxml')
        title = bsObj.find("span", {"id":"structureID"}).get_text()
        content = bsObj.find("div", {"id":"primarycitation"}).find("h4").get_text()
        paper = bsObj.find("li", {"id":"pubmedDOI"}).find_all("a",href=re.compile("^(http://dx.doi.org/)((?!:).)*$"))
        paper = paper[random.randint(0, len(paper)-1)].attrs["href"]
        print(title, content, paper)
        store(title, content, newArticle)
    except :
        PrintException()


def get_links(url) :
    # the links on rcsb are made with js,
    # so the approach needs to be different
    # create an HTML Session object
    session = HTMLSession()
    
    # Use the object above to connect to needed webpage
    resp = session.get(url)
    
    # Run JavaScript code on webpage
    # Running resp.html will give us an object that allows us to print out, 
    # +search through, and perform several functions on the webpage’s HTML
    resp.html.render()

    # To simulate running the JavaScript code, 
    # we use the render method on the resp.html object.
    # Note how we don’t need to set a variable equal to this rendered result
    resp.html.html

    #  So now resp.html.html contains the HTML we need containing the option tags.
    #  From here, we can parse out the expiration dates from these tags using the find method.


    soup = BeautifulSoup(resp.html.html, "lxml")
    with open("output1.html", "w", encoding='utf-8') as file:
        file.write(str(soup))
    links = soup.find("ul", {"id":"SearchResultsDetails-MainContent"}).find_all("a",href=re.compile("^(/structure/)((?!:).)*$"))
    PDBs = []
    PDBs = np.array(PDBs, dtype = np.float32)
    try :
        for x in range(len(links)) :
            newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
            # here you will get each link,
            # which points to a particular crystall structure
            print(newArticle)
            PDBs = np.append(PDBs,newArticle)
            # Here you use the dictionary
    except:
        PrintException()
        pass
    PDBs = np.unique(PDBs)
    for y in range(len(PDBs)):
        print(PDBs[y])
        get_pdb_page(PDBs[y])

def get_Search(word) :
    url = 'http://www.rcsb.org/'
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    browser.implicitly_wait(10) # this lets webdriver wait 10 seconds for the website to load

    search_bar = '//*[@id="autosearch_SearchBar"]'
    search_bar = WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.XPATH ,search_bar))) 
    search_bar.send_keys(word) 

    browser.implicitly_wait(10)
    btn_go = '//*[@id="searchbutton"]'
    btn_go = WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.XPATH ,btn_go)))
    btn_go.click()         

    print(browser.current_url)
    #get_links(browser.current_url)
    while True :
        try :
            browser.implicitly_wait(30)
            btn_next = '//*[@id="toppager"]/div/button[2]'
            btn_next = WebDriverWait(browser,30).until(EC.visibility_of_element_located((By.XPATH , btn_next)))
            btn_next.click()
            print(browser.current_url)
            try :
                get_links(browser.current_url)
            except:
                PrintException()
                pass
        except:
            PrintException()
            pass


# Start the Script

text_query = "adenosine"
#get_Search(text_query)

cur.execute("SELECT * FROM pdb.pages ORDER BY title;")
print(cur.fetchone())
# This query returns data from the contacts table:
cur.execute("SELECT title, COUNT(title) FROM pdb.pages GROUP BY title HAVING COUNT(title) > 1;")
# The following query returns the duplicate emails in the contacts table:
cur.execute("DELETE t1 FROM pdb.pages t1 INNER JOIN pdb.pages t2 WHERE t1.id < t2.id AND t1.title = t2.title;")
# The following query renumber the id columns starting from 1
cur.execute("SET @i=0;")
cur.execute("UPDATE pdb.pages SET id=(@i:=@i+1);")
connection.commit()
print(cur.fetchone())




