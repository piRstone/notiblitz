#############################
# ALL VARIABLES MUST BE SET #
#############################

# Set here the region you want to be notified if lightning strike inside.
# It must be a list of lists of coordinates (lng, lat).
# Use https://geojson.io/ to do so.
#
# e.g.: REGION = [[-0.65, 44.84], [-1.01, 43.55], [0.10, 43.28]]

REGION =


# Set here your Pushover credentials
USER_TOKEN =
APP_TOKEN =

# Time to wait before 2 notifications (minutes)
NOTIFICATION_DELTA = 5

# Set your Mapbox access token to display the striked city name (default to None)
MAPBOX_TOKEN = None
