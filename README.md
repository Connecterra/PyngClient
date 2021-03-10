# PyngClient

## About

PyngClient can be used to periodically send a ping to the GenericPingMonitoringing service.

## Features

- Support python 3.6+
- Send a 'GenericPing' update to the GenericPingMonitoringService.
- Automatically create a new ping monitor if it does not exist yet

## Installation

```bash
pip install ctra-ping-client
```

### Notes

- PyngClient is supported for python 3.6+ (due to usage of f-strings)
- Automatic re-authentication after token expiration is not supported if another odata client is used to authenticate and the token is passed in.
- By default, the ping will not update the server's alertTimeoutFrequency (ping timeout) after initial creation. To force modifying the interval from your application, include the `override_ping_timeout` flag to True.
- The alertFrequencyTimeout (ping timeout) is always at least 5minutes (300 seconds)

## How to use

### Basic example

The most basic example assumes you have odataUrl, authUrl, username and password set as environment variables (for example with a .env file if using pipenv)

```bash .env
oDataUrl="https://api.domain.io/odata",
authUrl="https://auth.domain.io",
authUsername="",
authPassword="",
```

```python
from pyngclient import GenericPingClient

# Initialize the pingClient
client = GenericPingClient()

# Send it a ping, and set the alertFrequencyTimeout to 1 hour
client.send_ping("YourMonitorName", 3600)

# Alternatively, ISO Durations are supported as an alertFrequencyTimeout as well.
client.send_ping("YourMonitorName, "PT1H")

# By default, the frequencyTimeout will not update after creation of the monitor.
# If it is for some reason changed at the server, the definition in your code will not update it.
# This behavior can be overridden by setting the override_timeout flag:
client.send_ping("YourMonitorName, "PT1H", override_timeout=True)
```

### Instantiation behavior

In additiona to environment variables, it is possible to initialize the GenericPingClient variables instead.
Also, if your application already has odata authentication, and you have a authentication token, it can be passed in directly and used without reauthentication.

```python
# Authenticate without using env vars:
client = GenericPingClient(username=sername, password=password, odata_url=odata_url, auth_url=auth_url)

# Instantiate the client with an already valid auth token
# Note that this method will not allow re-authentication to happen automatically after token expiration as GenericPingClient will not be aware of it.
client = GenericPingClient(token=auth_token)
```

### Usage in long running application

PyngClient also supports long running applications and async behavior.
Instead of calling the `send_ping()` command manually in your code, you can at an async task:

```python

client = GenericPingClient()

async def some_method():

  # Does not have to awaited but will just call send_ping() under the hood after every ping_interval.
  client.run_async("YourMonitorName", ping_interval="PT5M", ping_timeout="PT1H")
```
