from flask import Flask, render_template, request
import spotipy
import pandas as pd
#import logging
import json

#logging.basicConfig( level=logging.DEBUG)
#filename='demo.log',

#format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
#where the flask app will start running upon trigger.
#FLASK_APP=app.py
#point where Flask APP initiates.
app = Flask(__name__)

if __name__ == '__main__':
    app.debug = True
    app.run()

#app.config['DEBUG'] = True
SPOTIPY_CLIENT_ID='hidden'
SPOTIPY_CLIENT_SECRET='hidden'

from spotipy.oauth2 import SpotifyClientCredentials

""" Place client IDs in quotations - subsequently passes variable."""
def run_spclient():
    auth_manager = SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    playlists = sp.user_playlists('spotify')
    return sp
#obj = sp.recommendations(seed_artists=['spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg'], seed_genres=['soul'], limit = 5)
""" Test Pandas dataframe for printing on HTML"""
#test_data = pd.DataFrame({'track': ['Loyalty', 'Fear', 'Yah'], 'artist': ['Kendrick', 'Lamar', 'Duckworth']})

#render dataframe
# = test_data.to_html()

#text_file = open("Spotifytest.html", "w")

#text_file.close()
#print(track('spotify:track:21YVuJXatUwJnFS6CPExXj'))
#test program to insert data from HTML to flask, and return back to HTML>
@app.route('/', methods = ['GET', 'POST'])
def main():
    """df_marks = pd.DataFrame({"name": ['Kiko', 'Yui', 'Ian', 'Terra'],
                             "physics": [68, 74, 77, 78],
                             "chemistry": [84, 56, 73, 69],
                             "algebra": [78, 88, 82, 87]})
    prim = df_marks.to_json()
    return render_template('Spotifytest.html', prim = prim)"""

    #import list of genres for dropdown menu
    sp = run_spclient()
    l_gen = sp.recommendation_genre_seeds()['genres']
    l_genres = [x.capitalize() for x in l_gen]

    #form data returns recommendations - will display them in HTML.
    if request.method == 'POST':
        sp = run_spclient()
        genre =  (request.form['genres']).lower()  #"'"+ (request.form['genres']).lower() + "'"
        time = int(request.form['quantity'])
        #print(genre)
        seconds = time * 60
        dur = 0
        play_list = []
        input_genre = [genre]
        #play_list.update(sp.recommendations(seed_genres=['acoustic'], limit=10))
        #play_list.update(sp.recommendations(seed_genres=input_genre, limit=5))
        #play_list.update(sp.recommendations(seed_genres=input_genre, limit=5))
        j = 0
        while (dur < seconds):
            #recs = sp.recommendations(seed_genres=input_genre, limit=1)
            #print(recs.keys())
            #print(len(recs['tracks']))
            #print(recs['tracks'][0]['duration_ms'] // 1000)
            #print(recs.keys())
            #if 'tracks' not in recs.keys():
            play_list.append(sp.recommendations(seed_genres=input_genre, limit=1))
            #print(play_list[0]['tracks'][0]['duration_ms'])
            dur += ((play_list[j]['tracks'][0]['duration_ms']) // 1000)
            j += 1
        #print(i)
        #print(len(play_list))
        #print(play_list)
        #print(play_list[2]['tracks'])
        ch_list = pd.DataFrame({'track': [], 'artist': [], 'album': []})
        test = 0
        for i in play_list:
            #c1 = pd.DataFrame({'track': [(sp.track(i['tracks'][0]['uri'])['name'])], 'artist': [(i['artists'][0]['name'])],'album': [i['album']['name']]})
            c1 = pd.DataFrame({'track': [(sp.track(i['tracks'][0]['uri'])['name'])], 'artist': [(i['tracks'][0]['artists'][0]['name'])],'album': [i['tracks'][0]['album']['name']]})
            ch_list = ch_list.append(c1)
        ch_list.reset_index(inplace=True)
        ch = ch_list.to_json()
        return render_template('Spotifytest.html', l_genres = l_genres, ch = ch)

    #test JSON - will print out chart of recommended Kendrick tracks.
    obj = sp.recommendations(seed_artists=['spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg'], seed_genres=['soul'], limit=5)
    t_list = pd.DataFrame({'track': [], 'artist': [], 'album': []})
    for i in obj['tracks']:
        t1 = pd.DataFrame({'track': [(sp.track(i['uri'])['name'])], 'artist': [(i['artists'][0]['name'])],
                           'album': [i['album']['name']]})
        t_list = t_list.append(t1)
    t_list.reset_index(inplace=True)
    tj = t_list.to_json()


    return render_template('Spotifytest.html', l_genres = l_genres)

"""
@app.route('/', methods=['GET', 'POST'])
def results():

    sp = run_spclient()

    genre = request.form.get('genres')
    time = int(request.form.get('quantity'))
    seconds = time*60
    dur = 0
    play_list = {}
    play_list.update(sp.recommendations(seed_genres=[genre], limit=1))
    #while (dur < seconds):

        #recs = sp.recommendations(seed_genres=[genre], limit=1)
        #print(recs.keys())
        #print(len(recs['tracks']))
        #print(recs['tracks'][0]['duration_ms'] // 1000)
        #print(recs.keys())
        #if 'tracks' not in recs.keys():
        #dur += (recs['tracks'][0]['duration_ms'] // 1000)
        #play_list.update(recs)
    ch_list = pd.DataFrame({'track': [], 'artist': [], 'album': []})
    for i in play_list['tracks']:
        c1 = pd.DataFrame({'track': [(sp.track(i['uri'])['name'])], 'artist': [(i['artists'][0]['name'])],
                           'album': [i['album']['name']]})
        ch_list = ch_list.append(c1)
    ch_list.reset_index(inplace=True)
    ch = ch_list.to_json()


    #if request.method == 'POST': #form submitted
        #quantity = request.form.get('quantity')
    #logging.warning("lol")
    return render_template('Spotifytest.html', ch = ch, time = time)
"""
#@app.route('/', methods=['POST', 'GET'])
#def genres():
#    gen = request.form['genres']
#    return gen





#app = Flask(__name__)

"""Retrieves recommendations based on artist and genre IDs"""
# print(sp.recommendations(seed_artists='67lytN32YpUxiSeWlKfHJ3', , seed_genres="soul", seed_tracks=None, limit=5, country=None))
# print(sp.recommendations(seed_artists=['spotify:artist:1TtJ8j22Roc24e2Jx3OcU4'], seed_genres=['soul']))
#obj = sp.recommendations(seed_artists=['spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg'], seed_genres=['soul'], limit=5)

# print(sp.recommendation_genre_seeds())
#return render_template("index.html", accident_counts_bydistrict_yesbikelane_json=accident_counts_bydistrict_yesbikelane_json,  accident_counts_bydistrict_nobikelane_json=accident_counts_bydistrict_nobikelane_json, districts=districts  )
"""
#print(sp.track('spotify:track:7d5v4p5X0Vrf6RZdDigYVa'))
#while playlists:
#    for i, playlist in enumerate(playlists['items']):
       # print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
#    if playlists['next']:
        playlists = sp.next(playlists)
#    else:
#        playlists = None
"""
#test functions to check format of JSON file output.
#type(obj) #dictionary
#len(obj['tracks']) #5 tracks returned

#obj['tracks'] #returns



#unneeded code -- just hello world - delete later.
"""
@app.route('/')
def hello_world():
    return 'Hello World!'
    with open("newTest.csv", mode="w+") as file:
        fileWriter = csv.writer(file)
        fileWriter.writerow(['Time', 'HomeTeam', 'AwayTeam'])
    file.close()


if __name__ == '__main__':
    app.run()

//test to see if running at EOF works.
if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', post = '8080')
"""
