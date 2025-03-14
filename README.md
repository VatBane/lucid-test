# lucid-test

## Overview

Test Application for Lucid


## Running

To run application simply run command in root directory:
```docker-compose up -d```

Then you can go to ```localhost:8001/docs``` to interact with endpoints


## Crucial Notes
1) I prefer to separate code in v# folder and then mount to main app, 
for example almost everything besides main.py I would rather move to v1 folder.
It helps to separate different versions and global changes in application
2) I usually use prefixes like '/api/app-name/v1'. 
It helps to understand that it's an API (sometimes API and Web hosted on same address)
3) I would like to use external auth service 'cause it's less vulnerable and more comfortable,
for example Keycloak
4) Cache could be implemented with Redis