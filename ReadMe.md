# Setup

## Environment variables
Copy `env.template` to `.env` and fill it with valid values.

## Docker compose
Create the `Docker compose` environment (make sure to pass the environment variables to `docker compose`:

    set -a 
    source .env
    set +a
    docker-compose -f docker/docker-compose.yaml -p coins build
    docker-compose -f docker/docker-compose.yaml -p coins up

# Super user

The website creates a super user account on start. It's credentials are:

    username: test_user
    password: foobar2022

# Generating API keys

Once you have the docker compose environment set up go to the [admin page](http://localhost:8000/admin/rest_framework_api_key/apikey/),
login and create a API key.

To perform a REST API request add the authorization header:

    Authorization:Api-Key <YOUR-KEY>
