from flask import Blueprint, render_template, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/results')
def results():
    return render_template('results.html')

# API routes can be added here
@main.route('/api/data')
def get_data():
    return jsonify({"message": "API is working!"})
