# Constellation Explorer API
from flask import Flask, request, jsonify

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

# 5. Filter constellations by hemisphere and area (Query String)
@app.route('/constellations/filter', methods=['GET'])
def filter_constellations():
    hemisphere = request.args.get('hemisphere')
    min_area = request.args.get('min_area', type=int)
    max_area = request.args.get('max_area', type=int)
    
    filtered = constellations
    if hemisphere:
        filtered = [c for c in filtered if c['hemisphere'].lower() == hemisphere.lower()]
    if min_area is not None:
        filtered = [c for c in filtered if c['area'] >= min_area]
    if max_area is not None:
        filtered = [c for c in filtered if c['area'] <= max_area]
    
    return jsonify(filtered)

# 6. View the main stars of a constellation specified by name
@app.route('/constellations/<name>/stars', methods=['GET'])
def get_main_stars(name):
    for c in constellations:
        if c['name'].lower() == name.lower():
            return jsonify({'name': c['name'], 'main_stars': c['main_stars']})
    return jsonify({'error': 'Constellation not found'}), 404

# 7. Partially update a constellation specified by name
@app.route('/constellations/<name>', methods=['PATCH'])
def update_constellation(name):
    data = request.json
    for c in constellations:
        if c['name'].lower() == name.lower():
            if 'main_stars' in data:
                c['main_stars'] = data['main_stars']
            if 'hemisphere' in data:
                c['hemisphere'] = data['hemisphere']
            if 'area' in data:
                c['area'] = data['area']
            if 'origin' in data:
                c['origin'] = data['origin']
            return jsonify(c), 200
    return jsonify({'error': 'Constellation not found'}), 404

# 8. For a constellation specified by name, view the image
# You might have to use an image generator API - try https://imagepig.com/

@app.route('/constellations/<name>/image', methods=['GET'])
def get_constellation_image(name):
    for c in constellations:
        if c['name'].lower() == name.lower():
            # You can integrate a real image API here if desired
            image_url = f"https://example.com/images/{name.lower()}.jpg"  # Placeholder URL
            return jsonify({'name': c['name'], 'image_url': image_url})
    return jsonify({'error': 'Constellation not found'}), 404


# 9. Add a new custom endpoint (e.g., Find constellations by origin)
@app.route('/constellations/origin/<origin>', methods=['GET'])
def get_constellations_by_origin(origin):
    filtered = [c for c in constellations if c['origin'].lower() == origin.lower()]
    if filtered:
        return jsonify(filtered)
    else:
        return jsonify({'error': 'No constellations found with that origin'}), 404

# 10. Double check that all the endpoints return the appropriate status codes.
# For errors, display the status code using an HTTP Cat - https://http.cat/
@app.route('/http-cat-example', methods=['GET'])
def http_cat_example():
    # This endpoint demonstrates error status codes using HTTP Cat
    return jsonify({'message': 'This endpoint is a demonstration of HTTP status codes'}), 400  # Example 400 error


if __name__ == '__main__':
    app.run(debug=True)