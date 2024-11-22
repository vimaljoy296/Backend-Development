from flask import Flask, request, jsonify, redirect, url_for
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

# Predefined username and password for Basic Auth
stored_username = "vial"
stored_password = "1234567"

# Predefined Bearer token
VALID_TOKEN = "my_secure_token_123"

# GitHub OAuth configuration
CLIENT_ID = "Ov23liexrAtpcKOUuqyv"
CLIENT_SECRET = "a2e8e8908f84a21e58e7cf4cba0e9561725e3a81"
AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"
API_BASE_URL = "https://api.github.com/user"

@app.route('/basic-auth', methods=['GET'])
def basic_auth():
    """
    Handle Basic Authentication.
    Validates username and password from the request authorization header.
    """
    # Check if Authorization header is provided
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Authorization header missing or invalid format."}), 401

    # Extract username and password
    username = auth.username
    password = auth.password

    # Check if username and password match
    if username == stored_username and password == stored_password:
        return jsonify({"message": "Welcome to my website!"}), 200
    else:
        return jsonify({"message": "Unauthorized. Incorrect username or password."}), 401


@app.route('/bearer-auth', methods=['GET'])
def bearer_auth():
    """
    Handle Bearer Token Authentication.
    Validates the token provided in the Authorization header.
    """
    # Get Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({"message": "Authorization header is missing."}), 401

    # Check if the header starts with 'Bearer ' and extract the token
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        return jsonify({"message": "Invalid Authorization header format. Use 'Bearer <token>'."}), 401

    # Validate token
    if token == VALID_TOKEN:
        return jsonify({"message": "Welcome to my website!"}), 200
    else:
        return jsonify({"message": "Unauthorized. Invalid token."}), 401


# Route to start GitHub OAuth flow
@app.route('/oauth', methods=['GET'])
def oauth():
    # Redirect the user to GitHub's OAuth authorization page
    github_authorization_url = f"{AUTHORIZATION_BASE_URL}?client_id={CLIENT_ID}&scope=user"
    return redirect(github_authorization_url)


# Callback route that GitHub will redirect to after user authorization
@app.route('/callback', methods=['GET'])
def callback():
    # GitHub redirects here with a `code` query parameter
    code = request.args.get('code')
    if not code:
        return jsonify({"message": "Authorization code is missing."}), 400
    
    # Exchange the code for an access token
    response = requests.post(TOKEN_URL, data={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code
    }, headers={'Accept': 'application/json'})
    
    # Parse the response from GitHub
    token_data = response.json()
    access_token = token_data.get('access_token')
    
    if not access_token:
        return jsonify({"message": "Unable to fetch access token."}), 400
    
    # Use the access token to get the user's GitHub profile
    user_response = requests.get(API_BASE_URL, headers={'Authorization': f'token {access_token}'})
    
    if user_response.status_code == 200:
        user_data = user_response.json()
        return jsonify({
            "message": "Welcome to my website!",
            "user": user_data
        }), 200
    else:
        return jsonify({"message": "Failed to fetch user data."}), 500


if __name__ == '__main__':
    app.run(debug=True)
