# Deployment `sbml4humans`
This document provides instructions to deploy `frog-site` on a server. 
In many configurations a proxy server is used which proxies the requests 
to the services running in docker containers. The setup consists normally of 
setting up the proxy server (with https certificates) and the server with running 
the docker containers.

## Setup proxy
- login to proxy server `denbi-head`

**Activate page**  
The page must be copied and activated. Make sure to **update the IP** of the server 
in nginx configuration!
```
sudo cp <repo>/nginx/runfrog.de /etc/nginx/sites-available/runfrog.de
sudo ln -s /etc/nginx/sites-available/runfrog.de /etc/nginx/sites-enabled/
```

### Certificates
#### Initial certificates
Get certificates for `runfrog.de,www.runfrog.de`
```
sudo service nginx stop
sudo certbot certonly
sudo service nginx start
sudo service nginx status
```

#### Certificate renewal
```
sudo mkdir -p /usr/share/nginx/letsencrypt
sudo certbot certonly --webroot
```

## Setup server
On the actual server the containers are orchestrated using `docker-compose`.
Login to server `denbi-node-4`.

### Initial setup
```
cd /var/git
git clone https://github.com/matthiaskoenig/sbmlutils.git
git checkout sbml4humans
```

**start containers**
Pull latest changes 
```
./deploy.sh
```




