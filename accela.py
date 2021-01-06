import requests
import json
from config import Config

base_url = 'https://apis.accela.com/v4/'

def get_token(scope):
    auth_url = "https://auth.accela.com/oauth2/token"
    payload = {
        'client_id': Config.ACCELA_ID,
        'client_secret': Config.ACCELA_SECRET,
        'grant_type': 'password',
        'agency_name': Config.ACCELA_AGENCY,
        'username': Config.ACCELA_USER,
        'password': Config.ACCELA_PASSWORD,
        'environment': Config.ACCELA_ENVIRONMENT,
        'scope': ' '.join(scope)
    }
    response = requests.post(auth_url, data=payload)
    token = None
    try:
        assert response.status_code == 200
        content = json.loads(response.text)
        token = content['access_token']
    except Exception as e:
        print("POST error %s, \"%s\"" % (e, response.text))
        pass
    return token

def post_url(url, token=None, params={}):
    """
    url: partial url for service
    params: dict to pass as data
    token: passed in header
    """
    auth = {}
    if token: auth['Authorization'] = token
    jsonstring = json.dumps(params)
    response = requests.post(base_url + url, data=jsonstring, headers=auth)
    if response.status_code != 200:
        print("status %d : %s" % (response.status_code, url))
        print("POST failed, ", response.text)
        results = response.text
    else:
        try:
            results = json.loads(response.text)
            if 'result' in results:
                results = results['result']
        except Exception as e:
            print("status %d : %s" % (response.status_code, url))
            print("POST error %s, \"%s\"" % (e, response.text))
            results = response.content
    return results

def get_url(url, token, params={}):
    headers = {}
    if token : 
        headers['Authorization'] = token
    else:
        headers['x-accela-appid'] = Config.ACCELA_ID
        headers['x-accela-appsecret'] = Config.ACCELA_SECRET
        headers['x-accela-agency'] = Config.ACCELA_AGENCY
        headers['x-accela-environment'] = 'TEST'
        pass
    response = requests.get(base_url + url, params=params, headers=headers)

    if response.status_code != 200:
        print("status %d : %s" % (response.status_code, url))
        print(response.text)
        results = []
    else:
        try:
            results = json.loads(response.text)
            if 'result' in results:
                results = results['result']
        except Exception as e:
            results = response.content
    return results

# ==========================================================================

def get_addresses(token, options={}):
    results = get_url('addresses',  token, params=options)
    for item in results:
 #       print('name:', i['name'])
        try:
            print("id %s: %s %s %s" % (
                item['id'],
                item['streetStart'], 
                item['streetName'], 
                item['streetSuffix']['text']
            ))
        except Exception as e:
            print(json.dumps(item, indent=4, sort_keys=True))
    return

def get_agencies(token, options):
    # NOTE items say "no auth required" but fails without token
    results = get_url('agencies', token, params=options)
    for item in results:
        try:
            display = ''
            if 'display' in item:
                display = item['display']
            print("%s : %s" % (item['name'], display))
        except KeyError:
            print(item)
    return 

def search_agencies(token, options={}):
    # NOTE docs say "no auth required" but call fails without token
    results = post_url('search/agencies', token=token, params=options)
    print(results)
    return 

def get_announcements(token):
    # NOTE items say "no auth required" but fails without tokem
    url = 'announcements'
    options = {'fields': 'id,isRead,startEffectDate,text,title', 'isRead':'N'}
    results = get_url(url, token, params=options)
    print(results)
    return 

def get_app_settings():
    # Misc -- Get All App Settings
    # It fails with a token (as expected)
    #
    # "App Settings" are defined in My Apps at developer.accela.com
    #
    options = {
        'agency': Config.ACCELA_AGENCY,
        'appId': Config.ACCELA_ID,
        'appSecret': Config.ACCELA_SECRET,
    }
    results = get_url("appsettings", None, params=options)
    for item in results:
        try:
            print('%s = %s' % (item['key'], item['value']))
        except KeyError:
            print("get_app_settings() KeyError %s" % results)
    return results

def search_assessments(token):
    # Not sure whether limit goes in payload or as a REST parameter
    results = post_url('search/assessments', token=token, params={"limit":3})
    if len(results)>0:
        print(results)
    return

def get_assessments(token):
    results = get_url('assessments', token, params={'limit' : 3})
    if len(results)>0:
        print(results)
    return

def get_assets(token):
    results = get_url('assets', token, params={'limit' : 3})
    if len(results)>0:
        print(results)
    return

def get_approval_conditions(token):
    results = get_url('conditionsApprovals/standard', token, params={'limit' : 3})
    print(results)
    return

def get_standard_conditions(token):
    results = get_url('conditions/standard', token, params={'limit' : 10})
    for i in results:
        print('name:', i['name'])
        #print(json.dumps(i, indent=4, sort_keys=True))
    return

