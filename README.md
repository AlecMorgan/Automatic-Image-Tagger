# Tagging Pictures on Social Media using Deep Learning

Project from the 4th project week at Flatiron School's data science program. 

**Goal**: predict Instagram hashtags for a given image.

**Presentation**: [link to presentation](https://docs.google.com/presentation/d/1J3S1q_XvEhRQ1oK63WoLEthnBDFeddjv_a6V3gavuTU/edit)

**Team**: [Alec Morgan](https://github.com/AlecMorgan), [Andy Luc](https://github.com/rokaandy), [Anna Zubova](https://github.com/AnnaLara)

**Main working notebook**: https://github.com/AlecMorgan/mod_4_project/blob/master/index.ipynb
Some final steps need to be completed 

**Scraping notebook**: https://github.com/AlecMorgan/mod_4_project/blob/master/scraping.ipynb

**Ready-to-use model**: https://github.com/AlecMorgan/mod_4_project/blob/master/predict_hashtag_for_new_image.ipynb
Some final steps need to be completed


## Overvew

### Data collection

We scraped 3000 Instagram images that had the following hashtags (300 images per hashtag): #travel, #food, #animals, #cars, #babies, #wedding, #architecture, #selfie, #fitness, #nature. We also scraped all hashtags that appeared in the comments.

We initially stored the data in S3 bucket, but we experienced unexpected S3 bugs that prevented us from sharing the data between AWS accounts. As the images had an average size of just 100KB, we opted to store those locally.

### Modeling

We used a **neural network** to extract deep features from the base model MobileNetV2. We then applied **transfer learning** technique and applied the the model to our data, extracting deep features from each individual image. We stored information about deep features in a separate file.

Independently of the graphic data, we applied **ALS model** to the hashtag text data. This model analized relationship between hashtags and extracted model's *user features* (which in out case were image features) and *item features* (in our case - hashtag features). The dot product of each combination represents a kind of recommendation score that allows to select n numbers of the hashtags to recommend. The example of the recommendation made with the ALS model can be found in the presentation. The ALS model is saved in a separate file to be able to use it easily.

### Final step to make

The idea is to combine these 2 models to reach higher accuracy of recommendations.

The algorithm will be the following:

1. Given a new image to make recommendations for, extract its deep features uning the model pretrained with MobileNetV2.
2. Find *n* most similar images using cosine similarity between deep features.
3. For each of the *n* most similar images find the average of the ALS's *image features*.
4. Find the dot products of the above value and each hashtag's *item features* (from ALS)
5. Select n hashtags to recomment that have the highest dot product.

Due to the limited time we had for compliting the project, this step has not been yet completed. We expect to have the final model working in a short period of time.