# twitter_task


# To build the container
```
docker build -t tweet_reader:latest .
```

# To run the container (for example with twitter user foxnews)
```
docker run -it -p 5000:5000 tweet_reader -u "foxnews"
```

# To access the api for collected tweets
```
curl http://127.0.0.1:5000/tweets
```

# ASSUMPTIONS
1. The bulk of the task was to find a way to circumvent the authentication requirements from the official API's since a core requirement was "Make sure to use scraping or APIs that do not require user authentication or a twitter developer account." At the time of writing,v1.1 and v2 of the API both require user authentication. This means that a more elegant and strictly supported solution was sacrificed in adherence to the core requirement.
2. Only the tweet text and createtime is important to display to stdout. The API option will however print the enitre json object with full details
3. "new tweets" are assumed to be those identified by the default set of options from the advanced-search web API (https://twitter.com/search-advanced). Further details can be added/tweaked with modification to the search_options array in tweet_reader.py.
4. Assume in the 10 minute window, less than 100 tweets are made. If more than that, only the most recent 100 will be shown. This can be changed relatively easily by adding cursoring to the requests, however this was not seen as particularly important since the most active twitter user with > 50k followers only outputs ~135 tweets/day (source: https://sysomos.com/inside-twitter/most-active-twitter-user-data/)
5. Twitter's search service and, by extension, the Search API is not meant to be an exhaustive source of Tweets. Not all Tweets will be indexed or made available via the search interface --- https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
6. Tweet collection is assumed to have a negligible response time and is not factored into the 10 minute collection (i.e. if tweet collection always took 1 second, the program would actually run 10 minutes and 1 second apart)
7. To avoid confusion with updated tweets pushing more recent items to the bottom of stdout, tweets will be printed from least recent to most recent. 
8. Starting program again will remove previous collected tweets and that the programs memory is sufficent to hold JSON formatted data from the user (Otherwise conversion to another format is required). This is considered reasonable due to the low volumes of data we are expecting.
9. For simplicity of configuration, binding to port 5000 (The default for flask) is suitable to expose the API and the API will only be exposed locally