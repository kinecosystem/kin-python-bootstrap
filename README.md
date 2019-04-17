# kin-python-bootstrap
A ready to use server using the kin-python-sdk

## Prerequisites
* [Docker](https://github.com/docker/docker-install)
* [docker-compose](https://docs.docker.com/compose/install)

## Configuration
The server can be configured from the docker-compose.yml file
If no values are passed, the server will use a default configuration for testing


|          Variable          | Description                                                                                                                                                                                                                     |
|:--------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SEED          | The seed of your kin account                                                                                                                                                                                      |
| HORIZON_ENDPOINT          | The url for the kin blockchain|
| NETWORK_PASSPHRASE            | The passphrase for the kin blockchain                                                                                                                                                                                                                                                                                                                                                                                       |
| APP_ID                 | The app id (used to identify transactions)                                                                                                                                                                                                  |
| CHANNEL_COUNT                 | How many channels to use. **Read more in the "Channels" section**|                                                                                                                                                                                   |
| CHANNEL_STARTING_BALANCE                | How much Kin to create each channels with.                                                                                                                        |
| CHANNEL_SALT             | A string to be used when creating the channels                                                                                                                                                      |
| PORT                | Port to serve the app on.                                                                                                                                                                                                             |
| LOG_LEVEL             | Log level, either "INFO" or "ERROR"                                                                                                                                                      |


## Running the server
```bash
$ docker-compose up -d
```

Logs can be accessed with
```bash
$ docker-compose logs
```

## External API

The api for the server can be shown visually here:
https://editor.swagger.io?url=https://raw.githubusercontent.com/kinecosystem/kin-python-bootstrap/master/api.yaml

## Channels
Channels are additional accounts that are used internally in the kin-sdk to increase the performance of the server.
Simply put, if you have X channels, you will be able to perform X transactions at the same time.

**CHANNEL_COUNT**
When configuring the amount of channels, we recommend to just leave it at 100.
Otherwise, the acceptable values are 0<=X<=100 (0 Channels will still allow for 1 concurrent transaction)

**CHANNEL_STARTING_BALANCE**
When the server is starting for the first time, it will create the channels for you.
The channels need to have a small amount of Kin in them to pay for fees.
This is a one-time operation, so turning off/on the server will not take more Kin from you again.
If you are whitelisted, feel free to leave this value at 0, otherwise, we recommend 1.

**CHANNEL_SALT**
This is a string that the server is using to generate your channels.
If you are only setting one instance of the server, feel free to leave this value empty.
If you are setting up multiple instances of the server, make sure to input a different string in the configuration of each one