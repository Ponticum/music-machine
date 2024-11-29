import os
import subprocess
import datetime
import requests

# Set City and API Key
CITY = "Győr"
WEA_API = "---"  # OpenWeather API Key
GEO_API = "---"  # IP Geolocation API Key

# Set Music Directories
MUS_DIR = {
    "spring": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Sprouting Sessions",
    "summer": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Sunflower Sessions",
    "autumn": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Scarecrow Sessions",
    "winter": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Snowfall Sessions",

    "full-moon": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Starlight Sessions",
    "heat-wave": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Sunscreen Sessions Vol. 1",
    "cold-wave": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Subzero Sessions",
    "rainy-day": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Stormcloud Sessions",

    "morning": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Stairwell Sessions Vol. 3",
    "evening": r"C:\Users\Marton Toth\Music\Sonic Alchemy\Streetlight Sessions",
}

# End for Weather Data
wea_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={WEA_API}&units=metric"
geo_url = f"https://api.ipgeolocation.io/astronomy?apiKey={GEO_API}&location={CITY}"


def main():
    theme = select_theme(get_wea_data(), get_geo_data())
    play_music(theme)


def get_wea_data():
    """
    Get weather data from OpenWeather API.
    """
    try:
        response = requests.get(wea_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"WEA-OFFLINE: {e}")
        return None


def get_geo_data():
    """
    Get moon phase data from IP Geolocation API.
    """
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"GEO-OFFLINE: {e}")
        return None


def select_theme(wea_data, geo_data):
    """
    Select a music directory based on time.
    """
    # By time of day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    print(f"\nTime: {hour:02d}:{minute:02d}")
    if 6 <= hour < 8:
        return "morning"
    if 18 <= hour < 20:
        return "evening"
    if geo_data:
        moon_phase = geo_data.get("moon_phase", "").lower()
        print(f'Moon: {moon_phase.replace("_", " ").title()}')
        if "full" in moon_phase:
            return "full-moon"

    # By the weather
    if wea_data:
        degrees = wea_data["main"]["temp"]
        weather = wea_data["weather"][0]["main"].lower()
        print(f"WX: {degrees:.1f}°C - {weather.capitalize()}")
        if degrees > 30:
            return "heat-wave"
        if degrees < 0:
            return "cold-wave"
        if "rain" in weather or "storm" in weather:
            return "rainy-day"
    # By the season
    return get_season(datetime.datetime.now().month)


def get_season(month):
    """
    Determine the season based on the date.
    """
    if month in [3, 4, 5]:
        return "spring"
    elif month in [6, 7, 8]:
        return "summer"
    elif month in [9, 10, 11]:
        return "autumn"
    else:
        return "winter"


def play_music(theme):
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    music_dir = MUS_DIR[theme]
    if not os.path.exists(music_dir):
        raise FileNotFoundError(f"The directory {music_dir} does not exist.")

    # Open VLC and play the theme
    print(f'\n▶ Playing - {theme.replace("-", " ").title()}')
    subprocess.run([vlc_path, '--qt-start-minimized', '--loop', '--random', music_dir])


if __name__ == "__main__":
    main()
