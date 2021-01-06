import os

class Config(object):
    PORTAL = os.environ['PORTAL']
#    SERVER = os.environ['SERVER']
    PORTAL_USER = os.environ['PORTAL_USER']
    PORTAL_PASSWORD = os.environ['PORTAL_PASSWORD']

    ACCELA_AGENCY = os.environ['ACCELA_AGENCY']
    ACCELA_USER = os.environ['ACCELA_USER']
    ACCELA_PASSWORD = os.environ['ACCELA_PASSWORD']

    ACCELA_APP_TYPE = os.environ['ACCELA_APP_TYPE']
    ACCELA_ID = os.environ['ACCELA_ID']
    ACCELA_SECRET = os.environ['ACCELA_SECRET']

    # Chose one, from get_environment_status
    #ACCELA_ENVIRONMENT = 'DEV'   # Fails when requesting token
    #ACCELA_ENVIRONMENT = 'TEST'  # Many API calls forbidden
    #ACCELA_ENVIRONMENT = 'STAGE'
    #ACCELA_ENVIRONMENT = 'CONFIG'
    ACCELA_ENVIRONMENT = 'PROD'  # Works mostly
    #ACCELA_ENVIRONMENT = 'SUPP'

if __name__ == "__main__":

    assert Config.PORTAL
#    assert Config.SERVER
    assert Config.PORTAL_USER
    assert Config.PORTAL_PASSWORD

    assert Config.ACCELA_AGENCY
    assert Config.ACCELA_USER
    assert Config.ACCELA_PASSWORD
    assert Config.ACCELA_APP_TYPE
    assert Config.ACCELA_ID
    assert Config.ACCELA_SECRET
    assert Config.ACCELA_ENVIRONMENT

    
