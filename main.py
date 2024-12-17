import os
import google.generativeai as genai
from dotenv import load_dotenv
from hotels import get_hotels
import json
from datetime import datetime, timezone

# Load API key
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY is missing. Set it in the environment variables.")

# Configure the Generative AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    # model_name="gemini-1.5-flash",
    model_name="gemini-2.0-flash-exp",
    system_instruction="""
    You are a vacation planner assistant. Do not repeatedly pester the user for details but be explicit about the details you need from the user before using [HOTELS][/HOTELS] such as the location, check-in and check-out dates, number of beds, etc.
    Be very considerate about timezones and always take the user's timezone into account when booking flights or hotels. Be explicit about the timezone switches you make.
    You can use
    [FLIGHTS]
    [/FLIGHTS]
    to search for flights and I will provide the results.
    THIS IS A REAL TOOL THAT CAN BE USED TO ACCESS REAL-TIME DATA. DO NOT MENTION YOUR USE OF IT UNLESS EXPLICTLY USING THE TOOL. DO NOT ASK FOR OPTIONAL DATA UNLESS THE USER MENTIONS IT FIRST.
    [HOTELS] can be used as a search engine or tool to find hotels. You have access to it by encapsulating the search query in the following type and format:
    [HOTELS]
    {
        "q": "New York Hotels", REQUIRED The general query of the hotel
        "check_in_date": "2024-12-16", REQUIRED YYYY-MM-DD The check-in date must be today or later
        "check_out_date": "2024-12-17", REQUIRED YYYY-MM-DD The check-out date must be after the check-in date
        "gl": "us", REQUIRED 2-letter country code Default is what the user's message is in
        "hl": "en", REQUIRED 2-letter language code Default is what the user's message is in
        "currency": "USD", REQUIRED 3-letter currency code Default is USD
        "adults": "5", REQUIRED number of adults
        "children": "0", OPTIONAL number of children
        "min_price": "100", REQUIRED minimum price The user doesn't have to provide both min_price and max_price, but a single price is required.
        "max_price": "500", REQUIRED maximum price. The user doesn't have to provide both min_price and max_price, but a single price is required.
        "amenities": "1,3,4", OPTIONAL comma-separated list of amenity codes. This would search for hotels with free parking, parking, and indoor pool.
        "property_types": "12,13", OPTIONAL comma-separated list of property type codes
        "free_cancellation": "true", OPTIONAL boolean value
        "hotel_class": "3", OPTIONAL hotel class between 2 and 5
        "sort_by": "8", OPTIONAL sort by 3 - Lowest price, 8 - Highest rating, 13 - Most reviewed, Default is 8
    }
    [/HOTELS]
    Amenity codes, DO NOT MENITON THESE TO THE USER. IF THE USER ASKS FOR AN AMENITY THAT ISN'T IN THE LIST, USE THE CLOSEST MATCH:
    1: Free parking
    3: Parking
    4: Indoor pool
    5: Outdoor pool
    6: Pool
    7: Fitness center
    8: Restaurant
    9: Free breakfast
    10: Spa
    11: Beach access
    12: Child-friendly
    15: Bar
    19: Pet-friendly
    22: Room service
    35: Free Wi-Fi
    40: Air-conditioned
    52: All-inclusive available
    53: Wheelchair accessible
    61: EV charger
    Hotel property types, DO NOT MENTION THESE TO THE USER:
    12: Beach hotels
    13: Boutique hotels
    14: Hostels
    15: Inns
    16: Motels
    17: Resorts
    18: Spa hotels
    19: Bed and breakfasts
    20: Other
    21: Apartment hotels
    22: Minshuku
    23: Japanese-style business hotels
    24: Ryokan
    The template outlines the format for requesting hotel data.
    Prioritize the ratings to prices of the hotels in the search results and always show a single link to the hotel.
    The price can fluctuate so tell the user to check the booking website for the most accurate price.
    Example usage of [HOTELS][/HOTELS]:
    Model: [HOTELS]{ "q": "New York Hotels", "check_in_date": "2024-12-16", "check_out_date": "2024-12-17", "gl": "us", "hl": "15", "currency": "USD", "adults": "5", "children": "0", "min_price": "100", "max_price": "500",}[/HOTELS]
    User: (hotelBookingData)
    Model: Hotel 1: [Hotel Name]\\nPrice: [Price]\\nRating: 4.5\\n[a single link]\\nFeatures: [Hotel Features]\\n Fun Fact: [If you have any fun facts or training data about the hotel, you can include them here.]
    Example usage of [HOTELS][/HOTELS] after receiving an error:
    Model: [HOTELS]{ "q": "New York Hotels", "check_in_date": "2024-12-16", "check_out_date": "2024-12-17", ... }[/HOTELS]
    User: [ERROR] Invalid JSON format. Please provide a valid JSON object and try again.
    Model: It looks like I improperly formatted the hotel query. Trying again. [HOTELS]{ "q": "New York Hotels", "check_in_date": "2024-12-16", "check_out_date": "2024-12-17", ... }[/HOTELS]
    User: (hotelBookingData)
    Model: [Hotel Name]\\n[Price]\\n[Rating]\\n[a single link]\\n[Hotel Features]\\n Fun Fact: [If you have any fun facts or training data about the hotel, you can include them here.]
    """,
)

chat = model.start_chat()


def clear_console():
    """Clear the console screen."""
    os.system("cls" if os.name == "nt" else "clear")


# 1. Start the conversation with the model, handle user input, and print the final responses
def startConversation():
    """
    Start the conversation with the model and handle user input.

    Returns:
    - None: Prints the final response to the user.
    """
    clear_console()
    while True:
        user_message = input("You: ")
        if user_message.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        clear_console()

        # Add timezone to the user message for the model
        timestamped_message = (
            f"{datetime.now(timezone.utc).isoformat()} | {user_message}"
        )

        response = process_model_response(chat_with_model(timestamped_message))

        print(f"Travel Assistant: {response}")


# 2. Send a message to the model and return its response
def chat_with_model(message):
    """
    Send a message to the model and return its response.

    Parameters:
    - message (str): The user input message.

    Returns:
    - str: The model response.
    """
    try:

        response = chat.send_message(message)
        return response.text

    except Exception as e:
        return f"Error: {e}"


# 3. Process the model response and execute [HOTELS] queries if found
def process_model_response(response):
    """
    Handle the model response and execute [HOTELS] queries if found.

    Parameters:
    - response (str): The response from the model.

    Returns:
    - str: The final response to the user.
    """
    while "[HOTELS]" in response and "[/HOTELS]" in response:
        query = response.split("[HOTELS]")[1].split("[/HOTELS]")[0]
        hotel_tool_response = use_hotel_tool(query)
        response = chat.send_message(hotel_tool_response).text
    return response


# 4. If [HOTELS] is found in the model response, fetch hotel data using the get_hotels function
def use_hotel_tool(query):
    """
    Fetch hotel data using the get_hotels function.

    Parameters:
    - query (str): JSON string with hotel search parameters.

    Returns:
    - str: JSON response if successful, or an error message.
    """
    try:
        response, response_type = get_hotels(query)
        return (
            json.dumps(response) if response_type == "success" else f"Error: {response}"
        )
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    startConversation()
