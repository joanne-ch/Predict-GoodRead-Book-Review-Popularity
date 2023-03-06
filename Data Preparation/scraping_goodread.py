from enum import unique
from os import sep
from typing import List
import requests
from bs4 import BeautifulSoup
import lxml
import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

base_url = "https://www.goodreads.com"
link_search_url = ["https://www.goodreads.com/list/tag/thriller?page=38"] 

data_Links = {                                      #Dictionary to store all the data
    "Links_Each_LIST" : [],
    "Links_Each_BOOK" : [],
}

temp_data = {
    "Book_ID"           : [],
    "Book_Title"        : [],
    "Author_Name"       : [],
    "Average_Ratings"   : [],
    "Num_Ratings"       : [],
    "Num_Review"        : [],    
}

data = {
    "Book_ID"           : [],
    "Book_Title"        : [],
    "Author_Name"       : [],
    "Average_Ratings"   : [],
    "Num_Ratings"       : [],
    "Num_Review"        : [],    
    "Review"            : [],
    "Stars_Ratings"     : [],
    "Likes_Count"       : [],
    "User_ID"           : [],
}

def parse_page(url, attribute_name, attribute_value, hierarchy):
    print(url)  #REMOVE AFTER DEBUG CHECKING
    page = requests.get(url)

    if page.status_code == requests.codes.ok:
        bs = BeautifulSoup(page.text, "lxml")
        list = bs.find_all(attrs={attribute_name : attribute_value})

        #Getting attributes for each hierarchy
        if (hierarchy == "list"):
            for items in list:
                get_list_links(items)
        elif(hierarchy == 'books'):
            for items in list:
                get_book_links(items)

        #Checking if there's a next page for each hierarchy
        if (hierarchy == "list"):
            new_url = check_next_page(bs, "next »")
        elif(hierarchy == 'books'):
            new_url = check_next_page(bs, "Next →")

        if (new_url == 0):
            return
        else:
            parse_page(new_url, attribute_name, attribute_value, hierarchy)

def get_list_links(lists):
    Links_Each_LIST = base_url + lists['href']
    data_Links["Links_Each_LIST"].append(Links_Each_LIST)

def get_book_links(books):
    Book_ID_Title = books.find('a', class_ = "bookTitle")
    Book_ID_Title = Book_ID_Title['href'] if Book_ID_Title else ""
    Links_Each_BOOK = base_url + Book_ID_Title
    data_Links["Links_Each_BOOK"].append(Links_Each_BOOK)

def check_next_page(bs, text):
    next_page_text = bs.find('a', class_ = "next_page")
    next_page_text = next_page_text.text if next_page_text else ""
    
    print(next_page_text)

    if (next_page_text == text):
        next_page_partial = bs.find('a', class_ = "next_page")['href']
        next_page_url = base_url + next_page_partial
        return next_page_url 
    else:
        return 0

def get_EachBook_data(url):
    #Setting Selenium Up
    options = Options()
    options.add_argument("--windows-size=1920,1080")
    #options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    page_source = driver.page_source

    #Feed Page Source to BS4
    bs = BeautifulSoup(page_source, 'lxml')

    #Get BOOK_ID, Book_Title, Author, AVERAGE_RATING, NUM_RATING, Num_Review for each book
    get_page_data(bs, url)

    #Get REVIEW DATA
    get_review_data (bs)
   
    
    while(check_next_page(bs, "next »")):
        
        try:
            next_button = driver.find_element_by_xpath("//a[@class='next_page']")
            next_button.click()
            time.sleep(3)  #Wait for page to load
        except:
            time.sleep(3)
            continue
        bs = BeautifulSoup(driver.page_source, 'lxml')
        get_review_data(bs)
    else:
        return
        
