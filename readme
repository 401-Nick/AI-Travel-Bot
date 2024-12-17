# Vacation Planner Assistant

This project is an AI-driven **vacation planner assistant** that engages users in dynamic conversations to provide **real-time hotel recommendations**. Built using Google's Generative AI and integrated with **SerpAPI**, it seamlessly combines AI capabilities with live data to simplify vacation planning.

---

## Features

- **Real-Time Hotel Search**: Fetch live hotel recommendations tailored to the user's preferences (e.g., location, dates, price range, amenities).
- **Intelligent Conversations**: The assistant uses Google's `gemini` model to maintain a natural and interactive conversation flow.
- **Tool Integration**: AI seamlessly triggers real-time hotel queries using **SerpAPI**.
- **Timezone Awareness**: Handles timezone differences explicitly to ensure accurate date handling for bookings.
- **Error Handling**: Provides clear feedback in case of invalid inputs or unexpected issues.
- **Interactive Console**: Users can engage directly via a clean and conversational command-line interface.

---

## Setup Instructions

### 1. Prerequisites
Ensure you have the following installed and set up:

- **Python 3.8 or higher**  
- **Environment Variables**  
   - `GOOGLE_API_KEY`: API key for Google Generative AI.  
   - `SERP_API_KEY`: API key for SerpAPI hotel data.  

---

### 2. Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/401-Nick/AI-Travel-Bot
   cd AI-Travel-Bot
   ```

2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the project root directory.
   - Add the following keys:
     ```
     GOOGLE_API_KEY="your_google_api_key"
     SERP_API_KEY="your_serpapi_key"
     ```

---

### 3. Running the Project

To start the assistant, run:

```bash
python main.py
```

### 4. Interacting with the Assistant

- Launch the assistant and type your query (e.g., "Find hotels in New York for next weekend").
- Type `exit` or `quit` to end the conversation.

---

## How It Works

1. **User Input**: The assistant engages the user for details like destination, check-in/out dates, price range, etc.
2. **Hotel Search Trigger**: The assistant identifies hotel-related queries and fetches data via **SerpAPI**.
3. **Live Results**: Processed hotel data is displayed with ratings, price estimates, and direct booking links.
4. **Dynamic Follow-ups**: AI ensures the conversation flows naturally while accommodating user preferences.

---

## Example Interaction

**User**: *Find hotels in Los Angeles for December 16-20 under $300.*  
**Assistant**:
```
Fetching top-rated hotels in Los Angeles from Dec 16 to Dec 20 within a $300 budget...
Hotel 1: Sunset Inn
Price: $285/night
Rating: 4.6⭐
[Link to Hotel Booking]
Features: Free Wi-Fi, Parking, Outdoor Pool
```

---

## Error Handling

If the AI encounters an issue:
- It retries the hotel search.
- If invalid data is provided, the assistant requests clarification.

---

## Technology Stack

- **AI Model**: Google Generative AI (`gemini-2.0-flash-exp`)
- **Real-Time Data**: SerpAPI for hotel search
- **Language**: Python 3
- **Environment Management**: `dotenv` for API keys
- **CLI Interaction**: Console-based user input/output

---