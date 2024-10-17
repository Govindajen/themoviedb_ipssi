from flask import Flask, jsonify, request, render_template, redirect, url_for #import objects from the Flask model
app = Flask(__name__) #define app using Flask

import os
from dotenv import load_dotenv

import requests

################################################################################à
load_dotenv() 

tmdb_apikey = os.getenv('MOVIE_API')
tmdb_url = "https://api.themoviedb.org/3/movie/550"
tmdb_image_url = "https://image.tmdb.org/t/p/original/"
headers = {
	"accept": "application/json",
	"Authorization": 'Bearer ' + tmdb_apikey
	}

# response = requests.get(url, headers=headers)

# print(response.json())

movie = {}
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/testrouter/<int:movie_id>')
def movie_test(movie_id):

	movie_request = requests.get(tmdb_url + str(movie_id), headers=headers)
	movie_data = movie_request.json()
	return jsonify(movie_data)


@app.route('/get_movie', methods=['GET'])
def get_movie():
    movie_id = request.args.get('movie_id')
    if movie_id:
        return redirect(url_for('movie_details', movie_id=movie_id))
    return 'Movie ID is required', 400


@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
	movie_request = requests.get(tmdb_url + str(movie_id), headers=headers)

	if movie_request.status_code == 200:
		movie_data = movie_request.json()
		movie_info = {
		"title": movie_data['original_title'],
		'genres': movie_data['genres'][0]['name'],
		'release_date': movie_data['release_date'],
		'img': tmdb_image_url + movie_data['poster_path'],
		'overview': movie_data['overview'],
		'vote_average': movie_data['vote_average']
		}
		return render_template('movie.html', moviedata=movie_info)
	else:
		return render_template('index.html', error='Error, movie noy found')



#######################################################################
if __name__ == '__main__':
	app.run(debug=True, port=8080) #run app on port 8080 in debug mode
