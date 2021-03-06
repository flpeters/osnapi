# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['Settings', 'retry_on', 'login', 'getSensors', 'getSensor', 'addSensor', 'deleteSensor', 'mySensors',
           'mySensorIds', 'getFirstLastValueForSensor', 'getValues', 'getValuesForSensor', 'addValue',
           'addMultipleValues', 'profile', 'getMeasurands', 'getMeasurand', 'getLicenses', 'getLicense', 'getUnits',
           'getUnit']

# Cell
import requests

# Internal Cell
from typing import List, Tuple, Dict, Union, Optional, Callable
Sensor                   = Dict[str, Union[int, str, Dict[str, float]]]
SensorWithValue          = Dict[str, Union[int, str, Dict[str, float], Dict[str, Union[str, float]]]]
Value = Measurand = Unit = Dict[str, Union[str, float]]
License                  = Dict[str, Union[int, str, bool]]

# Cell
class Settings():
    api_endpoint = 'https://www.opensense.network/beta/api/v1.0/'
    username     = None
    password     = None
    auth_token   = None

    def __repr__(self):
        return f'api_endpoint:\t{self.api_endpoint}\nusername:\t{self.username}\npassword:\t{self.password}\nauth_token:\t{self.auth_token}'

# Cell
#######################################
#               HELPERS               #
#######################################

# Cell
def retry_on(EX:Exception, retries:int=1, on_failure:Callable=None): # TODO(florian): test that on_failure returns a boolean?
    """Decorator that retries the decorated function n (retries) times,
       calling on_failure each time it fails with a given Exception EX.
       EX can be one, or a tuple of Exception/s that should be caught.
       on_failure takes the Exception that caused the failure,
       and returns a boolean saying whether or not to try again."""
    assert retries >= 0, 'can\'t have negative retries'
    if on_failure is None: on_failure = lambda e: True
    def _retry_on(func):
        def _wrapper(*args, **kwargs):
            retry, _tries, _e = True, retries + 1, Exception('Something went wrong in retry_on()')
            while (retry and (_tries > 0)):
                retry, _tries = False, _tries - 1
                try: return func(*args, **kwargs)
                except EX as e: _e, retry = e, on_failure(e) # TODO(florian): also pass the repeat count / args / kwargs?
            else: raise _e
        return _wrapper
    return _retry_on

# Internal Cell
def generate_headers(requires_auth:bool) -> Dict:
    """ Return Headers to be used in HTTP requests.
        If requires_auth, the headers will contain a login token,
        but only if a token was previously generated by calling login().
    """
    headers = {'accept'         : 'application/json',
               'accept-encoding': 'gzip, deflate',
               'content-type'   : 'application/json',
               'cache-control'  : 'no-cache'}
    if requires_auth:
        headers['Authorization'] = Settings.auth_token
    return headers

# Internal Cell
def handle_response(query:str, response:requests.Response) -> Union[Dict, str]:
    """ If the HTTPS Status Code is 200, the json response will be returned as a dictionary.
        Otherwise an Exception with some information about the query is raised.
        If for some reason a conversion to json is not possible, uses the raw text representation.
    """
    try:    text = response.json()
    except: text = response.text
    if response.status_code == 200: return text

    info = f'\n--Status Code   : {response.status_code}\n--Request to    : {query}\n--Response Body : {text}'

    if response.status_code == 500 or response.status_code == 401:
        raise PermissionError(f'The Server has refused this request, due to you attempting something that requires authorization.\
        Try logging in and repeating the Request.{info}')

    if response.status_code == 408:
        raise Exception(f'The Server has closed this connection, probably due to the request being too large,\
        or the server being under heavy load. Try sending less data at once.{info}')

    raise Exception(f'Something went wrong with your request.{info}')

# Internal Cell
def _try_login(_):
    """Callback that attempts to re-authenticate by using stored Settings"""
    if Settings.username and Settings.password:
        try: login(Settings.username, Settings.password)
        except: return False
        else: return True
    else: return False

