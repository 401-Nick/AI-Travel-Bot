from serpapi import GoogleSearch
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_hotels(modelHotelQuery):
    """
    Fetch and clean hotel data from SerpAPI.

    Parameters:
    - modelHotelQuery (str or dict): JSON string or dictionary with search parameters for the SerpAPI query.

    Returns:
    - tuple: A cleaned hotel data dictionary (or error message) and a status string ("success" or "error").
    """
    print("Model requested to fetch hotel data...")
    try:
        # Convert JSON string to a dictionary if necessary
        if isinstance(modelHotelQuery, str):
            modelHotelQuery = json.loads(modelHotelQuery)

        # Add API key to the query
        modelHotelQuery["api_key"] = os.environ.get("SERP_API_KEY")

        # Ensure the query is a valid dictionary
        if not isinstance(modelHotelQuery, dict):
            return (
                "[ERROR] Invalid input format. Please provide a valid JSON object and try again.",
                "error",
            )

        # Execute the search using GoogleSearch API
        search = GoogleSearch(modelHotelQuery)
        results = search.get_dict()

        # Validate API response
        if not results or "error" in results:
            return (
                f"[ERROR] Error processing the hotel query. Try again. ERROR: {str(results)}",
                "error",
            )

        # Process and clean hotel data
        return clean_hotel_data(results), "success"

    except json.JSONDecodeError:
        return (
            "[ERROR] Invalid JSON format. Please provide a valid JSON object.",
            "error",
        )
    except Exception as e:
        return (
            f"[ERROR] An unexpected error occurred. ERROR: {str(e)}",
            "error",
        )


def clean_hotel_data(hotel_query_response):
    """
    Clean and structure the hotel data from the SerpAPI response.

    Parameters:
    - hotel_query_response (dict): Raw API response from SerpAPI.

    Returns:
    - dict: A dictionary containing a list of cleaned hotel data or an error message.
    """
    try:
        # Retrieve hotel data from the 'answer_box'
        hotels = hotel_query_response.get("answer_box", {}).get("hotels", [])
        if not hotels:
            return {"error": "No hotels found for the specified query."}

        # Extract relevant fields for each hotel
        cleaned_hotels = []
        for hotel in hotels:
            cleaned_hotels.append(
                {
                    "title": hotel.get("title"),
                    "price": hotel.get("price"),
                    "rating": hotel.get("rating"),
                    "reviews": hotel.get("reviews"),
                    "link": hotel.get("link"),
                    "features": hotel.get("features"),
                }
            )

        return {"hotels": cleaned_hotels}

    except Exception as e:
        return {"error": f"Failed to process hotel data: {str(e)}"}
