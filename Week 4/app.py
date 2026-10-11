from flask import Flask, jsonify, request, send_file, make_response
from flask_swagger_ui import get_swaggerui_blueprint
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import Schema, fields
from flask_httpauth import HTTPTokenAuth
import uuid, yaml, jwt

app = Flask(__name__)
app.config['SECRET-KEY'] = 'october19'

books = {
    "85d132be-8d1a-42bc-ba9c-8ed6d87d5709": {
        "id": "85d132be-8d1a-42bc-ba9c-8ed6d87d5709",
        "title": "Wild Flower of Armagada",
        "author": "Harvey Rookside"
    },
    "fa8a0e9f-70ad-4940-9571-8ebfdcf00d20": {
        "id": "fa8a0e9f-70ad-4940-9571-8ebfdcf00d20",
        "title": "Echoes of Tomorrow",
        "author": "Marcus Vail"
    },
    "c4b1a9e2-3f6b-4c9d-bb9e-2a1f4e7d9a22": {
        "id": "c4b1a9e2-3f6b-4c9d-bb9e-2a1f4e7d9a22",
        "title": "Whispers in the Library",
        "author": "Nora Finch"
    }
}
def error_response(type_, title, status, detail, instance):
    body = {
        "type": type_,
        "title": title,
        "status": status,
        "detail": detail or None,
        "instance": instance or None
    }

    response = make_response(jsonify(body))
    response.status_code = status
    response.headers["Content-Type"] = "application/problem+json"
    return response

def isValidUUID(uuid_, version=4):
    try:
        uuid_obj = uuid.UUID(str(uuid_), version=version)
    except ValueError:
        return False
    return True

# /books
@app.route("/books", methods=["GET"])
def list_books():
    return jsonify(list(books.values())), 200

@app.route("/books", methods=["POST"])
def create_book():
    try:
        data = request.get_json(force=True)
    except Exception:
        return error_response("/bad-request", "Bad Request", 400, "Invalid request format.", f"/books")
    data = request.get_json()
    if not data or "id" not in data or "name" not in data:
        return error_response(
            type_='/unprocessable-content',
            title='Unprocessable Content',
            status= 422,
            detail="The request contain invalid information.",
            instance="/books"
        )
    if data["id"] in books:
        return error_response(
            type_= "/conflict",
            title= "Conflict",
            status= 409,
            detail= "Conflict between the request and internal server state.",
            instance= "/books"
        )
    books[data["id"]] = data
    return jsonify(data), 201

@app.route("/books/<uuid:bookId>", methods=["GET"])
def get_book(bookId):
    if not bookId or not isValidUUID(bookId):
        return error_response("/bad-request", "Bad Request", 400,
                              "Invalid request format.",
                              f"/books/{bookId}")
    book = books.get(str(bookId), None)
    if not book:
        return error_response("/not-found", "Not Found", 404,
                              "The specified book could not be found.",
                              f"/books/{bookId}")
    return jsonify(book), 200

@app.route("/books/<uuid:bookId>", methods=["PUT"])
def replace_book(bookId):
    try:
        data = request.get_json(force=True)
    except Exception:
        return error_response("/bad-request", "Bad Request", 400, "Invalid request format.", f"/books/{bookId}")
    data_fields = data.keys()
    for k in data_fields:
        if k not in ["name", "author", "id"]:
          return error_response(
              type_='/unprocessable-content',
              title='Unprocessable Content',
              status= 422,
              detail="The request contain invalid information.",
              instance=f"/books/{bookId}"
          )
    book = books.get(str(bookId))
    if not book:
        return error_response("/not-found", "Not Found", 404,
                                  "The specified book could not be found.",
                                  f"/books/{bookId}")

    books[str(bookId)] = {
        "id": data["id"],
        "title": data["name"],
        "author": data["author"]
    }
    return jsonify(books[str(bookId)]), 200

@app.route("/books/<uuid:bookId>", methods=["PATCH"])
def update_book(bookId):
    try:
        data = request.get_json(force=True)
    except Exception:
        return error_response("/bad-request", "Bad Request", 400, "Invalid request format.", f"/books/{bookId}")

    book = books.get(str(bookId))
    if not book:
        return error_response("/not-found", "Not Found", 404,
                              "The specified book could not be found.",
                              f"/books/{bookId}")

    data_fields = data.keys()
    for k in data_fields:
        if k not in ["name", "author", "id"]:
          return error_response(
              type_='/unprocessable-content',
              title='Unprocessable Content',
              status= 422,
              detail="The request contain invalid information.",
              instance=f"/books/{bookId}"
          )
    books[str(bookId)] = book
    return jsonify(book), 200

@app.route("/books/<uuid:bookId>", methods=["DELETE"])
def delete_book(bookId):
    if not bookId or not isValidUUID(bookId):
        return error_response("/bad-request", "Bad Request", 400,
                              "Invalid request format.",
                              f"/books/{bookId}")
    book = books.pop(str(bookId), None)
    if not book:
        return error_response("/not-found", "Not Found", 404,
                              "The specified book could not be found.",
                              f"/books/{bookId}")
    return "", 204

@app.route("/openapi.json")
def openapi_spec():
    with open("bookmanagingLITE.yaml", "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    return jsonify(spec)

@app.route("/docs")
def docs():
    return """
    <!DOCTYPE html>
    <html>
    <head>
      <title>Book Managing API Docs</title>
      <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css" />
    </head>
    <body>
      <div id="swagger-ui"></div>
      <script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
      <script>
        const ui = SwaggerUIBundle({
          url: '/openapi.json',
          dom_id: '#swagger-ui'
        });
      </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
