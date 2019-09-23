# ADBKraken
Discord bot which is capable to manage android-devices which are connected via ADB.

# Things you need no matter how you deploy: 

## Discord bot user
You can create one at: https://discordapp.com/developers/applications/me

There you get your so called `BOT_TOKEN`, which is your token to login to discord.

## Config
- `cp kraken/config.py.dist kraken/config.py`

a config typically look like this:

```python
# Directory where the log file of the bot shall be stored
LOG_PATH = '.'

"""
Discord Section.
"""
# The Token of your botuser.
BOT_TOKEN = 'aasdasdasdasdasdasds'
# Discord Status
PLAYING = 'ADBKraken'
# Command prefix
PREFIX = '!'

DEVICES = {
    'DEVICE1' : '192.168.178.77:5555',
    'DEVICE2' : '192.168.178.95:5555',
}
```

# Things you need to deploy on your host directly:
## System Packages:
- python 3.7
- pip3
- adb

## Deploy
### Install python3 requirements
We recommend to use a virtual environment.
```
python3 -m venv adbkraken-venv
source adbkraken-venv/bin/activate
```

Then install the requirements.
```
pip3 install -U -r requirements.txt
```

### Start the bot
Call:
```
python3 start_bot.py
```

# Things you need to deploy with docker:
## Get Docker
First of all, you have to install Docker CE and docker-compose on your system.

- Docker CE: just execute this script [https://get.docker.com/](https://get.docker.com/) - or read through [https://docs.docker.com/install/](https://docs.docker.com/install/) 
- Docker-compose: [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

These sites are well documented and if you follow the install instructions, you are good to go.

## Docker image and docker-compose file
You can either use the docker-image: https://cloud.docker.com/repository/docker/breedocker/adbkraken
This image is automatically build on each push to github. 

Alternatively you build it locally. 


A docker-compose using the image file looks like this: 
```yaml
version: '2.4'
services:
  kraken:
    image: breedocker/adbkraken
    volumes:
      - ./kraken/:/usr/src/app/
    restart: always
```

A docker-compose which builds the image locally: 
```yaml
version: '2.4'
services:
  kraken:
    build:
      context: .
    volumes:
      - ./kraken/:/usr/src/app/
    restart: always
```

## Deploy:
Just execute:
``` 
docker-compose up -d kraken
```
this will pull/build if the docker-image, the image is not present,  and then start the service.

To examine the logs: 

``` 
docker-compose logs -f kraken
```

Take the service down: 
``` 
docker-compose down
```

To force a full rebuild:
``` 
docker-compose build --no-cache kraken
```