# Flask Airbnb Clone Template

This repository contains a minimal Flask application integrated with Supabase for authentication and data storage, along with a Google Maps integration to display property listings on an interactive map. It is designed as a starting point for building an Airbnb-style application.

## Features

* **Magic link authentication** via Supabase Auth. Users can request a magic link by entering their email, receive a link via email, and sign in without a password.
* **Session management** using Flask sessions and Supabase tokens. The app stores the current user's Supabase `access_token` and `refresh_token` in the session and uses them to fetch protected data.
* **Property listing map** powered by the Google Maps JavaScript API. Listings retrieved from Supabase are displayed as markers on the map with their name and price.
* **Mock data** for `user_profile` and `property_listings` tables stored in the `data/` directory. Use these JSON files to seed your Supabase database for development and testing.

## Setup

1. **Clone or download this repository** and navigate into the `airbnb_flask_app` directory.

2. **Create a virtual environment** (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** based on the provided `.env.example` and fill in your own Supabase credentials, Google Maps API key and Flask secret key.

5. **Seed your Supabase database** (optional). Import the JSON files from the `data/` directory into your Supabase project using the Supabase dashboard or CLI. These files contain mock entries for the `user_profile` and `property_listings` tables.

6. **Run the application**:

   ```bash
   python app.py
   ```

7. Open your browser to `http://localhost:5000` to see the app running.

## Security notes

* **Never commit your real Supabase credentials or Google Maps API key** to a public repository. Use environment variables and the `.env` file to keep secrets out of source control.
* This template is for educational purposes and does not include production-ready security features such as CSRF protection or rate limiting. Always harden your authentication flows before deploying a real application.

## Project structure

| Path | Description |
| --- | --- |
| `app.py` | Main Flask application containing routes for authentication, session management, and displaying the map with listings. |
| `templates/` | HTML templates rendered by Flask. |
| `static/` | Static assets like CSS. |
| `data/` | Mock JSON data for seeding Supabase tables. |
| `.env.example` | Example environment file. Copy to `.env` and set your own credentials. |
| `requirements.txt` | Python dependencies. |

## Further work

This template lays the foundation for a full-featured Airbnb-style app. Potential next steps include:

* Adding CRUD pages for property listings and user profiles.
* Implementing role-based access controls (hosts vs. guests).
* Handling booking and payment workflows.
* Deploying the application (e.g. on Heroku, Fly.io, or Render) and setting up a custom domain.

Feel free to extend this project as needed. Contributions and improvements are welcome!
