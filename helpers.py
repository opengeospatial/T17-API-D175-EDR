import requests
from pprint import pprint

'''
    HELPERS
'''

def get_useful_links(landing_page):
    links = []

    try:
        api_response = requests.get(url = landing_page, params = {'f':'application/json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False
        
    for link in json_api_response["links"]:
        if (link["rel"] == "self" and link["type"] == "application/json"):
            links.append((link["href"], "Landing page"))
        
        if (link["rel"] == "service-desc" and link["type"] == "application/json"):
            links.append((link["href"], link["title"]))
        
        if (link["rel"] == "conformance" and link["type"] == "application/json"):
            links.append((link["href"], link["title"]))
        
        if (link["rel"] == "data" and link["type"] == "application/json"):
            links.append((link["href"], link["title"]))

    return links


def get_api_name(landing_page):
    try:
        api_response = requests.get(url = landing_page, params = {'f':'application/json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False

    return json_api_response["title"]


def get_collections(landing_page):
    collections = []
    url = landing_page+'/collections'

    try:
        api_response = requests.get(url = url, params = {'f':'application/json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False
        
    for collection in json_api_response["collections"]:
        element = dict(id=collection["id"], name=collection["title"])
        collections.append(element)
        

    return collections


def get_queryables(landing_page):
    queryables_selector = []
    collections = []
    url = landing_page+'/collections'

    # Get collections id
    try:
        api_response = requests.get(url = url, params = {'f':'application/json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False
        
    for collection in json_api_response["collections"]:
        collections.append(collection["id"])

    # Get queryables for each collection
    for collection in collections:
        try:
            url = landing_page+'/collections/'+collection+'/queryables'
            api_response = requests.get(url = url, params = {'f':'application/json'})
            json_api_response = api_response.json()
        except requests.ConnectionError as exception:
            return False
            
        group = []
        aux = []

        for queryable in json_api_response["properties"]:
            aux.append(queryable)

        group.append(aux)
        queryables_selector.append(
            dict(
                collection_id = collection, 
                queryables = group
            )
        )
        
    return queryables_selector

def get_groups(landing_page):
    groups = []
    url = landing_page+'/groups'

    try:
        api_response = requests.get(url = url, params = {'f':'application/json'})
        json_api_response = api_response.json()
    except requests.ConnectionError as exception:
        return False
        
    for member in json_api_response["members"]:
        element = dict(url=member["href"], name=member["title"])
        groups.append(element)
        

    return groups