@retry_on(PermissionError, retries=1, on_failure=_try_login)
def send_get(query:str, requires_auth:bool=False) -> Dict:
    """ Sends an HTTP GET request using query as URL.
    """
    headers = generate_headers(requires_auth)
    response = requests.get(url=query,headers=headers)
    return handle_response(query, response)

@retry_on(PermissionError, retries=1, on_failure=_try_login)
def send_post(query:str, body:Dict, requires_auth:bool=False) -> Dict:
    """ Sends an HTTP POST request using query as URL and body as json content.
    """
    headers = generate_headers(requires_auth)
    response = requests.post(url=query, json=body, headers=headers)
    return handle_response(query, response)

@retry_on(PermissionError, retries=1, on_failure=_try_login)
def send_delete(query:str, requires_auth:bool=False) -> Dict:
    """ Sends an HTTP DELETE request using query as URL.
    """
    headers = generate_headers(requires_auth)
    response = requests.delete(url=query, headers=headers)
    return handle_response(query, response)

# Internal Cell
def build_query(target:str, **kwargs):
    """ Create an API query by combining all keyword arguments into one request URL.
        target is what comes after the api_endpoint but before the query arguments
        e.g. /units or /users/profile
    """
    query = f'{Settings.api_endpoint}{"" if target.startswith("/") else "/" }{target}?'
    for key, value in kwargs.items():
        if value and key != 'self': query += f'{key}={value}&'
    return query

# Cell
def login(username:str, password:str) -> str:
    """ HTTP: POST

        Input:
            - username: your opensense.network username
            - password: your opensense.network username

        Output:
             - A login Token that can be used for 1 hour.
        Note: The Token is automatically added to the Settings and used whenever one is needed.
        Note: username and password are also stored in the Settings.
        Example:
            {'id': '...'}
    """
    query = build_query(target='/users/login')
    body = {'username': username, 'password': password}
    token = send_post(query, body)['id']
    Settings.username, Settings.password = username, password
    Settings.auth_token = token
    return token

# Cell
#######################################
#              SENSORS                #
#######################################

# Cell
def getSensors(measurandId:int=None,
               refPoint:List[float]=None,
               maxDistance:float=None,
               numNearest:int=None,
               boundingBox:List[float]=None,
               boundingPolygon:List[float]=None,
               minAccuracy:int=None,
               maxAccuracy:int=None,
               maxSensors:int=None,
               allowsDerivatives:bool=None,
               allowsRedistribution:bool=None,
               requiresAttribution:bool=None,
               requiresChangeNote:bool=None,
               requiresShareAlike:bool=None,
               requiresKeepOpen:bool=None) -> List[Sensor]:
    """ HTTP: GET

        Input:
        Note: All parameters are optional.
        Note: maxDistance is in meters

        Output:
            - A List of Sensors
        Note: This function can return A LOT OF DATA,
              if you're not limiting the search by using the parameters.
        Note: The output is a List even if only a single item is returned.
        Note: An empty List if returned if no matching Sensor was found.
        Example:
            [
                {
                    'id': 14,
                    'userId': 1,
                    'measurandId': 1,
                    'unitId': 1,
                    'location': {'lat': 50.5605, 'lng': 9.6711},
                    'altitudeAboveGround': 2.0,
                    'directionVertical': 0,
                    'directionHorizontal': 0,
                    'sensorModel': 'DWD station',
                    'accuracy': 10,
                    'attributionText': 'Deutscher Wetterdienst (DWD)',
                    'attributionURL': 'ftp://ftp-cdc.dwd.de/pub/CDC/',
                    'licenseId': 4
                },
                {
                    'id': 13,
                    'userId': 1,
                    'measurandId': 1,
                    'unitId': 1,
                    'location': {'lat': 50.5668, 'lng': 9.6533},
                    'altitudeAboveGround': 2.0,
                    'directionVertical': 0,
                    'directionHorizontal': 0,
                    'sensorModel': 'DWD station',
                    'accuracy': 10,
                    'attributionText': 'Deutscher Wetterdienst (DWD)',
                    'attributionURL': 'ftp://ftp-cdc.dwd.de/pub/CDC/',
                    'licenseId': 4
                },
            ]
    """
    args = locals()
    query = build_query(target='/sensors', **args)
    return send_get(query)

