# notiblitz

v1.0.0

Thunderbolt detector based on [Blitzortung](http://blitzortung.org) data.

Receive a Pushover notification if a lightning strikes in your area.

If a Mapbox access token is set, the city name will be displayed in the notification message.

## Installation

_Use python 3.5 and later._

1. Create a virtualenv and source it:

```
python -m venv .venv
```

2. Install dependencies:

```
pip install -r requirements
```

3. Copy the `config.example.py` as `config.py` and fill in the environment variables.

4. Run the app:

```
python app.py -v
```

_Use `-v` option to see `DEBUG` logs._
