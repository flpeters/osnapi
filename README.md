# osnapi
> Unofficial opensense.network API  


If you want to submit data yourself, you can get in touch at https://opensense.network/

The official documentation can be found here: https://www.opensense.network/progprak/beta/apidocs/#/  

The docs for this Project are available at: https://flpeters.github.io/osnapi/

An example of a project using this api is: https://github.com/flamestro/serverless_opensense_dwd_importer  
In that project we implement a data importer that downloads data from https://www.dwd.de/ and pushes that data to opensense.

## What is https://opensense.network/?

OpenSense is "A participatory open sensor data platform", making a uniform data format for a variety of open source weather data sources available to the public.

## Install

To use this module in your project, you have multiple options. The easiest is to install it using the `pip` packetmanager:

    pip install osnapi
    
You can also clone this repo and create an editable install, in case you want to customize e.g. the error messages behaviour:

    git clone <this repo>
    cd <this repo>
    pip install -e .
    
This module uses [nbdev](https://github.com/fastai/nbdev), a jupyter notebook based environment. If you go for the editable install, we recommend you to take a short look at nbdev first.

If you want a lightweight portable module, you can also just copy the __osnapi__ folder into your project. No installation necessary.

## How to use

Once you have installed this module using any of the methods above, you can use

    import osnapi as api
    
and start coding.

If you want to use functions that require a login, use:

    api.login(username, password)
    
The default api_enpoint is https://www.opensense.network/beta/api/v1.0/. It is also stored inside the `Settings` object.

To change the `api_endpoint`, `username`, `password`, or `auth_token` manually, simply assign to the Settings objects class variables e.g. `api.Settings.username = 'Alice'`. It's important that you do not use an instance of Settings, but the class directly, because instanced changes will not be seen by the module.  
To view your current settings, you can instantiate a Settings object with `api.Settings()`. Its string representation will display the current settings.  
Except for the api_endpoint, the Settings are not defined when you import the package, and are not persisted when you reload. They are however automatically added when you use `api.login()`.

The authentication tokens you get from the server are JSON Web Tokens.  
A Token is valid for one hour, but will automatically be reaquired using the credentials saved in Settings, once it runs out.

For an overview and documentation of the available functionality, check out the links at the top of this README