# Cell
def getSensor(id:int) -> Sensor:
    """ HTTP: GET

        Input:
            - The id of the Sensor you want.

        Output:
            - The Sensor with the id you specified.
        Note: Throws an Exception() if no Sensor with that id is found.
        Example:
            {
                'id': 61,
                'userId': 2,
                'measurandId': 1,
                'unitId': 1,
                'location': {'lat': 1.0, 'lng': 1.0},
                'altitudeAboveGround': 0.0,
                'directionVertical': 0,
                'directionHorizontal': 0,
                'sensorModel': 'DWD station',
                'accuracy': 0,
                'attributionText': 'test_string',
                'attributionURL': 'test_url',
                'licenseId': 1
            }
    """
    query = build_query(target=f'/sensors/{id}')
    return send_get(query)

# Cell
def addSensor(body:Sensor) -> Sensor:
    """ HTTP: POST
        Note: This function requires previous authentication.

        Input:
            - A Dictionary describing a Sensor you want to add.
        Example:
            {
                'measurandId': 1,
                'unitId': 1,
                'location': {'lat': 1.0, 'lng': 1.0},
                'altitudeAboveGround': 0.0,
                'directionVertical': 0,
                'directionHorizontal': 0,
                'sensorModel': 'test_string',
                'accuracy': 10,
                'attributionText': 'Deutscher Wetterdienst (DWD)',
                'attributionURL': 'ftp://ftp-cdc.dwd.de/pub/CDC/',
                'licenseId': 1
            }

        Output:
            - The newly created Sensor, including its assigned id.
        Example:
            {
                'id' : 66,
                'userId': 2,
                'measurandId': 1,
                'unitId': 1,
                'location': {'lat': 1.0, 'lng': 1.0},
                'altitudeAboveGround': 0.0,
                'directionVertical': 0,
                'directionHorizontal': 0,
                'sensorModel': 'test_string',
                'accuracy': 10,
                'attributionText': 'Deutscher Wetterdienst (DWD)',
                'attributionURL': 'ftp://ftp-cdc.dwd.de/pub/CDC/',
                'licenseId': 1
            }
    """
    query = build_query(target='/sensors/addSensor')
    return send_post(query, body, requires_auth=True)

# Cell
def deleteSensor(id:int) -> str:
    """ HTTP: DELETE
        Note: This function requires previous authentication.

        Input:
            - The id of the Sensor you want to delete.
        Note: You can only delete Sensors you own (the ones you created).

        Output:
            - The string 'OK' if deletion was successful, weird status codes otherwise.
        Note: weird status codes cause an Exception() to be thrown.
    """
    query = build_query(target=f'/sensors/{id}')
    return send_delete(query, requires_auth=True)

# Cell
def mySensors() -> List[Sensor]:
    """ HTTP: GET
        Note: This function requires previous authentication.

        Output:
            - A List of the Sensors you've created / own.
        Note: Returns a List, even if you've only created one Sensor so far.
        Example:
            [
                {
                    'id': 61,
                    'userId': 2,
                    'measurandId': 1,
                    'unitId': 1,
                    'location': {'lat': 1.0, 'lng': 1.0},
                    'altitudeAboveGround': 0.0,
                    'directionVertical': 0,
                    'directionHorizontal': 0,
                    'sensorModel': 'test_string',
                    'accuracy': 0,
                    'attributionText': 'test_string',
                    'attributionURL': 'test_url',
                    'licenseId': 1
                  },
            ]
    """
    query = build_query(target='/sensors/mysensors')
    return send_get(query, requires_auth=True)