def search_contacts(token):
    results = post_url("search/contacts", token=token, params={"lastName":"Phillips"})
    print(results)
    return

def get_contacts(token):
    results = get_url('contacts', token, params={'limit' : 10})
    id_list = []
    for item in results:
        #print(json.dumps(item, indent=4, sort_keys=True))
        print(item['id'], item['firstName'], item['lastName'])
        id_list.append(item['id'])
    return id_list

def get_contact_addresses(token, id):
    options = {'limit' : 10, 'id': id}
    results = get_url('contacts/' + id + '/addresses', token, params=options)
    print(results)
    return

def get_contact_records(token, id):
    options = {'limit' : 10, 'id': id}
    results = get_url('contacts/' + id + '/records', token, params=options)
    for item in results:
        print(json.dumps(item, indent=4, sort_keys=True))
        #print(item['id'], item['firstName'], item['lastName'])
        #id_list.append(item['id'])
    return

def get_documents(token, id_list):
    ids = ','.join(id_list)
    options = {
        'documentIds': ids
    }
    results = get_url('documents/' + ids, token, params=options)
    for item in results:
        print(json.dumps(item, indent=4, sort_keys=True))
    return results

def download_document(token, filekey, filename):
    results = get_url("documents/" + filekey + "/download", token)
    with open(filename, 'wb') as fp:
        fp.write(results)
    return

def test_documents():
    """ First search for some documents, then download them. """
    items = search_all(token, {'type':'DOCUMENT','limit':3})
    for item in items:
        if item != 'status':
            print(json.dumps(item, indent=4, sort_keys=True))
            id = str(item['id'])
        filename = item['fileName']
        items = get_documents(token, [id])
        print("Downloading %s, id=%s" % (filename, id))
        download_document(token, id, filename)
    return


def get_environment_status(token):
    results = get_url("agencies/" + Config.ACCELA_AGENCY + "/environments", token)
    print(json.dumps(results, indent=4, sort_keys=True))
    return results

def reverse_geocode(token, lon, lat):
    options = { 'longitude': lon, 'latitude': lat }
    results = get_url('geo/geocode/reverse', token, params=options)
    try:    
        print(results['address']['addressFormat'])
    except Exception as e:
        print('Reverse geocode failed.', e)
    return

def get_inspections(token):
    results = get_url('inspections', token, params={'limit' : 3})
    for item in results:
        print(json.dumps(item, indent=4, sort_keys=True))
    return results

def get_related_inspections(token, id):
    options = {
        "limit": 3,
        "inspectionId": id
    }
    results = get_url('inspections/' + id + '/related', token, params=options)
    for item in results:
        print(json.dumps(item, indent=4, sort_keys=True))
    return results

def get_inspection_documents(token, id):
    options = {
        "limit": 3,
        "inspectionId": id
    }
    results = get_url('inspections/' + id + '/documents', token, params=options)
    for item in results:
        print(json.dumps(item, indent=4, sort_keys=True))
    return results

def get_inspectors(token):
    # Filtering on department fails... 
    results = get_url('inspectors', token, params={"department":"Building"})
    if type(results) == type([]):
        for item in results:
            #print(json.dumps(item, indent=4, sort_keys=True))
            print(item["firstName"], item["lastName"], '--', item["department"]["text"])
    else:
        print(results)
    return

def get_owners(token, options={}):
    results = get_url('owners', token, params=options)
    if type(results) == type([]):
        for item in results:
            try:
                print("%s: %s" % (item["fullName"],item["mailAddress"]))
            except KeyError:
                print(json.dumps(item, indent=4, sort_keys=True))
                pass
    else:
        print(results)
    return results

def get_parcel(token, id, options={}):
    item = get_url('parcels/' + id, token, params=options)
    try:
        print("id %s: parcel: %s" % (
            item['id'],
            item['parcelNumber'] 
        ))
    except Exception as e:
        print(json.dumps(item, indent=4, sort_keys=True))
    return

def get_parcels(token, options={}):
    results = get_url('parcels', token, params=options)
    if type(results) == type([]):
        for item in results:
    #       print('name:', item['name'])
            try:
                print("id %s: parcel: %s" % (
                    item['id'],
                    item['parcelNumber'] 
                ))
            except Exception as e:
                print(json.dumps(item, indent=4, sort_keys=True))
    else:
        print(results)
    return

def search_parcels(token, options={}):
    results = post_url("search/parcels", token=token, params=options)
    if type(results) == type([]):
        for item in results:
            print(item)
    else:
        print(results)
    return results

def get_professionals(token):
    options = {'limit' : 5}
    results = get_url('professionals', token, params=options)
    for item in results:
        #print(json.dumps(item, indent=4, sort_keys=True))
        print(item["businessName"], ' --', item["city"])
    return

def get_records(token, options={}):
    return get_url('records', token, params={'limit':5})

