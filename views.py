from flask import Flask, jsonify
import main
import json

app = Flask(__name__)

@app.route('/movie/<title>')
def search_by_title_page(title):
    return main.search_by_title(title)

@app.route('/movie/<int:year1>/to/<int:year2>')
def search_by_year_range_page(year1, year2):
    return main.search_by_year_range(year1, year2)

@app.route('/rating/<rating>')
def search_by_rating_page(rating):
    return main.search_by_rating(rating)

@app.route('/genre/<genre>')
def search_by_genre_page(genre):
    return main.search_by_genre(genre)

app.run()