# Instagram hashtags recommender

We created a model that recommends hashtags for Instagram images within 10 categories: travel, food, animals, cars, babies, wedding, architecture, selfie, fitness, nature.

Our recommendation algorithm is based on ALS model combined with graphic data extracted using transfer learning and base pretrained model MobileNetV2.

**Goal**: recommend 10 Instagram hashtags for a given image.

**Presentation**: [link to presentation](https://docs.google.com/presentation/d/1J3S1q_XvEhRQ1oK63WoLEthnBDFeddjv_a6V3gavuTU/edit)

**Team**: [Alec Morgan](https://github.com/AlecMorgan), [Andy Luc](https://github.com/rokaandy), [Anna Zubova](https://github.com/AnnaLara)

**Main working notebook**: index.ipynb

**Scraping notebook**: scraping.ipynb

**Ready-to-use model**: predict\*hashtag\*for\*new_image.ipynb
Note that pickle files used in this notebook are not uploaded to GitHub due to the size. Please, request them if necessary.
The model will be deployed as a Flask app shortly.

## Overvew

### Data collection

We scraped 3000 Instagram images that had the following hashtags (300 images per hashtag): #travel, #food, #animals, #cars, #babies, #wedding, #architecture, #selfie, #fitness, #nature. We also scraped all hashtags that appeared in the comments.

We initially stored the data in S3 bucket, but we experienced unexpected S3 bugs that prevented us from sharing the data between AWS accounts. As the images had an average size of just 100KB, we opted to store those locally.

### Modeling

We used a **neural network** to extract deep features from the base model MobileNetV2. We then applied **transfer learning** technique and applied the the model to our data, extracting deep features from each individual image. We stored information about deep features in a separate file.

Independently of the graphic data, we applied **ALS model** to the hashtag text data. This model analized relationship between hashtags and extracted model's _user features_ (which in out case were image features) and _item features_ (in our case - hashtag features). The dot product of each combination represents a kind of recommendation score that allows to select n numbers of the hashtags to recommend. The example of the recommendation made with the ALS model can be found in the presentation. The ALS model is saved in a separate file to be able to use it easily.

### Recommendation algorithm

Our recommendation algorithm combines two 2 models mentioned above to reach higher accuracy of recommendations.

The algorithm::

1. Given a new image to make recommendations for, extract its deep features uning the model pretrained with MobileNetV2.
2. Find _n_ most similar images using cosine similarity between deep features.
3. For each of the _n_ most similar images find the average of the ALS's _image features_.
4. Find the dot products of the above value and each hashtag's _item features_ (from ALS)
5. Select n hashtags to recomment that have the highest dot product.

### Recommendation example

Test image:
![test image](https://github.com/AnnaLara/mod_4_project/raw/master/test_wedding.jpg)

Hashtags recommended by the model:

1. #love
2. #selfie
3. #fashion
4. #instagood
5. #picoftheday
6. #photography
7. #summer
8. #happy
9. #instagram
10. #beautiful

### Further steps

1. The code needs some cleaning and organizing, which will be done in the nearest future
2. The model will be deployed as a Flask app
