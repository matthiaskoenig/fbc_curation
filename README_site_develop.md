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

Development should be run with node version 14. 
See here for installation instructions
https://github.com/nodesource/distributions/blob/master/README.md#deb
```
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs
```


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

Buildkit must be enabled via
https://docs.docker.com/develop/develop-images/build_enhancements/#to-enable-buildkit-builds
To enable docker BuildKit by default, set daemon configuration in /etc/docker/daemon.json feature to true and restart the daemon:
```
{ "features": { "buildkit": true } }
```


```
docker-compose -f docker-compose-develop.yml up --detach
```
