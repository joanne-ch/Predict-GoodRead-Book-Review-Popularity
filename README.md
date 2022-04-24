<img width="1000" alt="image" src="https://user-images.githubusercontent.com/92350663/164890945-72d37df1-769d-4077-bf5b-7e19b773e1ad.png">

# PredictingBookReviewPopularity_SC1015_Project
SC1015-Data Science Project!<br />
Welcome to our Predicting Popularity of Book Reviews Project Repository:
# ABOUT:
Our Project for SC1015-Introduction to Data Science and Artificial Intelligence aims at predicting the Popularity of Book Reviews using the Goodreads book review dataset<br />
The code can viewed in the aformentioned order:
1. Data preparation  
2. EDA
3. Logistic Regression Model
4. Xgboost Model

# CONTRIBUTORS:
1. JOANNE CHRISTINA SALIMIN : Data scrapping/cleaning & Preparation, Gradient Boosting Model
2. VARSHA BALAJI: Data Preparation, Logistic Regression Model 
3. NITHYA HARIHARAN: Exploratory Data Analysis 

# PROBLEM DEFINITON 
<br />
1. Can we predict the popularity of book reviews based on their Textual & Non Textual charactertistics and thus stimulate reading interest among people?<br />
2. How do we select an optimal Machine Learning model to help us do the same?

# MODELS USED
1. XGBOOST-Gradient Boosting
2. Logistic Regression

# RESULTS 
Using our Machine Learning Model, we can:
1. Modify variables and predict what changes can be made to identify if the review is popular or not
2. Predict potential popular book reviews with positive sentiment score and put it in the front page of GoodReads to receive increased interest in reader for that particular book
3. Book reviewers can understand better how to create reviews that would help support their favourite book/author
# OPTIMAL MODEL
Given an unknown dataset, we observed that it was best to use Logistic Regression with an undersampled Non-Textual data as compared to XGBoost for our prediction. <br />
The Logistic Regression model works generally well for predicting both popular and unpopular reviews.

# WHAT WE LEARNT 
1.  Web scraping using the Python library BeauitfulSoup and Selenium 
2.  Using Python library fasstext, and a premade model lid.176.bin in order to filter reviews written in English 
3.  Refining our skills in matplotlib library for detailed Exploratory Data analysis 
4.  sklearn library for Logistic Regression
5.  XGBoost library for Gradient Boosting 
# REFERENCES
1. https://www.analyticsvidhya.com/blog/2021/10/building-an-end-to-end-logistic-regression-model/
2. https://www.mikulskibartosz.name/xgboost-hyperparameter-tuning-in-python-using-grid-search/
3. https://pythonprogramming.net/introduction-scraping-parsing-beautiful-soup-tutorial/
4. https://fasttext.cc/docs/en/supervised-tutorial.html
5. https://www.datacamp.com/community/tutorials/text-analytics-beginners-nltk




<p> Dataset Used: https://drive.google.com/drive/folders/1FEuKncmRF5BChCKe2hoMEnktKBeiBFAr?usp=sharing <\p>
<p> Slides Used: https://docs.google.com/presentation/d/1OR5Q_Z-tb1yqVvIYZrhJd_lFhDjJuTR82FMFf7DqoJ4/edit?usp=sharing <\p>
