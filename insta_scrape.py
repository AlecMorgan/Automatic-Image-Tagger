# Base code taken from jnawjux with permission from owner:
# https://github.com/jnawjux/web_scraping_corgis/blob/master/insta_scrape.py

import time
import re
from selenium.webdriver import Chrome
from random import random
from urllib.request import urlretrieve
from uuid import uuid4
import boto3

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
    
    return [{'post_link': post_links[i], 'image': images[i], 'search_hashtag': hashtag} for i in range(len(post_links))]
 

def get_hashtags(url, browser):
    """Return a list of hashtags found in all post's comments"""
    browser.get(url)
    comments_html = browser.find_elements_by_css_selector('span')
    all_hashtags = []
    
    for comment in comments_html:
        hashtags = re.findall('#[A-Za-z]+', comment.text)
        if len(hashtags) > 0:
            all_hashtags.extend(hashtags)
    return list(set(all_hashtags))

def get_image(url, hashtag):
    """Download image from given url and return it's name"""
    uuid = uuid4()
    urlretrieve(url, f'data/{hashtag}/{uuid}.jpg')
    name = f'{uuid}.jpg'
    return name
        
    
def get_full_info(hashtag, n):
    """Return a dictionary with full n posts info for a given hashtag"""
    browser = Chrome()
    
    posts = get_posts(hashtag, n, browser)
    
    try:
        for post in posts:
            post['hashtags'] = get_hashtags(post['post_link'], browser)
            time.sleep(3 + (random() * 5))
            post['image_local_name'] = get_image(post['image'], hashtag)
            time.sleep(3 + (random() * 5))
        return posts
    except:
        return posts
    
def upload_files_to_s3(dir_path, hashtag, bucket_name): ##ex dir_path: 'data/cars/' ; hashtag: 'travel'
    '''Upload files from specific folder to S3 'instagram-images-mod4' bucket to a folder with hashtag name'''
    s3 = boto3.resource('s3')
    
    # make a list of images filenames stored in local directory
    f = []
    for (dirpath, dirnames, filenames) in walk(dir_path):
        f.extend(filenames)
        break
    
    for name in f:
        source = dir_path + name
        bucket = bucket_name
        destination = hashtag + '/' + name
        s3.meta.client.upload_file(source, bucket, destination)
 