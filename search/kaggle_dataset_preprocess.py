import pandas as pd

songs = pd.read_csv("songdata.csv", header=0)
songs = songs[songs.artist != 'Lata Mangeshkar']
songs = songs[['song','text']]
songs.columns = ['name','text']
songs.to_csv('songs.csv', index=False)
