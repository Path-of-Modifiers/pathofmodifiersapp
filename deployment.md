# Path of Modifiers - Deployment

## Preparation

 - Have a remote server ready and available.
 - Configure the DNS records of your domain to point to the IP of the server you just created.
 - Configure a wildcard subdomain for your domain, so that you can have multiple subdomains for different services, `*.pathofmodifiers.com`. This will be useful for accessing different components, like `traefik.pathofmodifiers.com`, `adminer.pathofmodifiers.com`, etc. And also for staging, like `staging.pathofmodifiers.com`, `staging.adminer.pathofmodifiers.com`, etc.
 - Install and configure [Docker](https://docs.docker.com/engine/install/ubuntu/) on the remote server (Docker Engine, not Docker Desktop).

## Setting up environment variables 

Follow the steps to set the `changethis` variables in [Generate secret keys](#generate-secret-keys). 

### <a id="generate-secret-keys"></a> Generate secret keys

Some environment variables in the `.env` file have a default value of `changethis`.

You have to change them with a secret key, to generate secret keys you can run the following command:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the content and use that as password / secret key. And run that again to generate another secure key.

2. In `src/.env`, change these variables:
  - `DOMAIN=pathofmodifiers.com`
  - `ENVIRONMENT=production`
  - `PRIVATIZE_API=True`
  - `TESTING=False`
  - `MANUAL_NEXT_CHANGE_ID=False`
  - `CURRENT_SOFTCORE_LEAGUE="Current League"`

3. In `src/frontend/vite.config.ts`, use these contents:

```bash
// vite.config.ts
import { TanStackRouterVite } from "@tanstack/router-vite-plugin"
import react from "@vitejs/plugin-react-swc"
import { defineConfig } from "vite"

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), TanStackRouterVite()],
});                                                                                                                                               
```

4. In `src/frontend/src/env-vars.tsx`, change:
```bash
defaultSoftcoreLeague = "Current league";
```

## Change content files with proper ones

In `src/frontend/src/hooks/graphing`, replace the decoy files with hidden `*.tsx` graphing hooks.

## Traefik network

### Traefik Docker Compose

- Create a remote directory to store your Traefik Docker Compose file:

```bash
mkdir -p /root/code/traefik-public/
```

- Copy the Traefik Docker Compose file to your server. You could do it by running the command rsync in your local terminal:

```bash
rsync -a docker-compose.traefik.yml root@your-server.example.com:/root/code/traefik-public/
```

### Traefik Public Network

This Traefik will expect a Docker "public network" named `traefik-public` to communicate with your stack(s).

This way, there will be a single public Traefik proxy that handles the communication (HTTP and HTTPS) with the outside world, and then behind that, you could have one or more stacks with different domains, even if they are on the same single server.

To create a Docker "public network" named `traefik-public` run the following command in your remote server:

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
export EMAIL=pomodifiers@outlook.com
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
