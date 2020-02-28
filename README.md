# osnapi
> Summary description here.


The official documentation can be found here: https://www.opensense.network/progprak/beta/apidocs/#/ 
This file will become your README and also the index of your documentation.

## Install

Put this whole folder in your project, and then do `import osnapi as api`.  
`pip install your_project_name`

## How to use

if you want to use functions that require a login, use `api.login(username, password)`.
After successfully logging in, the username and password you used, as well as the token that was returned by the server, are stored inside the `Settings` object.  
The default api_enpoint is "https://dep2.osn.k8s.ise-apps.de/api/v1.0". It is also stored inside the `Settings` object.  
Except for the api_endpoint, the other three Settings are not defined when you import the package.  

> first pass on readme
