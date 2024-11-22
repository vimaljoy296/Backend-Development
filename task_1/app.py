# Constellation Explorer API
from flask import Flask, request, jsonify ,redirect
import requests

app = Flask(__name__)

# Sample constellation data
constellations = [
    {'id': 1, 'name': 'Orion', 'hemisphere': 'Northern', 'main_stars': ['Betelgeuse', 'Rigel', 'Bellatrix'], 'area': 594, 'origin': 'Greek'},
    {'id': 2, 'name': 'Scorpius', 'hemisphere': 'Southern', 'main_stars': ['Antares', 'Shaula', 'Sargas'], 'area': 497, 'origin': 'Greek'},
    {'id': 3, 'name': 'Ursa Major', 'hemisphere': 'Northern', 'main_stars': ['Dubhe', 'Merak', 'Phecda'], 'area': 1280, 'origin': 'Greek'},
    {'id': 4, 'name': 'Cassiopeia', 'hemisphere': 'Northern', 'main_stars': ['Schedar', 'Caph', 'Ruchbah'], 'area': 598, 'origin': 'Greek'},
    {'id': 5, 'name': 'Crux', 'hemisphere': 'Southern', 'main_stars': ['Acrux', 'Mimosa', 'Gacrux'], 'area': 68, 'origin': 'Latin'},
    {'id': 6, 'name': 'Lyra', 'hemisphere': 'Northern', 'main_stars': ['Vega', 'Sheliak', 'Sulafat'], 'area': 286, 'origin': 'Greek'},
    {'id': 7, 'name': 'Aquarius', 'hemisphere': 'Southern', 'main_stars': ['Sadalsuud', 'Sadalmelik', 'Sadachbia'], 'area': 980, 'origin': 'Babylonian'},
    {'id': 8, 'name': 'Andromeda', 'hemisphere': 'Northern', 'main_stars': ['Alpheratz', 'Mirach', 'Almach'], 'area': 722, 'origin': 'Greek'},
    {'id': 9, 'name': 'Pegasus', 'hemisphere': 'Northern', 'main_stars': ['Markab', 'Scheat', 'Algenib'], 'area': 1121, 'origin': 'Greek'},
    {'id': 10, 'name': 'Sagittarius', 'hemisphere': 'Southern', 'main_stars': ['Kaus Australis', 'Nunki', 'Ascella'], 'area': 867, 'origin': 'Greek'}
]

# The first endpoint is completed for your reference. Some endpoints have hints,
# and you must complete the others from scratch. Use principles of Uniform Interface.

# 1. View all constellations
# GET /constellations
@app.route('/constellations', methods=['GET'])
def get_all_constellations():
    return jsonify(constellations)

# 2. View a specific constellation by name
# GET /constellations/<name> (Path Parameter)
# 2. View a specific constellation by name
@app.route('/constellations/<name>', methods=['GET'])
def get_constellation(name):
    
    for c in constellations:
        if c['name'] == name:
            return jsonify(c)
        
    # Return a 404 response if the constellation is not found
    return jsonify({'error': 'Constellation not found'}), 404
   
# 3. Add a new constellation
@app.route('/constellations', methods=['POST'])
def add_constellation():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid input, JSON data is required'}), 400
    new_constellation = {
        'id': len(constellations) + 1,
        'name': data.get('name'),
        'hemisphere': data.get('hemisphere'),
        'main_stars': data.get('main_stars', []),
        'area': data.get('area'),
        'origin': data.get('origin')
    }
    constellations.append(new_constellation)
    return jsonify(new_constellation), 201

# 4. Delete a constellation
@app.route('/constellations/<name>', methods=['DELETE'])
def delete_constellation(name):
    global constellations
    constellations = [c for c in constellations if c['name'].lower() != name.lower()]
    return jsonify({'message': f'Constellation {name} deleted successfully'}), 200

# 5. Filter constellations by hemisphere and area
@app.route('/constellations/filters', methods=['GET'])
def filter_constellations():
    hemisphere = request.args.get('hemisphere')
    min_area = request.args.get('min_area', type=int, default=0)
    
    filtered_constellations = [
        c for c in constellations
        if (hemisphere is None or hemisphere.lower() in c['hemisphere'].lower()) and
           c['area'] >= min_area
    ]
    
    return jsonify(filtered_constellations), 200


# 6. View the main stars of a constellation specified by name
@app.route('/constellations/<name>/stars', methods=['GET'])
def get_main_stars(name):
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    
    if constellation:
        return jsonify({'main_stars': constellation['main_stars']}), 200
    else:
        # Redirect to the corresponding HTTP Cat image for 404 error
        return redirect(get_http_cat(404), code=302)
    
# 7. Partially update a constellation specified by name
@app.route('/constellations/<name>', methods=['PATCH'])
def update_constellation(name):
    constellation = next((c for c in constellations if c['name'].lower() == name.lower()), None)
    
    if constellation:
        data = request.get_json()
        
        if 'main_stars' in data:
            constellation['main_stars'] = data['main_stars']
        if 'origin' in data:
            constellation['origin'] = data['origin']
        if 'area' in data:
            constellation['area'] = data['area']
        if 'hemisphere' in data:
            constellation['hemisphere'] = data['hemisphere']
        
        return jsonify(constellation), 200
    else:
        # Redirect to the corresponding HTTP Cat image for 404 error
        return redirect(get_http_cat(404), code=302)

# 10. Double check that all the endpoints return the appropriate status codes.
# For errors, display the status code using an HTTP Cat - https://http.cat/
@app.errorhandler(404)
def not_found_error(error):
    return redirect("https://http.cat/404")

if __name__ == '__main__':
    app.run(debug=True)