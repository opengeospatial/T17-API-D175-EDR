import json
import requests
from pprint import pprint
from helpers import get_useful_links, get_api_name, get_collections, get_queryables, get_groups

from flask import Flask, render_template, request, url_for
app = Flask(__name__)

API_BASE_URL = 'https://aws4ogc17.webmapengine.com/edr/'

API_NAME = get_api_name(API_BASE_URL)
USEFUL_LINKS = get_useful_links(API_BASE_URL)
COLLECTIONS_IN_API = get_collections(API_BASE_URL)
# QUERYABLES_IN_API = get_queryables(API_BASE_URL)
DEFAULT_LIMIT = 20
DEFAULT_COLLECTION_ID = "" # I.e. "aerofacp_1m"
DEFAULT_BBOX = "" # I.e. "-0.489,51.28,0.236,51.686" # LONDON
DEFAULT_ELEMENT_ID = "" # I.e.  "CWFID.AEROFACP_1M.5212.5610.7AEB8DB2246327DC1F20020000" # HEATHROW
TILESERVER_URL = 'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
GROUPS = get_groups(API_BASE_URL)
DEFAULT_ZOOM = 12
DEFAULT_CENTER = [0,0]

@app.route('/')
def index():
    if not request.root_url:
        # this assumes that the 'index' view function handles the path '/'
        request.root_url = url_for('index', _external=True)
    return render_template(
        'index.html', 
        links=USEFUL_LINKS, 
        name=API_NAME,
        default_collection_id=DEFAULT_COLLECTION_ID,
        default_bbox=DEFAULT_BBOX,
        default_element_id=DEFAULT_ELEMENT_ID,
        tileserver=TILESERVER_URL,
        collections = COLLECTIONS_IN_API,
        # queryables = QUERYABLES_IN_API,
        groups = GROUPS,
        zoom=DEFAULT_ZOOM,
        center=DEFAULT_CENTER
    )

@app.route('/collections/<collectionId>/items/', defaults={
    'bbox': DEFAULT_BBOX,
    'collectionId': DEFAULT_COLLECTION_ID,
    'l': DEFAULT_LIMIT
})
def get_features(collectionId, l, bbox):
    if (request.args.get('l') == '' or request.args.get('l') == None):
        limitArg = l
    else:
        limitArg = request.args.get('l')

    if (request.args.get('collectionId') == '' or request.args.get('collectionId') == None):
        collectionIdArg = collectionId
    else:
        collectionIdArg = request.args.get('collectionId')

    # Get the collection ID
    collection_id = collectionIdArg
    # Set the API resource url
    URL = API_BASE_URL+"/collections/"+collection_id+"/items"
    f = "application/json" # str | A MIME type indicating the representation of the resources to be presented (e.g. application/gml+xml; version=3.2 for GML 3.2). (optional)
    limitParam = limitArg # int | The optional limit parameter limits the number of items that are presented in the response document.  Only items are counted that are on the first level of the collection in the response document. Nested objects contained within the explicitly requested items shall not be counted. (optional) (default to 10)
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        'f':f,
        'limit':limitParam,
    }

    # Accepted queryables:
    # bbox list[float] | Only features that have a geometry that intersects the bounding box are selected. The bounding box is provided as four or six numbers, depending on whether the coordinate reference system includes a vertical axis (elevation or depth): * Lower left corner, coordinate axis 1 * Lower left corner, coordinate axis 2 * Lower left corner, coordinate axis 3 (optional) * Upper right corner, coordinate axis 1 * Upper right corner, coordinate axis 2 * Upper right corner, coordinate axis 3 (optional) The coordinate reference system of the values is WGS84 longitude/latitude (http://www.opengis.net/def/crs/OGC/1.3/CRS84) unless a different coordinate reference system is specified in the parameter `bbox-crs`. For WGS84 longitude/latitude the values are in most cases the sequence of minimum longitude, minimum latitude, maximum longitude and maximum latitude. However, in cases where the box spans the antimeridian the first value (west-most box edge) is larger than the third value (east-most box edge). If a feature has multiple spatial geometry properties, it is the decision of the server whether only a single spatial geometry property is used to determine the extent or all relevant geometries. (optional)
    # property_name = 'property_name_example' # str | A list of feature properties to include in the response.  For some output formats, such as XML that can be validate against a formal schema, this list represents the optional properties to include in the response. (optional)
    # crs = 'http://www.opengis.net/def/crs/epsg/0/4326' # str | Asserts the CRS to use for encoding features in the response document. (optional)
    # lat = 3.4 # float | The latitude of the center point of a proximity search. (optional)
    # lon = 3.4 # float | The longitude of the center point of a proximity search. (optional)
    # radius = 3.4 # float | The search radius in meters of a proximity search. (optional)
    if (request.args.get('bbox') != '' and request.args.get('bbox') != None):
        PARAMS['bbox'] = request.args.get('bbox') 
    if (request.args.get('queryableName') != '' and request.args.get('queryableName') != None and request.args.get('queryableValue') != '' and request.args.get('queryableValue')):
        # PARAMS[request.args.get('queryableName')] = request.args.get('queryableValue')
        name = request.args.get('queryableName')
        value = request.args.get('queryableValue')
        PARAMS[name] = value

    # sending get request and saving the response as response object
    api_response = requests.get(url = URL, params = PARAMS)
    # extracting data in json format
    json_api_response = api_response.json()
    # Looking for exceptions
    if ('code' in json_api_response and json_api_response['code'] == "InvalidParameterValue"):
        return json.dumps(['error', json_api_response['description']])
    if ('code' in json_api_response and json_api_response['code'] == "NotFound"):
        return json.dumps(['error', json_api_response['description']])
    # Get features 
    json_fearures_list = json_api_response["features"]
    # Parsing to string
    features_list = json.dumps(json_fearures_list)
    # Returning string
    return features_list