# Cell
def mySensorIds() -> List[int]:
    """ HTTP: GET
        Note: This function requires previous authentication.

        Output:
            - A List of ids of Sensors you've created / own.
        Example:
            [61, 62, 63]
    """
    query = build_query(target='/sensors/mysensorids')
    return send_get(query, requires_auth=True)

# Cell
#######################################
#                VALUES               #
#######################################

# Cell
def getFirstLastValueForSensor(id:int,
                               first:bool,
                               last:bool) -> SensorWithValue:
    """ HTTP: GET

        Input:
            - id: The id of the Sensor you want to get values from
            - first: whether or not to get its first value
            - last:  whether or not to get its last value
        Note: At least one of either first or last must be True, or both.

        Output:
            - A Sensor, with its first and / or the last value included in the 'values' attribute.
        Example:
            {
                'id': 123,
                'userId': 2,
                'measurandId': 1,
                'unitId': 1,
                'location': {'lat': 50.5605, 'lng': 9.6711},
                'altitudeAboveGround': 2.0,
                'directionVertical': 0,
                'directionHorizontal': 0,
                'sensorModel': 'DWD station',
                'accuracy': 10,
                'attributionText': 'Deutscher Wetterdienst (DWD)',
                'attributionURL': 'ftp://ftp-cdc.dwd.de/pub/CDC/',
                'licenseId': 4,
                'values': [{'timestamp': '1999-11-23T00:00:00.000Z', 'numberValue': 1.0},
                           {'timestamp': '2019-11-23T22:22:22.222Z', 'numberValue': 3.0}]
            }
    """
    if first and last:
        query = build_query(target=f'/sensors/{id}/values/firstlast')
    elif first:
        query = build_query(target=f'/sensors/{id}/values/first')
    elif last:
        query = build_query(target=f'/sensors/{id}/values/last')
    else:
        raise Exception(f'At least one of the options has to be true:\
        \nfirst: {first}\nlast: {last}')
    return send_get(query)

# Cell
def getValues(measurandId:int=None,
              refPoint:List[float]=None,
              maxDistance:float=None,
              boundingBox:List[float]=None,
              boundingPolygon:List[float]=None,
              maxSensors:int=None,
              minTimestamp:str=None,
              maxTimestamp:str=None,
              aggregationType:str=None,
              aggregationRange:str=None,
              minValue:float=None,
              maxValue:float=None,
              allowsDerivatives:bool=None,
              allowsRedistribution:bool=None,
              requiresAttribution:bool=None,
              requiresChangeNote:bool=None,
              requiresShareAlike:bool=None,
              requiresKeepOpen:bool=None) -> List[SensorWithValue]:
    """ HTTP: GET

        Input:
        Note: All parameters are optional.

        Output:
            - A List of Sensors, each including its matching values in the 'values' attribute.
        Example:
            [
                {
                    'id': 123,
                    'userId': 2,
                    'measurandId': 1,
                    'unitId': 1,
                    'location': {'lat': 50.5605, 'lng': 9.6711},
                    'altitudeAboveGround': 2.0,
                    'directionVertical': 0,
                    'directionHorizontal': 0,
                    'sensorModel': 'DWD station',
                    'accuracy': 10,
                    'attributionText': 'Deutscher Wetterdienst (DWD)',
                    'attributionURL': 'ftp://ftp-cdc.dwd.de/pub/CDC/',
                    'licenseId': 4,
                    'values': [{'timestamp': '2019-11-23T01:23:45.678Z', 'numberValue': 1.0},
                               {'timestamp': '2019-11-23T11:23:45.678Z', 'numberValue': 2.0},
                               {'timestamp': '2019-11-23T21:23:45.678Z', 'numberValue': 3.0}]
                },
            ]
    """
    args = locals()
    query = build_query(target='/values', **args)
    return send_get(query)

