from flask import Flask, jsonify, request, redirect

app = Flask(__name__)

# Sample books data (10 books)
books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "year": 1925},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "genre": "Fiction", "year": 1960},
    {"id": 3, "title": "1984", "author": "George Orwell", "genre": "Dystopian", "year": 1949},
    {"id": 4, "title": "Moby Dick", "author": "Herman Melville", "genre": "Adventure", "year": 1851},
    {"id": 5, "title": "Pride and Prejudice", "author": "Jane Austen", "genre": "Romance", "year": 1813},
    {"id": 6, "title": "War and Peace", "author": "Leo Tolstoy", "genre": "Historical", "year": 1869},
    {"id": 7, "title": "The Catcher in the Rye", "author": "J.D. Salinger", "genre": "Fiction", "year": 1951},
    {"id": 8, "title": "Brave New World", "author": "Aldous Huxley", "genre": "Dystopian", "year": 1932},
    {"id": 9, "title": "The Hobbit", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1937},
    {"id": 10, "title": "The Lord of the Rings", "author": "J.R.R. Tolkien", "genre": "Fantasy", "year": 1954},
]

# ------------------------------------
# Buggy Case 1: Missing Field on POST
# ------------------------------------
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    new_book = {
        "id": len(books) + 1,
        "title": data.get("title"),  # Missing validation
        "author": data.get("author"),
        "genre": data.get("genre"),
        "year": data.get("year"),
    }
    books.append(new_book)  # Allows incomplete entries
    return jsonify(new_book), 201

# --------------------------------------
# Buggy Case 2: Case-Sensitivity in GET
# --------------------------------------
@app.route('/books/<title>', methods=['GET'])
def get_book(title):
    for book in books:
        if book["title"] == title:  # Case-sensitive
            return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# --------------------------------------
# Buggy Case 3: Duplicate Book Entries
# --------------------------------------
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books)

# ----------------------------------------
# Buggy Case 4: Empty GET Response Message
# ----------------------------------------
@app.route('/books/genre/<genre>', methods=['GET'])
def search_books_by_genre(genre):
    filtered_books = [book for book in books if book["genre"].lower() == genre.lower()]
    return jsonify(filtered_books), 200  # No message if empty

# --------------------------------------
# Buggy Case 5: Incorrect Error Codes
# --------------------------------------
@app.route('/invalid', methods=['GET'])
def invalid_route():
    return jsonify({"error": "Invalid route"}), 200  # Should be 404

# --------------------------------------
# Buggy Case 6: Hardcoded Responses
# --------------------------------------
@app.route('/hardcoded', methods=['GET'])
def hardcoded_response():
    return jsonify([{"id": 1, "title": "Fake Book", "author": "Unknown"}])  # Hardcoded

# ----------------------------------------
# Buggy Case 7: Incorrect Deletion Logic
# ----------------------------------------
@app.route('/books/<title>', methods=['DELETE'])
def delete_book(title):
    global books
    books = [book for book in books if book["title"] != title]  # Case-sensitive
    return jsonify({"message": "Book deleted"}), 200

# --------------------------------------
# Buggy Case 8: Infinite Loop
# --------------------------------------
@app.route('/loop/<title>', methods=['GET'])
def infinite_loop(title):
    while True:  # Infinite loop
        pass

# ----------------------------------------
# Buggy Case 9: No Validation in PATCH
# ----------------------------------------
@app.route('/books/<title>', methods=['PATCH'])
def update_book(title):
    data = request.json
    for book in books:
        if book["title"] == title:
            book.update(data)  # No validation
            return jsonify(book)
    return jsonify({"error": "Book not found"}), 404

# --------------------------------------
# Buggy Case 10: Broken Redirect
# --------------------------------------
@app.route('/redirect')
def broken_redirect():
    return redirect("http://invalid-url")  # Broken redirect

# --------------------------------------
# Buggy Case 11: Unhandled Empty Data
# --------------------------------------
@app.route('/books/add-empty', methods=['POST'])
def add_empty_book():
    data = {}
    new_book = {
        "id": len(books) + 1,
        "title": data.get("title"),  # Fails due to empty data
        "author": data.get("author"),
        "genre": data.get("genre"),
        "year": data.get("year"),
    }
    books.append(new_book)
    return jsonify(new_book), 201

# --------------------------------------
# Buggy Case 12: Missing Content-Type
# --------------------------------------
@app.route('/books/content-type', methods=['POST'])
def add_book_no_content_type():
    if not request.is_json:  # Missing Content-Type header
        return jsonify({"error": "Invalid Content-Type"}), 400
    return jsonify({"message": "Book added"}), 201

# --------------------------------------
# Buggy Case 13: Invalid JSON Format
# --------------------------------------
@app.route('/books/invalid-json', methods=['POST'])
def add_invalid_json():
    try:
        data = request.get_json()
        new_book = {
            "id": len(books) + 1,
            "title": data["title"],
            "author": data["author"],
            "genre": data["genre"],
            "year": data["year"],
        }
        books.append(new_book)
        return jsonify(new_book), 201
    except Exception as e:
        return jsonify({"error": "Invalid JSON format"}), 400

# --------------------------------------
# Buggy Case 14: Lack of Pagination
# --------------------------------------
@app.route('/books/pagination', methods=['GET'])
def get_books_no_pagination():
    return jsonify(books)  # Returns all books at once

# --------------------------------------
# Buggy Case 15: Static List Sorting
# --------------------------------------
@app.route('/books/sort', methods=['GET'])
def get_sorted_books():
    return jsonify(sorted(books, key=lambda x: x["title"]))  # Static sorting logic

# --------------------------------------
# Buggy Case 16: Error in Search Logic
# --------------------------------------
@app.route('/books/author/<author>', methods=['GET'])
def search_books_by_author(author):
    filtered_books = [book for book in books if author.lower() in book["author"].lower()]
    return jsonify(filtered_books if filtered_books else {"error": "Author not found"})

# --------------------------------------
# Buggy Case 17: Hidden Sensitive Data
# --------------------------------------
@app.route('/books/full-data', methods=['GET'])
def get_full_data():
    return jsonify(books)  # Exposes internal IDs unnecessarily

# --------------------------------------
# Buggy Case 18: Uncaught Timeout
# --------------------------------------
@app.route('/books/timeout', methods=['GET'])
def timeout_example():
    import time
    time.sleep(60)  # Long response time
    return jsonify({"message": "Request took too long"}), 200

# --------------------------------------
# Buggy Case 19: Overwriting IDs
# --------------------------------------
@app.route('/books/overwrite-id', methods=['POST'])
def overwrite_book_id():
    data = request.json
    data["id"] = 1  # Overwrites existing book ID
    books.append(data)
    return jsonify(data), 201

# --------------------------------------
# Buggy Case 20: Broken Error Handling
# --------------------------------------
@app.route('/broken-error', methods=['GET'])
def broken_error_handling():
    raise Exception("This is a deliberate error")  # No error handling

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
