# Deployment `runfrog.de`
This document provides information on how to deploy the `frog-site` on a server
(https://runfrog.de). For development see [./README_site_develop.md](./README_site_develop.md).

The `runfrog` stack is provided as docker containers managed by `docker-compose`.
In typical setups a proxy server acceps all requests on a given IP and 
proxies the requests to the respective services. 

Necessary steps for the setup are
* test that sites works locally
* setup the proxy server (register service in nginx under endpoint)
* create SSH certificates for proxy server
The setup consists normally of 
setting up the proxy server (with https certificates) and the server with running 
the docker containers.

## Test site
See instructions in 

## Setup proxy
**Setup domain**
First the domain must be setup to point to the correct IP. 

**Login to server**  
Login via SSH to the proxy server `denbi-head`

**Activate page**  
The page must be copied and activated. Make sure to **update the IP** of the server 
in nginx configuration!
```
sudo cp <repo>/nginx/runfrog.de /etc/nginx/sites-available/runfrog.de
sudo ln -s /etc/nginx/sites-available/runfrog.de /etc/nginx/sites-enabled/
```

### SSH Certificates
#### Initial certificates
Get certificates for `runfrog.de,www.runfrog.de`
```
sudo service nginx stop
sudo certbot certonly
sudo service nginx start
sudo service nginx status
```
Setup webroot for renewal (check)
```
sudo mkdir -p /usr/share/nginx/letsencrypt
sudo certbot certonly --webroot
```
#### Certificate renewal
```
sudo certbot certonly --webroot
runfrog.de, www.runfrog.de
```

## Setup server
On the actual server the containers are orchestrated using `docker-compose`.
Login to server `denbi-node-4`.

### Initial setup
```
cd /var/git
git clone https://github.com/matthiaskoenig/fbc_curation.git
git checkout develop
```

**start containers**
Pull latest changes 
```
./deploy.sh
```




