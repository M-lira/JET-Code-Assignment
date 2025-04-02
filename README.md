# Restaurant Finder

## Description
This project is a simple Flask-based web application that allows users to search for the top 10 restaurants in the UK based on a postcode. It fetches restaurant data from the Just Eat API and displays the results in a clean, user-friendly interface. The application also integrates the Postcodes.io API to fetch the region associated with the entered postcode.

## Features
 - Validates UK postcodes using a regular expression.
 - Fetches and displays the top 10 restaurants in a given region based on user input.
 - Sorts restaurants by rating and displays key information such as cuisine, rating, and address.
 - Handles simple errors and provides informative messages to the user if no results are found.

## How to Build and Run

### Prerequisites

Make sure you have the following installed on your system:

- Python 3.13.2
- pip (Python package manager)
- Flask
- Requests library


### How to Install

Clone the repository:

- git clone https://github.com/M-lira/JET-Code-Assignment
- cd restaurant-finder

Create a virtual environment (optional but recommended):
- python -m venv venv
- On Linux and macOS, use `source venv/bin/activate`
- On Windows, use `venv\Scripts\activate`

Install the required dependencies:
- `pip install -r requirements.txt`

Create a requirements.txt file if you don't already have one. It should include:
- Flask==3.1.0
- requests==2.32.3

## Running the Application
- To start the Flask development server:
`python app.py`

- After running the command, open your browser and navigate to http://127.0.0.1:5000/.
- You should see the **Restaurant Finder** app running locally.

## Assumptions
 - **Postcode input**: Users are expected to enter valid UK postcodes. Basic regex validation is applied, but it may not cover all cases.
 - **Just Eat API**: The app depends on the Just Eat API for restaurant data. If the API changes, functionality may break.
 - **Region information**: The app uses the Postcodes.io API to find region details. If an invalid postcode is entered, the app will display "Unknown Region."."
- **Data availability**: The Just Eat API's response can vary based on postcode. Not all postcodes will necessarily have restaurant data available, which may result in a lack of results for certain areas.

## Improvements for Future Versions

Here are some ways to improve the project:

- **Better error handling**: Provide clearer error messages and backup options if the Just Eat or Postcodes.io APIs fail.
- **Improved postcode validation**: The current validation is basic and may not cover all UK postcode formats. A more advanced solution would ensure greater accuracy.
- **Better front-End features**: Add pagination and more filtering options to make browsing restaurants easier. Instead of only showing the top 10 highest-rated restaurants, allow users to search by cuisine type (e.g., Mexican, Burgers, Pizza) and meal preference (e.g., breakfast, lunch, dinner). Also, add filters to sort by star rating instead of only displaying the top-rated options.
- **Testing and documentation**: Improve reliability with automated tests and expand documentation to help future contributors.
- **Enhanced design**: Make the UI more interactive by adding sorting options and dynamic restaurant filters.

## Acknowledgements
- **Just Eat API**: For providing restaurant data.
- **Postcodes.io API**: For offering region information based on UK postcodes.
