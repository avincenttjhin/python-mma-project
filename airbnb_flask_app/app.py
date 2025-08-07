import json
import os
from urllib.parse import urlencode, urlparse, parse_qs

from flask import (Flask, redirect, render_template, request, session,
                   url_for, flash)
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables from .env if present
load_dotenv()

# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")
SUPABASE_SERVICE_ROLE = os.getenv("SUPABASE_SERVICE_ROLE")

# Google Maps API key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Magic link redirect URL
MAGIC_LINK_REDIRECT_URL = os.getenv(
    "MAGIC_LINK_REDIRECT_URL", "http://localhost:5000/auth/callback"
)

if not SUPABASE_URL or not SUPABASE_ANON_KEY:
    raise RuntimeError(
        "Supabase credentials are not configured. Please set SUPABASE_URL and SUPABASE_ANON_KEY in your .env file."
    )

# Initialize Supabase clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

supabase_admin: Client | None = None
if SUPABASE_SERVICE_ROLE:
    # Create a second client with the service role key for privileged operations
    supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", os.urandom(24))

def get_property_listings() -> list[dict]:
    """Retrieve property listings from Supabase or fallback to local JSON."""
    listings: list[dict] = []
    try:
        client = supabase_admin if supabase_admin else supabase
        response = client.table("property_listings").select("*").execute()
        if response.data:
            listings = response.data
    except Exception:
        # If Supabase is unreachable (e.g. offline development), load from local file
        data_path = os.path.join(os.path.dirname(__file__), "data", "property_listings.json")
        with open(data_path, "r") as f:
            listings = json.load(f)
    return listings

@app.route("/")
def index():
    listings = get_property_listings()
    return render_template(
        "index.html",
        listings=listings,
        google_api_key=GOOGLE_MAPS_API_KEY,
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        if not email:
            flash("Please provide a valid email address.")
            return render_template("login.html")
        try:
            # Send a magic link to the provided email address
            supabase.auth.sign_in_with_otp(
                email=email,
                options={
                    "email_redirect_to": MAGIC_LINK_REDIRECT_URL,
                },
            )
            flash(
                "If an account exists for this address, a magic link has been sent. Please check your email to continue."
            )
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error sending magic link: {e}")
            return render_template("login.html")
    # GET request
    return render_template("login.html")

@app.route("/auth/callback")
def auth_callback():
    """Handle the redirect from the magic link and set the session."""
    # Supabase will include access_token and refresh_token in the query string
    access_token = request.args.get("access_token")
    refresh_token = request.args.get("refresh_token")
    if not access_token or not refresh_token:
        flash("Invalid or expired magic link. Please try logging in again.")
        return redirect(url_for("login"))
    try:
        # Set the session on the supabase client to authenticate as this user
        supabase.auth.set_session(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        # Retrieve the user information
        user = supabase.auth.get_user().user
        # Store user and tokens in Flask session
        session["user"] = {
            "id": user.id,
            "email": user.email,
        }
        session["access_token"] = access_token
        session["refresh_token"] = refresh_token
        flash("Logged in successfully!")
        return redirect(url_for("index"))
    except Exception as e:
        flash(f"Authentication failed: {e}")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    """Sign the user out of Supabase and clear the session."""
    try:
        # Sign out of Supabase (may raise if no session)
        supabase.auth.sign_out()
    except Exception:
        pass
    # Clear the Flask session
    session.clear()
    flash("You have been logged out.")
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Run the Flask development server
    app.run(debug=True, host="0.0.0.0", port=5000)
