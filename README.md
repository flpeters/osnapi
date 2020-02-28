# osnapi
> Unofficial opensense.network API  


If you want to submit data yourself, you can get in touch at https://opensense.network/

The official documentation can be found here: https://www.opensense.network/progprak/beta/apidocs/#/  

The docs for this Project are available at: (insert link here)

## Install

To use this module in your project, you have multiple options. The easiest is to install it using the `pip` packetmanager:

    pip install osnapi
    
You can also clone this repo and create an editable install, in case you want to customize the api's behaviour:

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
    
After successfully logging in, the username and password you used, as well as the token that was returned by the server, are stored inside the `Settings` object.  
The default api_enpoint is "https://dep2.osn.k8s.ise-apps.de/api/v1.0". It is also stored inside the `Settings` object.  
Except for the api_endpoint, the Settings are not defined when you import the package, and are not persisted when you reload.

For an overview and documentation of the available functionality, check out the links at the top of this README
