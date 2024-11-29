# Music Machine

#### Video Demo:
https://youtu.be/-7BasCENJQ8

#### Description:
**Music Machine** is a Python-based program designed to intelligently select and play music based on various environmental and temporal factors. Created as a **CS50P Final Project**, this project combines creativity, technical problem-solving, and my passion for music. The goal was simple yet meaningful: eliminate distractions caused by indecision over music selection, allowing users to focus on their tasks while enjoying a tailored listening experience.

By leveraging data such as the time of day, current weather, season, and even the moon phase, Music Machine selects the most appropriate playlist from a library of about 1,000 songs. The program then launches the playlist through VLC Media Player, operating seamlessly in the background.

This project challenged me to work with APIs, integrate external libraries, automate a multimedia workflow, and design a program that solves a real-world problem in an elegant way.

---

### Features:
1. **Automated Music Selection:**
   - The program dynamically selects a playlist based on:
     - **Time of Day:** Different playlists for morning and evening.
     - **Weather Conditions:** Tailored music for rainy days, heatwaves, or cold spells.
     - **Moon Phase:** Special playlists for full-moon nights.
     - **Season:** Music that reflects the mood of spring, summer, autumn, or winter.

2. **Offline Functionality:**
   - If internet access is unavailable, the program falls back to selecting music based on the current season. This ensures the program works reliably without external dependencies.

3. **Integration with VLC Media Player:**
   - Music Machine uses VLC’s command-line capabilities to play playlists in a randomized, looped format. This creates a diverse listening experience without requiring user intervention.

4. **Customizable Music Library:**
   - Users can easily modify the pre-defined music directories to include their own playlists, ensuring a personalized experience.

5. **Fallback Mechanisms:**
   - If the weather or moon phase data is unavailable due to API issues, the program still selects an appropriate playlist based on other factors.

---

### Playlists:
The program organizes music into the following ten themes:
- **Seasonal Themes:**  
  - Spring  
  - Summer  
  - Autumn  
  - Winter  
- **Special Weather Conditions:**  
  - Heatwave  
  - Coldwave  
  - Rainy Day  
- **Time-Based Themes:**  
  - Morning  
  - Evening  
- **Lunar Themes:**  
  - Full Moon  

Each playlist is stored in its own directory, making it easy for users to update or customize the library.

---

### How It Works:
1. **Data Retrieval:**
   - **Weather Data:** The program uses the OpenWeather API to gather real-time data, including temperature and weather conditions like rain, storms, or clear skies.  
   - **Moon Phase Data:** It leverages the IP Geolocation API to determine the current moon phase.

2. **Theme Selection:**
   - The program evaluates multiple factors to determine the most appropriate playlist:
     - **Time of Day:** For early mornings (6:00–8:00 AM) or early evenings (6:00–8:00 PM), time-specific playlists are prioritized.
     - **Moon Phase:** On nights with a full moon, a special "Full Moon" playlist is selected.  
     - **Weather Conditions:** For extreme temperatures or rainy weather, the program picks a corresponding playlist.  
     - **Seasonal Context:** When other factors are neutral or unavailable, the program defaults to a playlist that matches the current season.

3. **Music Playback:**
   - Once a theme is selected, the program launches VLC Media Player to play the music directory associated with the chosen theme. The playback is randomized and looped for continuous listening.

4. **Fallback System:**
   - If either the weather API or moon phase API is offline, the program gracefully falls back to selecting music based on the time or season.

---

### Code Walkthrough:

#### Data Retrieval Functions:
The program uses APIs to fetch weather and moon phase data, ensuring the music selection aligns with real-time environmental conditions.  

```python
def get_wea_data():
    """Fetch weather data from the OpenWeather API."""
    try:
        response = requests.get(wea_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"WEA-OFFLINE: {e}")
        return None

def get_geo_data():
    """Fetch moon phase data from the IP Geolocation API."""
    try:
        response = requests.get(geo_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"GEO-OFFLINE: {e}")
        return None
```

#### Theme Selection Logic:

The program evaluates multiple conditions to determine the best playlist. It prioritizes time-based themes first, then checks moon phase data, weather conditions, and finally defaults to the current season if no other criteria are met.

```python
def select_theme(wea_data, geo_data):
    """Select the most appropriate music theme based on current conditions."""
    hour = datetime.datetime.now().hour
    if 6 <= hour < 8:
        return "morning"
    if 18 <= hour < 20:
        return "evening"

    if geo_data:
        moon_phase = geo_data.get("moon_phase", "").lower()
        if "full" in moon_phase:
            return "full-moon"

    if wea_data:
        degrees = wea_data["main"]["temp"]
        weather = wea_data["weather"][0]["main"].lower()
        if degrees > 30:
            return "heat-wave"
        if degrees < 0:
            return "cold-wave"
        if "rain" in weather:
            return "rainy-day"
    
    return get_season(datetime.datetime.now().month)
```

#### Playback Function:

Music is played using VLC Media Player. The program ensures that the selected music directory exists before attempting playback.

```python
def play_music(theme):
    """Play the selected music theme using VLC Media Player."""
    vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
    music_dir = MUS_DIR[theme]
    if not os.path.exists(music_dir):
        raise FileNotFoundError(f"The directory {music_dir} does not exist.")
    subprocess.run([vlc_path, '--qt-start-minimized', '--loop', '--random', music_dir])
```

### Challenges:
Developing **Music Machine** involved overcoming several challenges:

1. **API Integration:** Learning how to fetch and handle data from external APIs, including error handling and fallback mechanisms.
2. **Offline Functionality:** Designing a system that works seamlessly even without internet access by relying on time and seasonal data.
3. **VLC Integration:** Automating VLC Media Player using Python's `subprocess` module to control playback.
4. **User Experience:** Ensuring the program is intuitive and doesn’t require user intervention after being launched.

---

### Future Plans:
1. **Enhanced Customization:**
    - Add the ability for users to create and name custom playlists directly through the program.
    - Include more granular time-of-day themes (e.g., mid-afternoon, late-night).
2. **Expanded Data Integration:**
    - Incorporate more weather conditions, such as snowstorms or fog.
    - Support additional lunar phases like new moon or waxing crescent.
3. **Graphical User Interface (GUI):**
    - Build a user-friendly interface to allow playlist customization and playback controls.
4. **Cross-Platform Support:**
    - Adapt the program for macOS and Linux users.

---

**Music Machine** represents the intersection of technology, creativity, and personal passion. By automating music selection, it enhances focus, productivity, and enjoyment in everyday tasks. This project reflects my growth as a programmer and my ability to solve real-world problems with code.
