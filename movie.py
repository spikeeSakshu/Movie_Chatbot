# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 19:50:03 2019

@author: POORVI
"""

import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
import re

movie_url=[]


def imdb(name):
    movie=name
            # str(input('Movie Name: '))
    movie = movie.title()
    movie_search = '+'.join(movie.split())

    base_url = 'http://www.imdb.com/find?ref_=nv_sr_fn&q='
    url = base_url + movie_search + '&s=all'

    try:
        with urllib.request.urlopen(url) as r:
            html_d = r.read()
        soup = BeautifulSoup(html_d, 'html.parser')
        movies = soup.find_all('a', string=movie)
        
        movie_url=('https://www.imdb.com' + str(movies[0].get('href')))
        
        with urllib.request.urlopen(movie_url) as r:
            html_doc = r.read()
            soup1 = BeautifulSoup(html_doc, 'html.parser')
            movie_title = soup1.find('title').contents[0]
            rate = soup1.find('span', itemprop='ratingValue').contents[0]
            print(movie_title)
            
            
            return 'IMDB: ' + rate + '/10.0'
                
    except Exception as e:
        print(e)
        print("There is no movie like this. ",movie)
        
        return "There is no movie like this. "+movie
    


def rot_handle(movie): 
    search_name = '%20'.join(movie.split())
#    print('hi')
    base_url="https://www.rottentomatoes.com/search/?search="
    url=base_url+search_name
    driver=webdriver.PhantomJS()
    driver.get(url)
#    print(url)
    
    title1= driver.find_element_by_id("movieSection")
    movie = title1.find_element_by_class_name('unstyled')
    link=movie.get_attribute("href")
    name=movie.text
    with urllib.request.urlopen(link) as r:
            html_d = r.read()
    soup = BeautifulSoup(html_d, 'html.parser')

#        print(type(movie_title))
    rate = soup.find('span', attrs={'class': 'mop-ratings-wrap__percentage'})
    rate=rate.get_text()
        # rating = " ".join(re.split("\s+", rate, flags=re.UNICODE))
    rating=re.sub(r"\s+"," ",rate)

    rating=rating.split(" ")
    
    driver.quit()
    print(name)
    print("Tomatometer:",rating[1])
    return "Tomatometer:"+ rating[1]

       
def rotten_tomatoes(name):
    
    movie=name
    movie_search = '_'.join(movie.split())  # joined the movie name by splitting through spaces
        # search for how to do case insensitive search for movie names

    base_url = 'https://www.rottentomatoes.com/m/'
    url = base_url + movie_search  # main url which will give movie info
#    print(url)
    try:
        with urllib.request.urlopen(url) as r:
            html_d = r.read()
        soup = BeautifulSoup(html_d, 'html.parser')

        movie_title = soup.find('title').contents[0]
#        print(type(movie_title))
        rate = soup.find('span', attrs={'class': 'mop-ratings-wrap__percentage'})
        rate=rate.get_text()
        # rating = " ".join(re.split("\s+", rate, flags=re.UNICODE))
        rating=re.sub(r"\s+"," ",rate)

        rating=rating.split(" ")
        print(movie_title)
        
#        rating=rating[3].split("/")

        print("Tomatometer:",rating[1])
        return "Tomatometer: "+ rating[1]
        
    except Exception as e:
#        print(e)
        if e.code==404:
            return rot_handle(movie)
            
        print("There is no movie like this",movie)


def call(name):
    print("NAME ",name)
    if 'jhonny' in name or 'Rating' in name or 'rating' in name:
        return 'No'
    
    else:
        imdb_rating = imdb(name)
        rotten = rotten_tomatoes(name)
       
    
    return ''+str(imdb_rating)+"\n"+ str(rotten)
    