def search_records(token, options={}):
    results = post_url('search/records', token, params=options)
    for item in results:
        print(json.dumps(item, indent=4, sort_keys=True))
        #print(item["businessName"], ' --', item["city"])
    return results

def search_all(token, params={}):
    """ Type can be one of RECORD ADDRESS LICENSEDPROFESSIONAL ASSET CONTACT PARCEL DOCUMENT 
    """
    if not 'type' in params:
        raise AttributeError("'type' not defined in params")
    return get_url("search/global", token, params=params)

# ====================================================================

if __name__ == "__main__":

    token = None # 'citizen' apps use the app credentials in the header.
    if Config.ACCELA_APP_TYPE == 'agency':
        scope = [
            "addresses", "agencies", "announcements", "app_data", "assessments", "get_assets",
            "conditions", "contacts", "documents",
            "global_search", "inspections", "owners", 
            "parcels", "professionals", "records"
        ]
        token = get_token(scope)
    if not token: print('no token available')
 
    results = search_records(token, options={'parcelNumber': '51032BC01400'})

    # So far I have not found TRS settings that return anything.
    get_parcels(token, options={'parcelNumber': '51032BC01400'})

    search_parcels(token, options={'parcelNumber': '51032BC01400'})
    search_parcels(token, options={'township': 'T8N', 'range': 'R9W'})
    search_parcels(token, options={'township': '8N', 'range': '9W'})
    search_parcels(token, options={'township': '8N', 'range': '9W', 'section': 18})

    get_environment_status(token)

    # Does not return an error, but does not find any results, either.
    items = search_all(token, {'type':'ADDRESS', 'query':'streetName=5TH', 'limit':13}) # Type is required, no matter what the docs say
    print(items)

    get_addresses(token, options={'city':'Astoria', 'streetName':'5th'})
    get_addresses(token, options={'id':2643})

    get_agencies(token, {'name': Config.ACCELA_AGENCY})
    #get_agencies(token, {'limit': 5}) # Seems to ignore the limit and jam up.
    # 500 error but I don't really care, do you?
    search_agencies(token, options={'latitude':46.18805,'longitude':-123.83426,'state':'OR'}) # 800 Exchange

    get_announcements(token) # 200
    get_app_settings()

# maybe we don't have assessments at all in Accela
    #search_assessments(token) # 403 Forbidden
    #get_assessments(token) # 403 Forbidden
    #get_assets(token) # 403 forbidden

    # batch_request ---- not interested in using this call
    # citizen_access ---- don't know what this is

    get_approval_conditions(token) # 404 not defined in API 
    get_standard_conditions(token)
    search_contacts(token)
    id_list = get_contacts(token)
    for id in id_list:
        get_contact_addresses(token, id=id) # always returns 200, which just means no address on record
        get_contact_records(token, id=id) # WORKS
        pass

    reverse_geocode(token, 0, 0) # Should fail 
    reverse_geocode(token, -123.8155, 46.1979)    # Shows as Astoria Oregon
    reverse_geocode(token, -123.83426, 46.18805)  # Should be 800 Exchange
    reverse_geocode(token, -123.8380, 46.1744)    # Should be 1830 5th St

    #test_documents() # WORKS! commented out because downloads take time

    get_inspectors(token) # WORKS

    inspections = get_inspections(token) # WORKS
    for item in inspections:
        id = str(item['id'])
        get_related_inspections(token, id) # 403 Forbidden
        get_inspection_documents(token, id)
    # There are about 10 more inspections calls...
    
    get_owners(token, options={'limit': 20, 'city':'Astoria', 'lastName': 'Wilson'})
    get_parcels(token, options={'limit': 10, 'city':'Astoria', 'streetName': '5th'})

    search_parcels(token, options={'limit': 10, 'address': {'city':'Astoria', 'streetName': '5th'}})

    get_professionals(token) # 403 forbidden

    payload = {
        'limit': 50,
        'address': {
            'city': 'Astoria',
            'streetName': '5th'
        }
    }
    search_parcels(token, options=payload)

    results = get_records(token, options={'limit':5})
    for item in results:
        recordId = item['id']
        typeId = item['type']['id']

        print('record %s  type %s' % (recordId, typeId))
#        print(json.dumps(item, indent=4, sort_keys=True))

        # get_all_parcels for this record.
        parcels = get_url('records/' + recordId + '/parcels', token)
        for parcel in parcels:
            if parcel != 'status':
                print(json.dumps(parcel, indent=4, sort_keys=True))
                parcelId = parcel['id']

                get_owners(token, options={
                    'parcelId': parcelId })

                get_parcel(token, parcelId)

        # get_all_documents for this record.
        documents = get_url('records/' + recordId + '/documents', token)
        for item in documents:
            if item != 'status':
                print(json.dumps(item, indent=4, sort_keys=True))

    print("That's all!")