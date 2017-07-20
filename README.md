# Twitter Data Analytics
This Project is a Python(2.7) implementation of the Chapters in the book [Twitter Data Analytics](http://tweettracker.fulton.asu.edu/tda/). This implementation covers:
1. Twitter REST API usage.
2. Twitter Streaming API usage.
3. Network Analysis on Tweets.
4. Sentiment Analysis on Tweets.
5. LDA on Tweets
6. Geo Spatial Visualizations.
7. Network Visualizations.
8. Text Visualizations.
9. Trend Visualizations.

**About Book**
Social media has become a major platform for information sharing. Due to its openness in sharing data, Twitter is a prime example of social media in which researchers can verify their hypotheses, and practitioners can mine interesting patterns and build realworld applications. This book takes a reader through the process of harnessing Twitter data to find answers to intriguing questions. We begin with an introduction to the process of collecting data through Twitter's APIs and proceed to discuss strategies for curating large datasets. We then guide the reader through the process of visualizing Twitter data with realworld examples, present challenges and complexities of building visual analytic tools, and provide strategies to address these issues. We show by example how some powerful measures can be computed using various Twitter data sources. This book is designed to provide researchers, practitioners, project managers, and graduate students new to the field with an entry point to jump start their endeavors. It also serves as a convenient reference for readers seasoned in Twitter data analysis.

## Installation
This software depends on few python packages for scientific computing. You must have them installed prior to running the project. 
The simple way to install these packages is running pip in requirements.txt file in the project:
```
pip install -r /path/to/requirements.txt
```
Note: Run with sudo or admin priviledges if the command fails.
Note: If facing problem while install gensim in windows. Try installing using wheel file. [Link to whl](http://www.lfd.uci.edu/~gohlke/pythonlibs/#gensim)

## Book Chapter Mapping
The files mentioned in this Tree Mapping directory structure are the runnable python files of the project. The Chapter Mapping refers to the chapter where the book is explaining the concept being implemented in the python file.
```
.
├── Chapter2                                                Chapter Mapping
│   ├── Location
│   │   └── LocationTranslationExample.py ──────────────    2.6
│   ├── openauthentication
│   │   ├── OAuthExample.py ────────────────────────────    2.2
│   ├── restapi
│   │   ├── RESTApiExample.py ──────────────────────────    2.2, 2.3, 2.4
│   │   ├── RESTSearchExample.py ───────────────────────    2.5.1
│   └── streamingapi
│       └── StreamingApiExample.py ─────────────────────    2.5.2
├── Chapter4
│   ├── centrality
│   │   ├── BetweennessCentrality.py ───────────────────    4.1.3
│   │   ├── EigenvectorCentrality.py ───────────────────    4.1.3
│   │   ├── InDegreeCentrality.py ──────────────────────    4.1.3
│   │   ├── PagerankCentrality.py ──────────────────────    4.1.3
│   │   ├── SimpleGraph.py ─────────────────────────────    4.5
│   ├── classificationbayes
│   │   ├── NaiveBayesSentimentClassifier.py ───────────    4.2.2
│   │   └── NBCTest.py ─────────────────────────────────    4.2.2
│   └── tweetlda
│       └── LDA.py ─────────────────────────────────────    4.2.1
└── Chapter5
    ├── geospatial
    │   └── KDEHeatmap.py ──────────────────────────────    5.3
    ├── network
    │   ├── CreateD3Network.py ─────────────────────────    5.1
    │   └── ExtractUserTagNetwork.py ───────────────────    5.1
    ├── text
    │   ├── EventSummaryExtractor.py ───────────────────    5.4.2
    │   └── ExtractTopKeywords.py ──────────────────────    5.4.1
    └── trends
        ├── ControlChartExample.py ─────────────────────    5.2.2
        ├── ExtractDatasetTrend.py ─────────────────────    5.2.1
        ├── SparkLineExample.py ────────────────────────    5.2.2
        └── TrendComparisonExample.py ──────────────────    5.2.2
```
## Getting Started
### Setup

The first thing needs to be done is creating a Twitter API consumer key. This can be done by creating an application: https://apps.twitter.com/
Creating an application will give you **consumer_secret** and a **consumer_key** which you need to copy paste in **config.json** file of the project. The config file should look like this
```
{
    "consumer_key": "Your_Consumer_Key", 
    "consumer_secret": "Your_Consumer_Secret", 
    "user_access_secret": "??", 
    "user_access_token": "??"
}
```
Now you need to run the **OAuthExample.py** file which is under Chapter2/openauthentication/ directory. Running this file will help you generate your **user_access_secret** and **user_access_token**.You can run the file using:
```
python OAuthExample.py
```
When you are done with steps asked by OAuthExample.py you can see the config.json file and verify that the config.json will now have the user secret and token instead of ??.
```
{
    "consumer_key": "your_consumer_key", 
    "consumer_secret": "your_consumer_secret", 
    "user_access_secret": "your_user_access_secret",
    "user_access_token": "your_user_access_token"
}
```
### Running Examples
To run the python files use the following command:
```
$ python /path/to/file_name.py
```
For Example for running RESTApiExample.py file go inside the Chapter2/restspi/ directory and run:
```
$ python RESTApiExample.py
```
You can also get detailed help about what each file do and also if they need any parameters using -h argument. For Example:
```
$ python RESTApiExample.py -h

usage: RESTApiExample.py [-h] [-i [I]] [-o [O]] [-a [A]]
File to use Twitter REST API and get User Profile Info or Friend Info or Follower Info or Statuses Info.
optional arguments:
  -h, --help  show this help message and exit
  -i [I]      Name of the input file, which has user names separated by new line.
  -o [O]      Name of the output file for saving result
  -a [A]      API Code. 0 for PROFILE_INFO , 1 for FOLLOWER_INFO , 2 for FRIEND_INFO , 3 for STATUSES_INFO

TweetTracker. Copyright (c) Arizona Board of Regents on behalf of Arizona State University
@author Shobhit Sharma
```
## Support
Send a mail to Shobhit Sharma ( sshar107@asu.edu ) to report any issue or if facing problem while running the project.
## Authors
**Python Code Author**: [Shobhit Sharma](https://www.linkedin.com/in/shosharma)
**Book Authors**: [Shamanth Kumar](http://www.public.asu.edu/~skumar34/), [Fred Morstatter](http://www.public.asu.edu/~fmorstat/), and [Huan Liu](http://www.public.asu.edu/~huanliu/)
Data Mining and Machine Learning Lab
School of Computing, Informatics, and Decision Systems Engineering
Arizona State University
## Citing Book
### MLA
```
Kumar, Shamanth, Morstatter, Fred, and Huan Liu. Twitter Data Analytics. Springer, 2013.
```
### BibTeX
```
  @book{TwitterDataAnalytics2013,
    author = {Kumar, Shamanth and Morstatter, Fred and Liu, Huan},
    title = {Twitter Data Analytics},
    publisher = {Springer},
    address = {New York, NY, USA},
    year = {2013}
  }
```