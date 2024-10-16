# Path of Modifiers - Deployment

## Preparation

 - Have a remote server ready and available.
 - Configure the DNS records of your domain to point to the IP of the server you just created.
 - Configure a wildcard subdomain for your domain, so that you can have multiple subdomains for different services, `*.pathofmodifiers.com`. This will be useful for accessing different components, like `traefik.pathofmodifiers.com`, `adminer.pathofmodifiers.com`, etc. And also for staging, like `staging.pathofmodifiers.com`, `staging.adminer.pathofmodifiers.com`, etc.
 - Install and configure [Docker Engine](https://docs.docker.com/engine/install/ubuntu/) on the remote server (Docker Engine, not Docker Desktop).

## Setting up environment variables

Follow the steps to set the `changethis` variables in [Generate secret keys](#generate-secret-keys).

### <a id="generate-secret-keys"></a> Generate secret keys

Some environment variables in the `.env` file have a default value of `changethis`.

You have to change them with a secret key, to generate secret keys you can run the following command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the content and use that as password / secret key. And run that again to generate another secure key.

2. In directory `./src/.env`, change these variables:
  - `DOMAIN=pathofmodifiers.com`
  - `ENVIRONMENT=production`
  - `PRIVATIZE_API=`
  - `TESTING=`
  - `MANUAL_NEXT_CHANGE_ID=`
  - `CURRENT_SOFTCORE_LEAGUE=changethis`
  - All of the `changethis` variables


3. In directory `./src/frontend/src/.env`, change these variables:

  - `VITE_API_URL=https://pathofmodifiers.com`
  - `VITE_APP_DEFAULT_LEAGUE=Settlers`
  - `VITE_APP_TURNSTILE_SITE_KEY=changethis`

## Change decoy content files with hidden ones

In `src/frontend/src/hooks/graphing`, replace the decoy files with hidden `*.tsx` graphing hooks.

## Traefik network

### Traefik Docker Compose

- Create a remote directory to store your Traefik Docker Compose file:

```bash
sudo mkdir -p /root/code/traefik-public/
```

- Move the Traefik Docker Compose file to your server. You could do it by running this command with rsync in the server instance:

```bash
sudo mv docker-compose.traefik.yml /root/code/traefic-public/
```

If you are using a different user or domain, change the user `ubuntu` or domain `pathofmodifiers.com`.

### Traefik Public Network

Traefik will expect a Docker public network named `traefik-public` to communicate with your stack(s).

This way, there will be a single public Traefik proxy that handles the communication (HTTP and HTTPS) with the outside world, and then behind that, you could have one or more stacks with different domains, even if they are on the same single server.

To create a Docker public network named `traefik-public` run the following command in your remote server:

```bash
docker network create traefik-public
```

### Traefik Environment Variables

The Traefik Docker Compose file expects some environment variables to be set in your terminal before starting it. You can do it by running the following commands in your remote server.

Create the username for HTTP Basic Auth, e.g.:

```bash
export USERNAME=admin
```

Create an environment variable with the password for HTTP Basic Auth, e.g.:

```bash
export PASSWORD=changethis
```

Use openssl to generate the "hashed" version of the password for HTTP Basic Auth and store it in an environment variable:

```bash
export HASHED_PASSWORD=$(openssl passwd -apr1 $PASSWORD)
```

To verify that the hashed password is correct, you can print it:

```bash
echo $HASHED_PASSWORD
```

Create an environment variable with the domain name for your server, e.g.:

```bash
export DOMAIN=pathofmodifiers.com
```

Create an environment variable with the email for Let's Encrypt:

```bash
export EMAIL=team@pathofmodifiers.com
```

Create an environment variable with the CF_DNS_API_TOKEN for cloudfare api token:

```bash
export CF_DNS_API_TOKEN=changethis
```

### Start the Traefik Docker Compose
Go to the directory where you copied the Traefik Docker Compose file in your remote server:

```bash
cd /root/code/traefik-public/
```

Now with the environment variables set and the `docker-compose.traefik.yml` in place, you can start the Traefik Docker Compose running the following command:

```bash
docker compose -f docker-compose.traefik.yml up -d
```

## Oracle cloud open connections

To open port 80 (HTTP) and 443 (HTTPS), run the commands below in the oracle cloud instance:

```bash
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo netfilter-persistent save
```
