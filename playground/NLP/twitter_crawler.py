# python-twiter only works for 3.5
import twitter

api = twitter.Api(consumer_key='TWmKyljuWlPAZx0tRv8KvfGYC',
                          consumer_secret='Zu7oEOm56CKC6lS9w7URXh7uqduXv1086WSOoI30hjyJlJ3D3r',
                          access_token_key='2370561757-sQkeKvT17gB8kmVAatONcKLLzlJoLKFM0nDfNuN',
                          access_token_secret='4By7EsIiRyum8laJZHeStZyJM4pzpPZTzLG3WIhC7PfJL')
print(api.VerifyCredentials())

# See more: https://github.com/bear/python-twitter

# Apply filter and Crawl twits
results = api.GetSearch(
    raw_query="q=twitter%20&result_type=mixed&lang=en&since=2018-01-01&count=100")
print(results)

for twit in results:
    print(twit.text)

print(len(results))

# Save filtered twits to the database - for annotation and analysis
