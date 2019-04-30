# Kin Python Bootstrap
A ready-to-use server using the [Kin Python SDK](https://github.com/kinecosystem/kin-sdk-python/tree/v2-master)

## Prerequisites
Docker software installed:
* [Docker](https://github.com/docker/docker-install)
* [docker-compose](https://docs.docker.com/compose/install)

## Configuration
The server can be configured from the docker-compose.yml file.
If no values are entered, the server will use a default configuration for testing.


|          Variable          | Description                                                                                                                                                                                                                     |
|:--------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SEED          | The seed of your Kin account                                                                                                                                                                                      |
| HORIZON_ENDPOINT          | The URL for the Kin blockchain|
| NETWORK_PASSPHRASE            | The passphrase for the kin blockchain                                                                                                                                                                                                                                                                                                                                                                                       |
| APP_ID                 | The app ID (used to identify transactions)                                                                                                                                                                                                  |
| CHANNEL_COUNT                 | How many channels to use. **See more in the Channels section**|                                                                                                                                                                                   |
| CHANNEL_STARTING_BALANCE                | Initial Kin balance of each channel                                                                                                                        |
| CHANNEL_SALT             | A string to be used when creating the channels                                                                                                                                                      |
| PORT                | Port to serve the app on                                                                                                                                                                                                             |
| LOG_LEVEL             | Log level, either "INFO" or "ERROR"                                                                                                                                                      |


## Running the Server
```bash
$ docker-compose up -d
```

Logs can be accessed with
```bash
$ docker-compose logs
```

## External API

The API for the server can be viewed here:
https://editor.swagger.io?url=https://raw.githubusercontent.com/kinecosystem/kin-python-bootstrap/master/api.yaml

## Channels
Channels are additional accounts that are used internally in the Kin SDK to increase the performance of the server.
Simply put, if you have X channels, you will be able to perform X transactions at the same time.

**CHANNEL_COUNT**
When configuring the number of channels, we recommend to just leave it at 100.
Otherwise, the acceptable values are 0<=X<=100 (0 channels will still allow for processing one transaction at a time)

**CHANNEL_STARTING_BALANCE**
When the server starts for the first time, it will create the channels for you.
The channels need to have a small amount of Kin in them to pay for fees.
This is a one-time operation, so turning the server off/on again will will not cost you more Kin.
If you are whitelisted, you may leave this value at 0, otherwise, we recommend 1.

**CHANNEL_SALT**
This is a string that the server uses to generate your channels.
If you are only setting up one instance of the server, you may leave this value empty.
If you are setting up multiple instances of the server, make sure to input a different string in the configuration of each one.
