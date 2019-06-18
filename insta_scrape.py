# code taken from jnawjux with permission from owner:
# https://github.com/jnawjux/web_scraping_corgis/blob/master/insta_scrape.py

import time
import re
from selenium.webdriver import Chrome, Firefox
from random import random
from urllib.request import urlretrieve
from uuid import uuid4

def get_posts(hashtag, n, browser):
    """With the input of an account page, scrape the n most recent posts urls"""
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    browser.get(url)
    post = 'https://www.instagram.com/p/'
    post_links = []
    images = []
    while len(post_links) < n or len(images) < n :
        
        img_src = [img.get_attribute('src') for img in browser.find_elements_by_css_selector('article img')]
        links = [a.get_attribute('href') for a in browser.find_elements_by_tag_name('a')]
        
        for link in links:
            if post in link and link not in post_links and len(post_links) < n:
                post_links.append(link)
                
        for image in img_src:
            if image not in images and len(images) < n:
                images.append(image)
                
        scroll_down = "window.scrollTo(0, document.body.scrollHeight);"
        browser.execute_script(scroll_down)
        time.sleep(3 + (random() * 5))
    
    print(len(images), len(post_links))
    return [{'post_link': post_links[i], 'image': images[i], 'search_hashtag': hashtag} for i in range(len(post_links))]
    
def insta_details(urls):
    """Take a post url and return post details"""
    browser = Chrome()
    post_details = []
    for link in urls:
        browser.get(link)
        try:
        # This captures the standard like count. 
            likes = browser.find_element_by_partial_link_text(' likes').text
        except:
        # This captures the like count for videos which is stored
            view_id = '//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span'
            likes = browser.find_element_by_xpath(view_id).text
        age = browser.find_element_by_css_selector('a time').text
        xpath_c = '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/ul/li[1]/div/div/div'
        comment = browser.find_element_by_xpath(xpath_c).text
        post_details.append({'link': link, 'likes/views': likes, 'age': age, 'comment': comment})
        time.sleep(3 + (random() * 5))
    return post_details  

def find_hashtags(comment):
    """Find hastags used in comment and return them"""
    hashtags = re.findall('#[A-Za-z]+', comment)
    return hashtags
 

def get_hashtags(url, browser):

    browser.get(url)
    comments_html = browser.find_elements_by_css_selector('span')
    all_hashtags = []
    
    for comment in comments_html:
        hashtags = re.findall('#[A-Za-z]+', comment.text)
        if len(hashtags) > 0:
            all_hashtags.extend(hashtags)
    return list(set(all_hashtags))

def get_image(url):
    #browser.get(url)
    uuid = uuid4()
    urlretrieve(url, f'data/{uuid}.jpg')
    name = f'{uuid}.jpg'
    return name
        
    
def get_full_info(hashtag, n):
    browser = Chrome()
    
    posts = get_posts(hashtag, n, browser)
     
    for post in posts:
        post['hashtags'] = get_hashtags(post['post_link'], browser)
        time.sleep(3 + (random() * 5))
        post['image_local_name'] = get_image(post['image'])
        time.sleep(3 + (random() * 5))
    return posts
 