def get_page_data(bs, url):
    Book_ID = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", url[36:])

    Book_Title = bs.find('h1', id = "bookTitle")
    Book_Title = Book_Title.text.strip() if Book_Title else " "

    Author = bs.find_all('span', attrs={"itemprop" : "name"})
    Author_Name = ''
    if (Author):
        for Each_Author in Author:
            Author_Name = Author_Name + ", " + Each_Author.text

    Average_Ratings = bs.find("span", attrs={"itemprop" : "ratingValue"})
    Average_Ratings = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", Average_Ratings.text)[0] if Average_Ratings else ""
    
    Num_Ratings = bs.find('meta', attrs={"itemprop" : "ratingCount"})
    Num_Ratings = Num_Ratings["content"] if Num_Ratings else ""
    
    Num_Review = bs.find('meta', attrs={"itemprop" : "reviewCount"})
    Num_Review = Num_Review["content"] if Num_Review else ""

    temp_data["Book_ID"] = Book_ID[0]
    temp_data["Book_Title"] = Book_Title
    temp_data["Author_Name"] = Author_Name[1:]
    temp_data["Average_Ratings"] = Average_Ratings
    temp_data["Num_Ratings"] = Num_Ratings
    temp_data["Num_Review"] = Num_Review

def get_review_data(bs):
    list_of_reviews = bs.find_all(attrs={"class" : "review"})

    for reviews in list_of_reviews:
        Review = reviews.find('div', class_ = "reviewText stacked")
        Review_Expanded = Review.find(attrs={"style" : "display:none"})     #To deal with ...more button
        if (Review_Expanded):
            Review_Expanded_Spoiler = Review_Expanded.find(attrs={"style" : "display:none"})
            if (Review_Expanded_Spoiler):
                data["Review"].append(Review_Expanded_Spoiler.text)         #To deal with spoiler button
            else:
                data["Review"].append(Review_Expanded.text)
        else:
            Review_Not_Expanded = Review.find(attrs={"class" : "readable"})  #To deal with ones with no ...more button
            Review_Not_Expanded = Review_Not_Expanded.text.strip() if Review_Not_Expanded else " "
            data["Review"].append(Review_Not_Expanded)
        
        Stars_Ratings = reviews.find('span', class_ = 'staticStars notranslate')
        Stars_Ratings = Stars_Ratings.find_all('span', class_ = 'staticStar p10') if Stars_Ratings else ""
        data["Stars_Ratings"].append(len(Stars_Ratings))

        Likes_Count = reviews.find('span', class_ = "likesCount")
        if (Likes_Count):
            Likes_Count = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", Likes_Count.text)
            data["Likes_Count"].append(Likes_Count[0])
        else:
            data["Likes_Count"].append('0')

        User_ID = reviews.find("a", class_ = 'user')
        User_ID = User_ID['href'][11:] if User_ID else ""
        data["User_ID"].append(User_ID)

        data["Book_ID"].append(temp_data["Book_ID"])
        data["Book_Title"].append(temp_data["Book_Title"])
        data["Author_Name"].append(temp_data["Author_Name"])
        data["Average_Ratings"].append(temp_data["Average_Ratings"])
        data["Num_Ratings"].append(temp_data["Num_Ratings"])
        data["Num_Review"].append(temp_data["Num_Review"])

def List_Drop_Duplicates(list_book):
    list_book = list(dict.fromkeys(list_book))

def export_table_and_print(data):
    table = pd.DataFrame.from_dict(data, orient='index')       #Putting our data in a dataframe to make it easier to read
    table = table.transpose()
    print(table.shape)
    table.to_csv("Goodread_dtf.csv", sep=",", encoding = "utf-8", index=False) #Saving the table into a csv file
            

def main():
    parse_page(link_search_url[0], "class", "listTitle", "list") #Get the LINK of each LIST in a specific TAGS. 
    
    for i in range(len(data_Links["Links_Each_LIST"])):
        #Get the LINK of each LIST in a specific TAGS. 
        parse_page(data_Links["Links_Each_LIST"][i], "itemtype", "http://schema.org/Book", "books")

    List_Drop_Duplicates(data_Links["Links_Each_BOOK"])

    for i in range(len(data_Links["Links_Each_BOOK"])):
        get_EachBook_data(data_Links["Links_Each_BOOK"][i])

    #print(data["Review"])
    export_table_and_print(data)


if __name__ == '__main__':
    main()

