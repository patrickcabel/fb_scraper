from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_cars
from db import init_db, get_listings

app = Flask(__name__)

# Enable CORS for all routes, restricted to your frontend (adjust the origin as needed)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Initialize the database
init_db()

@app.route('/api/listings', methods=['GET'])
def fetch_listings():
    listings = get_listings()
    return jsonify(listings)

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        make = data.get('make', '')
        model = data.get('model', '')

        if not make or not model:
            return jsonify({'success': False, 'error': 'Make and model are required'}), 400
        
        # Call scraper with make and model
        results = scrape_cars(make, model)
        
        if not results:
            return jsonify({
                'success': True,
                'data': [
                    { 'title': 'No results found', 'price': '-', 'link': '#' }
                ]
            })
        
        print("Scraped results:", results)
        return jsonify({ 'success': True, 'data': results })

    except Exception as e:
        print("Error during scraping:", str(e))
        return jsonify({ 'success': False, 'error': str(e) }), 500


if __name__ == '__main__':
    app.run(debug=True)
