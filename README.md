# notiblitz

Thunderbolt detector based on [Blitzortung](http://blitzortung.org) data.

_Work in progress._

## Installation

Create a virtualenv and source it:

```
virtualent venv -p python3.7
```

Install dependencies:

```
pip install -r requirements
```

Run app:

```
python app.py
```

## TODO

- Define region to listen.
- Check if strike is inside region.
- Notify via [Pushover](https://pushover.net/) application.
