from flask import Flask, render_template
import requests
import re

app = Flask(__name__)

#URL for the API
API_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"

#Pass through cloudfare block
HEADERS = {
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive"
}


# Fetch top 10 rstaurants for a given postcode
def fetch_restaurant_data(postcode):
    try:
        response = requests.get(API_URL.format(postcode = postcode), headers = HEADERS)

        if response.status_code == 200:
            data = response.json() #Parse the JSON response
            restaurants = data.get('restaurants', [])[:10]
            return restaurants
        
        else:
            print( f"Error: {response.status_code} - {response.text}")
            return []
        
    except Exception as e:
        print(f"An error as ocurred: {e}")
        return []




#Route for the homepage
@app.route('/')

# Main data handling 
def home():

    postcode = "M16 0RA" #This is the default code choosen but it can be replaced with the desired one as long as it is within the UK region
    restaurants = fetch_restaurant_data(postcode)

    #prepare the restaurant data for display
    restaurant_list = []
    for restaurant in restaurants:
                name = restaurant.get('name')
                cuisines = ','.join([cuisine ['name'] for cuisine in restaurant.get('cuisines', [])])
                rating_info = restaurant.get('rating',{})
                rating = f"{rating_info.get('starRating', 'N/A')}⭐ ({rating_info.get('count', 0)} reviews)"
                address = restaurant.get('address', {}).get('line_1', 'No address listed')
   
                restaurant_list.append({
                        'name' : name,
                        'cuisines' : cuisines,
                        'rating' : rating,
                        'address' : address
                    })
    return render_template('index.html', restaurants=restaurant_list)


    

if __name__ == '__main__':
    app.run(debug=True)