# Cell
def getValuesForSensor(id:int,
                       minTimestamp:str=None,
                       maxTimestamp:str=None,
                       aggregationType:str=None,
                       aggregationRange:str=None,
                       minValue:float=None,
                       maxValue:float=None) -> SensorWithValue:
    """ HTTP: GET

        Input:
        Note: All values except for id are optional.

        Output:
            - A Sensor, including all its values stored in the 'values' attribute.
        Example:
            {
                'id': 123,
                'userId': 2,
                'measurandId': 1,
                'unitId': 1,
                'location': {'lat': 50.5605, 'lng': 9.6711},
                'altitudeAboveGround': 2.0,
                'directionVertical': 0,
                'directionHorizontal': 0,
                'sensorModel': 'DWD station',
                'accuracy': 10,
                'attributionText': 'Deutscher Wetterdienst (DWD)',
                'attributionURL': 'ftp://ftp-cdc.dwd.de/pub/CDC/',
                'licenseId': 4,
                'values': [{'timestamp': '2019-11-23T01:23:45.678Z', 'numberValue': 1.0},
                           {'timestamp': '2019-11-23T11:23:45.678Z', 'numberValue': 2.0},
                           {'timestamp': '2019-11-23T21:23:45.678Z', 'numberValue': 3.0}]
            }
    """
    args = locals()
    query = build_query(target=f'/sensors/{args.pop("id")}/values', **args)
    return send_get(query)

# Cell
def addValue(body:Value) -> str:
    """ HTTP: POST
        Note: This function requires previous authentication.

        Input:
            - A Value, including the sensorId that it should be added to.
        Note: You can only add values to sensors you've created / own.
        Example:
            {
                "sensorId": 61,
                "timestamp": "2019-11-23T01:23:45.678Z",
                "numberValue": 1.0
            }

        Output:
            - The string 'OK' if operation was successful, weird status codes otherwise.
        Note: weird status codes cause an Exception() to be thrown.
    """
    query = build_query(target='/sensors/addValue')
    return send_post(query, body, requires_auth=True)

# Cell
def addMultipleValues(body:Dict[str, List[Value]]) -> str:
    """ HTTP: POST
        Note: This function requires previous authentication.

        Input:
            - A Dict that has the key collapsedMessages, with a list of values,
              including the sensorId that each should be added to, as value.
        Note: You can only add values to sensors you've created / own.
        Example:
            {"collapsedMessages":
                [
                    {
                        "sensorId": 14,
                        "timestamp": "2019-11-23T11:11:11.111Z",
                        "numberValue": 2.0
                    },
                    {
                        "sensorId": 66,
                        "timestamp": "2019-11-23T22:22:22.222Z",
                        "numberValue": 3.0
                    }
                ]
            }

        Output:
            - The string 'OK' if operation was successful, weird status codes otherwise.
        Note: weird status codes cause an Exception() to be thrown.
    """
    query = build_query(target='/sensors/addMultipleValues')
    return send_post(query, body, requires_auth=True)

# Cell
#######################################
#                USERS                #
#######################################

# Cell
def profile() -> List[Dict[str, Union[str, int]]]:
    """ HTTP: GET
        Note: This function requires previous authentication.

        Output:
            - Profile information for the user who is currently logged in.
        Example:
            [{'username': 'yourname', 'id': 123}]
    """
    query = build_query(target='/users/profile')
    return send_get(query, requires_auth=True)

# Cell
#######################################
#              MEASURANDS             #
#######################################

# Cell
def getMeasurands(name:str=None) -> List[Measurand]:
    """ HTTP: GET

        Input:
            - The name of a specific Measurant e.g. 'temperature'.
        Note: This parameter is optional

        Output:
            - A List of (all) Measurands.
        Note: The output is a List even if a name was specified,
              and only a single item is returned.
        Note: An empty List if returned if no matching Measurand was found.
        Example:
            [
                {'id': 1, 'name': 'temperature', 'defaultUnitId': 1},
            ]
    """
    args = locals()
    query = build_query(target='/measurands', **args)
    return send_get(query)

