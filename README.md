# OpenSense API
> The Unofficial opensense.network API  

[official documentation](https://opensense.infra.ise-apps.de/)

# NOTICE:
> It seems like this service has been discontinued, or at least is no longer being maintained. The web address has changed since the time when this unofficial project was developed, and the api documentation can't be reached as far as I can tell.  
> Maybe it will be revived some time in the future, but for now I'll just leave this project here for reference.

## What is OpenSense?

OpenSense is "A participatory open sensor data platform", making a uniform data format for a variety of open source weather data sources available to the public.  
For more information, visit [the website](https://opensense.infra.ise-apps.de/).

## Install

To use this module in your project, you have multiple options. The easiest is to install it using the `pip` packetmanager:

    pip install osnapi
    
You can also clone this repo and create an editable install, in case you want to customize e.g. the error messages behaviour:

    git clone <this repo>
    cd <this repo>
    pip install -e .
    
This module uses [nbdev](https://github.com/fastai/nbdev), a jupyter notebook based environment. If you go for the editable install, we recommend you to take a short look at nbdev first.

If you want a simple portable module, you can also just copy the __osnapi__ folder into your project. No installation necessary.

## How to use

Once you have installed this module using any of the methods above, you can use

    import osnapi as api
    
and start coding.

If you want to use functions that require a login, use:

    api.login(username, password)
    
The default api_enpoint is https://www.opensense.network/beta/api/v1.0/. This is stored inside the `Settings` object.

The `Settings` object looks like this:
```python
class Settings():
    api_endpoint = 'https://www.opensense.network/beta/api/v1.0/'
    username     = None
    password     = None
    auth_token   = None
```

To change the `api_endpoint`, `username`, `password`, or `auth_token` manually, simply assign to the Settings objects class variables e.g. `api.Settings.username = 'Alice'`. Doing this is normally not necessary, because the values will automatically be filled out when using `api.login()`.  
It's important that you do not use an instance of Settings, but the class directly, because instanced changes will not be seen by the module.  
To view your current settings, you can however instantiate a Settings object with `api.Settings()`. Its string representation will display the current settings.  

The authentication tokens you get from the server are JSON Web Tokens.  
A Token is valid for one hour, but will automatically be reaquired using the credentials saved in Settings, once it runs out.

For an overview and documentation of the available functionality, check out the links at the top of this README

## References

An example of a project using this api is: https://github.com/flpeters/serverless_opensense_dwd_importer  
In that project we implement a data importer that downloads data from https://www.dwd.de/ and pushes that data to opensense.
