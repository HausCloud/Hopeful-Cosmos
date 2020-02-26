import basewish
import storage
import uuid
from flask import Flask, render_template, url_for, jsonify, request, abort
from flask_cors import CORS

# Create flask instance and apply CORS
app = Flask(__name__)
CORS(app)

# Disable strict slashes for all routes
app.url_map.strict_slashes = False

@app.route('/')
def main_page():
    """
    Serve main page
    """
    return render_template('example.html', cache_id=uuid.uuid4())


@app.route('/api/wish/all', methods=['GET'])
def all_wish():
    """
    GET route to return JSON of 50 wishes
    """
    my_dict = {}
    wish_list = storage.storage_instance.grab_all()
    for wish in wish_list:
        my_dict['{}'.format(wish.wish_id)] = wish.to_dict()
    return jsonify(my_dict)

@app.route('/api/wish/make', methods=['POST'])
def create_wish():
    """
    POST route to save a wish
    """
    req = request.json

    # Ensure request contains all necessary informtion to create a wish object
    if req is None:
        abort(400, 'Not JSON')
    elif type(req) is not dict:
        abort(400, 'Failed to convert to dict')
    elif 'name' not in req:
        abort(400, 'Incoming JSON object requires name attribute')
    elif 'state' not in req:
        abort(400, 'Incoming JSON object requires state attribute')
    elif 'country' not in req:
        abort(400, 'Incoming JSON object requires country attribute')
    elif 'star_name' not in req:
        abort(400, 'Incoming JSON object requires star_name attribute')
    elif 'wish' not in req:
        abort(400, 'Incoming JSON object requires wish attribute')
    else:
        wish_instance = basewish.Wish(req['name'], req['state'], req['country'], req['star_name'], req['wish'])
        if wish_instance.save() is False:
            abort(500, 'Whoops, Something happened with the code.')
    return jsonify(wish_instance.to_dict())


@app.teardown_appcontext
def teardown_db(exception):
    """
    A teardown function that is to be called after each request
    """
    storage.storage_instance.close()


@app.errorhandler(404)
def not_found_error(error):
    """
    404 gif page
    """
    return render_template('404.html', cache_id=uuid.uuid4())


@app.errorhandler(500)
def internal_error(error):
    """
    Broad 500 error code handler
    """
    abort(500, 'Whoops, something went wrong')


@app.errorhandler(502)
def bad_gateway(error):
    """
    Bad gateway error 
    """
    abort(502, 'Bad Gateway')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
