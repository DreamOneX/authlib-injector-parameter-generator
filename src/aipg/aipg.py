import requests, json, base64
__all__ = ["SkinWebsite", "Account"]

class LoginError(Exception):
    '''
    password wrong
    username not found
    etc
    '''
    def __init__(self, message: str = 'Your username or password is invalid') -> None:
        super().__init__(message)
        self.message = message

class SkinWebsite():
    '''
    A yggdrasil api site like Blessing Skin
    '''
    def __init__(self, api_base: str) -> None:
        '''
        api_base Yggdrasil Api URL like
                 https://example.tld/api/yggdrasil
        '''
        self.api_base = api_base

    def get_metadata(self) -> str:
        '''
        get metadata of this yggdrasil api
        should specified in -Dauthlibinjector.yggdrasil.prefetched
        '''
        return base64.b64encode(requests.get(self.api_base).text.encode('ascii')).decode('ascii')

class Account():
    '''
    An yggdrasil account
    '''
    def __init__(self, website: SkinWebsite, **kwargs) -> None:
        '''
        website website object
        username email or id
        password ¿dont you know
        '''
        self.website = website
        if kwargs.get('username') != None: self.__username = str(kwargs.get('username'))
        else: self.__username = None
        if kwargs.get('password') != None: self.__password = str(kwargs.get('password'))
        else: self.__password = None
        self.__header = {'Content-Type': 'application/json'}

    def __build_data(self, username: str, password: str) -> str:
        return json.dumps({'username': username, 'password': password, 'requestUser': False, 'agent': {'name': 'Minecraft', 'version': 1}})

    def __check_info(self) -> bool:
        if (self.__username == None or self.__password == None):
            raise LoginError("No email or password provided")
        if ((not isinstance(self.__username, str)) or (not isinstance(self.__password, str))):
            raise LoginError("Email or password is not a instance of str")
        return True

    def login(self, **kwargs) -> bool:
        '''
        username email or id
        if you provide at instantiation, no need provide again
        '''
        if kwargs.get('username') != None: self.__username = str(kwargs.get('username'))
        if kwargs.get('password') != None: self.__password = str(kwargs.get('password'))
        self.__check_info()
        response = requests.post(\
                self.website.api_base + "/authserver/authenticate", \
                headers=self.__header, \
                data=self.__build_data(\
                    self.__username, \
                    self.__password\
                ) \
            )
        body = json.loads(response.text)
        if response.status_code != 200:
            raise LoginError
        self.access_token = body['accessToken']
        self.client_token = body['clientToken']
        return True
