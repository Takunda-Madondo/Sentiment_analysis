import os
from flask import Flask, request, render_template, jsonify
from twitter import TwitterClient

# Initialize the Flask application
app = Flask(__name__)

# Create an instance of the TwitterClient with a specific username
api = TwitterClient('@takunda_kagura')

# Function to convert string to boolean
def strtobool(v):
    return v.lower() in ["yes", "true", "t", "1"]

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch tweets based on query parameters
@app.route('/tweets')
def tweets():
    # Get the retweets_only parameter from the request
    retweets_only = request.args.get('retweets_only')
    api.set_retweet_checking(strtobool(retweets_only.lower()))
    
    # Get the with_sentiment parameter from the request
    with_sentiment = request.args.get('with_sentiment')
    api.set_with_sentiment(strtobool(with_sentiment.lower()))
    
    # Get the query parameter from the request
    query = request.args.get('query')
    api.set_query(query)

    # Fetch tweets based on the set parameters
    tweets = api.get_tweets()
    
    # Return the tweets in JSON format
    return jsonify({'data': tweets, 'count': len(tweets)})

# Run the application
if __name__ == '__main__':
    app.run()
