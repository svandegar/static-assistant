# Static Assistant
## Intro
This tool is a small backend meant to provide different useful features for static websites. 
e.g.: form endpoint, newsletter registration endpoint, etc.


# Features
## Email form forwarding
Use this assistant to forward forms on a static website to an email address. The configurable spam blacklist keeps your inbox clean.

## Newsletter registration
Work in progress. Should be released soon.

# How to use it?
The setup process is in two steps: 
1. Deploy this to your favourite server. (see [Deploy](##Deploy))
2. Point your form to `yourserveraddress/contact`
And voilà 

## Deploy
Two different options:
1. Deploy to a VPS
2. Deploy to a PaaS

### VPS
Follow the process described under [Contribution](#Contribution) on a VPS, then configure NGINX [See Digital Ocean's doc](https://blog.nawaz.info/deploy-fastapi-application-on-ubuntu-with-nginx-gunicorn-and-uvicorn)

### PaaS
A Digital Ocean config fill will be added to the project soon.

## Config
The assistant is highly configurable. The goal is to be able to deploy one instance and use it for multiple sites.

All the configuration lies in a JSON config file at `config/config.json`

Here's an example: 
```json
{
  "allowed_sources": ["testserver", "localhost"], // requests not coming from one of these hosts will be rejected
  "email": {
    "allow_default_to": true, // if true, requests fron an host not configured in "to" will be forwarded to the default email. If false, they will be rejected 
    "from": "jean@petit.be", // sender email address. Must be the one configured in your Postman account
    "to": {
      "default": "jean@petit.be", // default forward to email
      "myapp": "me@myapp.com" // "host" : "fowrward to email". This is useful to use one deployment of this tool for multiple static websites with different form recipients
    }
  },
  "spam": {
    "emails": ["spammer@email.be"], // emails spamlist. Requests with one of these as reply_to address will be rejected
    "content": ["please check this obscure website"] // requests with these sequences in the body will be rejected
  }
}
```



# Contribution
Contributions are welcome in the form of PR's. Please open an issue first, so we can discuss the change beforehand.   
Here's how to setup your local environment:

## Prerequisites
- Python 3.9
- A [Postmark](https://postmarkapp.com/) account and API token.
## Setup local environment
1. Clone this repos
```bash
git clone git@github.com:svandegar/static-assistant.git && cd static-assistant
```
2. Create a virtual environment at the project root
```bash
virtualenv venv
```
3. Activate the virtual environment
```bash
source venv/bin/activate
```
4. Install the Python dependencies
```bash
pip install -r requirements
```
5. Duplicate `config/.env.example` and rename it to `.env`
```bash
cp config/.env.example config/.env
```
6. Add your Postmark token in .env
7. Add your own config to `config/contig.json` (see [Config](#config) section)
8. Run the tests
```bash
pytest
```