# Cell
def getMeasurand(id:int) -> Measurand:
    """ HTTP: GET

        Input:
            - id of the Measurand you're interested in.

        Output:
            - The matching Measurand
        Note: If no Measurand with that id exists, a 404 status code is returned,
              which causes an Exception() to be thrown.
        Example:
            {'id': 1, 'name': 'temperature', 'defaultUnitId': 1}
    """
    query = build_query(target=f'/measurands/{id}')
    return send_get(query)

# Cell
#######################################
#               LICENSES              #
#######################################

# Cell
def getLicenses(shortName:str=None,
                allowsDerivatives:bool=None,
                allowsRedistribution:bool=None,
                requiresAttribution:bool=None,
                requiresChangeNote:bool=None,
                requiresShareAlike:bool=None,
                requiresKeepOpen:bool=None) -> List[License]:
    """ HTTP: GET

        Input:
        Note: All parameters are optional.

        Output:
            - A List of Licenses matching the given criteria
        Note: The output is a List even if only a single item is returned.
        Note: An empty List if returned if no matching License was found.
        Example:
            [
                {
                    'id': 2,
                    'shortName': 'ODC-BY-1.0',
                    'fullName': 'Open Data Commons Attribution License',
                    'version': 1,
                    'referenceLink': 'https://opendatacommons.org/licenses/by/1.0/',
                    'description': '...',
                    'allowsRedistribution': True,
                    'allowsDerivatives': True,
                    'requiresAttribution': True,
                    'requiresShareAlike': False,
                    'requiresKeepOpen': False,
                    'requiresChangeNote': False
                  },
            ]
    """
    args = locals()
    query = build_query(target='/licenses', **args)
    return send_get(query)

# Cell
def getLicense(id:int) -> License:
    """ HTTP: GET

        Input:
            - id of the License you're interested in.

        Output:
            - The matching License
        Note: If no License with that id exists, a 404 status code is returned,
              which causes an Exception() to be thrown.
        Example:
            {
                'id': 1,
                'shortName': 'ODC-PDDL-1.0',
                'fullName': 'Open Data Commons Public Domain Dedication and License',
                'version': 1,
                'referenceLink': 'https://opendatacommons.org/licenses/pddl/1.0/',
                'description': '...',
                'allowsRedistribution': True,
                'allowsDerivatives': True,
                'requiresAttribution': False,
                'requiresShareAlike': False,
                'requiresKeepOpen': False,
                'requiresChangeNote': False
            }
    """
    query = build_query(target=f'/licenses/{id}')
    return send_get(query)

# Cell
#######################################
#                UNITS                #
#######################################

# Cell
def getUnits(name:str=None,
             measurandId:int=None) -> List[Unit]:
    """ HTTP: GET

        Input:
        Note: All parameters are optional.

        Output:
            - A List of Units matching the given criteria
        Note: The output is a List even if only a single item is returned.
        Note: An empty List if returned if no matching Unit was found.
        Example:
            [
                {
                    "id": 1,
                    "name": "celsius",
                    "measurandId": 1
                },
                {
                    "id": 2,
                    "name": "fahrenheit",
                    "measurandId": 1
                }
            ]
    """
    args = locals()
    query = build_query(target='/units', **args)
    return send_get(query)

# Cell
def getUnit(id:int) -> Unit:
    """ HTTP: GET

        Input:
            - id of the Unit you're interested in.

        Output:
            - The matching Unit
        Note: If no Unit with that id exists, a 404 status code is returned,
              which causes an Exception() to be thrown.
        Example:
            {
                "id": 1,
                "name": "celsius",
                "measurandId": 1
            }
    """
    query = build_query(target=f'/units/{id}')
    return send_get(query)