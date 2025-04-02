from flask import Flask, render_template, request
import requests
import re
import logging

app = Flask(__name__)

#URL for the API
API_URL = "https://uk.api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}"

#Pass through cloudfare block
HEADERS = {
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
     "Accept": "application/json",
     "Referer": "https://www.just-eat.co.uk/",
     "Origin": "https://www.just-eat.co.uk/",
}

# Fetch top 10 rstaurants for a given postcode
def fetch_restaurant_data(postcode):
    try:
        url = API_URL.format(postcode=postcode)
        response = requests.get(url, headers = HEADERS)

        if response.status_code == 200:

            data = response.json() #Parse the JSON response
            restaurants = data.get('restaurants', [])

            #sort restaurants rating in descending order
            restaurants.sort(key=lambda x: x.get('rating', {}).get('starRating', 0), reverse= True)

            return restaurants[:10] #return the top 10 restaurants
        else:
            logging.error(f"Error: {response.status_code} - {response.text}")
            return[]
    except Exception as e:
        logging.exception(f"An error occurred: {e}") #Log full exception details
        return[]

#Simple UK postcode validation using regex
def is_valid_postcode(postcode):
     #this regex is a basic validation for UK postcodes (it may not be exhaustive)
     postcode_regex = r"(GIR 0AA|[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}|[A-Z]{1,2}\d{1,2}[A-Z]? \d[A-Z]{2})$"
     return bool(re.match(postcode_regex, postcode.strip().upper()))

#Fetches the city/region associated with a UK postcode via API
def get_region_from_postcode(postcode):
     try: 
         url_region_API= f"https://api.postcodes.io/postcodes/{postcode}"
         response = requests.get(url_region_API)
         if response.status_code == 200:
             data = response.json()
             return data["result"]["admin_district"] # returns city or region nam
         else:
             print(f"Error while fetching the postcode region")
             return"Unknown Region"         
     except Exception as e:
         print(f"Error while fetching the postcode region")
         return"Unknown Region"

#filters the words I don't want to be shown as cuisines
def filter_cuisines(cuisine_list):
    excluded_cuisines = [
        "Deals", "Low Delivery Fee", "Cheeky Tuesday", "Freebies", 
        "Halal", "Local Legends", "Shops", "Collect stamps", "£8 off", " *NEW*"
    ]
    return [cuisine['name'] for cuisine in cuisine_list if cuisine['name'] not in excluded_cuisines]

#Route for the homepage
@app.route('/', methods=['GET', 'POST'])
def home(): # main function
    postcode = ""
    restaurants = []
    error_message= None
    region = 'Unknown Region'

    if request.method == 'POST':
            postcode = request.form.get('postcode', '').strip() 
            if postcode: #only proceed if postcode isn't empty  
                if is_valid_postcode(postcode):
                    region = get_region_from_postcode(postcode) # Get the city name, mainly for asthetic purposes
                    restaurants = fetch_restaurant_data(postcode)

                    if not restaurants:
                        error_message = "No restaurants found for this {region}."
                else: 
                    error_message = "Please enter a valid UK postcode."
            else:
                error_message = None
        
    #prepare the restaurant data for display
    restaurant_list = [{
                        'name' : restaurant.get('name','Unknown'),
                        'cuisines' : ', '.join(filter_cuisines( restaurant.get('cuisines', []))),
                        'rating': f"{restaurant.get('rating', {}).get('starRating', 'N/A')}⭐ ({restaurant.get('rating', {}).get('count', 0)} reviews)",
                        'address': restaurant.get('metaData', {}).get('district', region)
                }
                for restaurant in restaurants
            ] 
    return render_template('index.html', restaurants=restaurant_list, postcode=postcode, error_message=error_message, region=region)


    

if __name__ == '__main__':
    app.run(debug=True)