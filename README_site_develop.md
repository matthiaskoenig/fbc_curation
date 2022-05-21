# runfrog-site 
This document describes how to setup and run the `runfrog-site` 
([https://runfrog.de](https://runfrog.de))site for local development. 
For information on how to deploy the page see 
[./README_site_deploy.md](./README_site_deploy.md).

## Technology
The following technology is used in the `runfrog-site`:
1. Backend API: `fbc_curation` python package served using FastAPI [https://fastapi.tiangolo.com/]
2. Frontend User Interface: Vue.js 3 [https://vuejs.org/]
    - TypeScript + SCSS
    - Vuex
    - Vue Router
3. Frontend UI/UX Package: PrimeVue

## Vue.js devtools
Vue 3 is only working with the beta version of the devtools available from
https://github.com/vuejs/vue-devtools/releases.
For setup download and install the `xpi` package.

## Run local development server

### Install all dependencies
```
cd runfrog-site
npm install
```

### Start development server
To run the local development server on http://localhost:4567/
```
npm run serve
```
In addition, the API must be served locally via 

```
(frog) python src/fbc_curation/api.py 
```

## Run local docker server

```
docker-compose -f docker-compose-develop.yml build --no-cache
```
