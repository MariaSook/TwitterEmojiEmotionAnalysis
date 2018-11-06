import tweepy
import emoji
import geocoder
import requests
import copy

from matplotlib import pyplot as plt
import xlsxwriter
from matplotlib.colors import LogNorm

consumer_key = "gTOiHFrbwzok0Y9RO0f4tYBxE"
consumer_secret = "6PreYoQI44yRSGijltpHcyPYWuKMPA9oYeOJHL6lgjwxbUEnFZ"

access_token = "998811230860070912-X7mhWfQT6J6M7eRvJdoGp96TVoDd1Ft"
access_token_secret = "6ywc79Qsaj7CBBykJr9G8GQw8eZ4d5XemezxqIRxHE5xv"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#query = "1F602"
#tweetCount = 10

#tweets = api.search(q=query, count=tweetCount)
#tweets = api.user_timeline('chrissyteigen')

def unicodeExtractor(tweet, tweetString):
    if (not tweet.retweeted) and ('RT @' not in tweetString):
        emojiList = []
        for char in tweetString:
            if char in emoji.UNICODE_EMOJI:
                emojiList.append(f'U+{ord(char):X}')
                #emojiList.append(char.encode('unicode-escape'))
                #s = char.encode('unicode-escape')
                #print(s.decode('unicode-escape'))
        if emojiList == []:
            return 0
        else:
            return emojiList
    else:
        return 0

def tweetLocation(tweet):
    try:
        if (not tweet.retweeted) and ('RT @' not in tweet.text):
            tul = tweet.user.location
            if tweet.coordinates is not None:
                coords, c = [], tweet.coordinates.get('coordinates')
                coords.append(c[1])
                coords.append(c[0])
                return coords
            elif tweet.coordinates is None and tweet.place is not None:
                g = geocoder.google(tweet.place)
                if g.ok:
                    return g.latlng
                return 0
            elif tweet.place is None and (tul is not None or tul is not "" or tul is not " "):
                g = geocoder.google(tweet.user.location)
                if g.ok:
                    return g.latlng
                elif '|' in tul:
                    geo = geocoder.google(tul.split('|')[0])
                    return geo.latlng
                return 0
            else:
                return 0
        else:
            return 0
    except requests.exceptions.RequestException as e:
        return 0

def histogram(df, emoji):
    lat = []
    lon = []
    for row in df.rows:
        if emoji in row:
            lat.append(row.column('latlon')[0])
            lon.append(row.column('latlon')[1])

    center = [21.790107,-21.135572]
    return density_map(lat, lon, center)


def density_map(latitudes, longitudes, center, bins=100000, radius=0.1):
    cmap = copy.copy(plt.cm.jet)
    cmap.set_bad((0, 0, 0))  # Fill background with black

    # Center the map around the provided center coordinates
    histogram_range = [
        [center[1] - radius, center[1] + radius],
        [center[0] - radius, center[0] + radius]
    ]

    fig = plt.figure(figsize=(5, 5))
    plt.hist2d(longitudes, latitudes, bins=bins, norm=LogNorm(),
               cmap=cmap, range=histogram_range)

    # Remove all axes and annotations to keep the map clean and simple
    plt.grid('off')
    plt.axis('off')
    fig.axes[0].get_xaxis().set_visible(False)
    fig.axes[0].get_yaxis().set_visible(False)
    plt.tight_layout()
    plt.show()

latlonlist = []
emojislist = []
timelist = []

#
# for tweet in tweets:
#     e = unicodeExtractor(tweet, tweet.text)
#     #ll = tweetLocation(tweet)
#
#     if e is not 0 and e is not None:
#         ll = tweetLocation(tweet)
#         #if ll is not 0 and ll is not None:
#         emojislist.append(e)
#         #    latlonlist.append(ll)
#         #    timelist.append(str(tweet.created_at))
#
# print(emojislist)



query = '1F602' # u'\U0001F602'

max_tweets = 30
search = tweepy.Cursor(api.search, q=query).items(max_tweets)
for status in search:
    print (status.text)

#df = pd.DataFrame({'Lat Lon': latlonlist, 'Emojis': emojislist,'Time': timelist})

#writer = pd.ExcelWriter('twitter_data_excel.xlsx', engine='xlsxwriter')
#df.to_excel(writer, sheet_name='Sheet1')
#writer.save()

#histogram(df, b'\\U0001f62d')
