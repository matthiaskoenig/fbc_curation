# runfrog-site
This document describes how to setup and run the `runfrog-site` webpage locally. 
For deployment see [./README_site_deploy.md](./README_site_deploy.md)

## Technology
The following technology is used for the `runfrog-site`:
1. Backend API: `fbc_curation` python package served using FastAPI service [https://fastapi.tiangolo.com/]
2. Frontend User Interface: Vue.js 3 [https://vuejs.org/]
    - TypeScript + SCSS
    - Vuex
    - Vue Router
3. Frontend UI/UX Package: PrimeVue

## Vue.js devtools
Vue 3 is only working with the beta version of the devtools available from
https://github.com/vuejs/vue-devtools/releases.
For setup download and install the `xpi` package.

## Project setup

### Install all dependencies
```
cd runfrog-site
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```