@app.route('/collections/<collectionId>/items/<itemId>', defaults={
    'bbox': DEFAULT_BBOX,
    'collectionId': DEFAULT_COLLECTION_ID,
    'itemId': DEFAULT_ELEMENT_ID,
})
def get_feature(collectionId, itemId, bbox):
    if (request.args.get('itemId') == '' or request.args.get('itemId') == None):
        itemIdArg = itemId
    else:
        itemIdArg = request.args.get('itemId')

    if (request.args.get('collectionId') == '' or request.args.get('collectionId') == None):
        collectionIdArg = collectionId
    else:
        collectionIdArg = request.args.get('collectionId')

    # Get the collection ID
    collection_id = collectionIdArg
    # get the item ID
    item_id = itemIdArg
    # bbox = [3.4] # list[float] | Only features that have a geometry that intersects the bounding box are selected. The bounding box is provided as four or six numbers, depending on whether the coordinate reference system includes a vertical axis (elevation or depth): * Lower left corner, coordinate axis 1 * Lower left corner, coordinate axis 2 * Lower left corner, coordinate axis 3 (optional) * Upper right corner, coordinate axis 1 * Upper right corner, coordinate axis 2 * Upper right corner, coordinate axis 3 (optional) The coordinate reference system of the values is WGS84 longitude/latitude (http://www.opengis.net/def/crs/OGC/1.3/CRS84) unless a different coordinate reference system is specified in the parameter `bbox-crs`. For WGS84 longitude/latitude the values are in most cases the sequence of minimum longitude, minimum latitude, maximum longitude and maximum latitude. However, in cases where the box spans the antimeridian the first value (west-most box edge) is larger than the third value (east-most box edge). If a feature has multiple spatial geometry properties, it is the decision of the server whether only a single spatial geometry property is used to determine the extent or all relevant geometries. (optional)
    # Set the API resource url
    URL = API_BASE_URL+"/collections/"+collection_id+"/items/"+item_id
    f = "application/json" # str | A MIME type indicating the representation of the resources to be presented (e.g. application/gml+xml; version=3.2 for GML 3.2). (optional)
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {
        'f':f,
    }
    # Queriables
    if (request.args.get('bbox') != '' or request.args.get('bbox') != None):
        PARAMS['bbox'] = request.args.get('bbox') # list[float] | Only features that have a geometry that intersects the bounding box are selected. The bounding box is provided as four or six numbers, depending on whether the coordinate reference system includes a vertical axis (elevation or depth): * Lower left corner, coordinate axis 1 * Lower left corner, coordinate axis 2 * Lower left corner, coordinate axis 3 (optional) * Upper right corner, coordinate axis 1 * Upper right corner, coordinate axis 2 * Upper right corner, coordinate axis 3 (optional) The coordinate reference system of the values is WGS84 longitude/latitude (http://www.opengis.net/def/crs/OGC/1.3/CRS84) unless a different coordinate reference system is specified in the parameter `bbox-crs`. For WGS84 longitude/latitude the values are in most cases the sequence of minimum longitude, minimum latitude, maximum longitude and maximum latitude. However, in cases where the box spans the antimeridian the first value (west-most box edge) is larger than the third value (east-most box edge). If a feature has multiple spatial geometry properties, it is the decision of the server whether only a single spatial geometry property is used to determine the extent or all relevant geometries. (optional)
    
    # sending get request and saving the response as response object
    api_response = requests.get(url = URL, params = PARAMS)
    # extracting data in json format
    json_api_response = api_response.json()
    # Looking for exceptions
    if ('code' in json_api_response and json_api_response['code'] == "InvalidParameterValue"):
        return json.dumps(['error', json_api_response['description']])
    if ('code' in json_api_response and json_api_response['code'] == "NotFound"):
        return json.dumps(['error', json_api_response['description']])
    if ('code' in json_api_response and json_api_response['code'] == "error"):
        return json.dumps(['error', json_api_response['description']])
    # Parsing to string
    features_item = json.dumps(json_api_response)
    # Returning string
    return features_item


