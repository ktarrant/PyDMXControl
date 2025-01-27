from datetime import datetime
from subprocess import run
from time import sleep
from typing import List, Dict, Callable

from PyDMXControl import Colors
from PyDMXControl.controllers import uDMXController as Controller
from PyDMXControl.effects.Color import Color_Chase
from timed_events_data import get_timed_events

# This is my home setup, which also acts as a great demo of some of what this library is capable of doing.
# See the tests directory for other recent/new features that I've possibly been working on.

# Create our controller
dmx = Controller()

# Load some fixtures from JSON
dmx.json.load_config('json/home.json')

# Define some custom colors, a global fade time and the divoom device
custom_blue = [0, 16, 255, 0]
custom_blue_2 = [0, 160, 255, 0]
custom_snow = [32, 48, 255, 0]
custom_cyan = [0, 128, 255, 0]
custom_cyan_2 = [0, 255, 64, 0]
custom_white = [255, 255, int(255 * 0.8), 255]
flood_warm = [255, int(255 * 0.9), int(255 * 0.5), 255]
flood_white = [int(255 * 0.9), 255, 255, 255]
key_white = [int(255 * 0.75), int(255 * 0.9 * 0.75), int(255 * 0.8 * 0.75), 255]
fade_time = 5000
divoom_address = '11:75:58:2D:A8:65'


# Create all the custom state methods

# XMAS state, used throughout the day/evening in December
# Warm shelves + flood, with snowy art/books/board, standard white desk + key
def xmas():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_name_include('Flood'):
        f.color(flood_warm, fade_time)
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_name_include('Shelf'):
        f.color(Colors.Warm, fade_time)
        f.dim(64, fade_time)

    blue_white_group = dmx.get_fixtures_by_name_include('Art') \
                       + dmx.get_fixtures_by_name_include('Board') \
                       + dmx.get_fixtures_by_name_include('Books')
    Color_Chase.group_apply(blue_white_group, 60 * 1000,
                            colors=[custom_blue, custom_snow, custom_blue, custom_blue])
    for f in blue_white_group:
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_name_include('Desk'):
        f.color(custom_white, fade_time)
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_name_include('Key'):
        f.color(key_white, fade_time)
        f.dim(int(255 * 0.25), fade_time)


# Nighttime state, everything off
def night():
    dmx.clear_all_effects()

    for f in dmx.get_all_fixtures():
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    divoom_off()


# Daytime state, used during the day outside December
# White flood + desk + key, no art/shelves/board, blue books
def day():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_name_include('Flood'):
        f.color(flood_white, fade_time)
        f.dim(int(255 * 0.5), fade_time)

    off_group = dmx.get_fixtures_by_name_include('Art') \
                + dmx.get_fixtures_by_name_include('Board') \
                + dmx.get_fixtures_by_name_include('Shelf')
    for f in off_group:
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    for f in dmx.get_fixtures_by_name_include('Desk'):
        f.color(custom_white, fade_time)
        f.dim(255, fade_time)

    books = dmx.get_fixtures_by_name_include('Books')
    for f in books:
        f.dim(255, fade_time)

    Color_Chase.group_apply(books, 60 * 1000,
                            colors=[custom_blue, custom_cyan, custom_blue, custom_blue])

    for f in dmx.get_fixtures_by_name_include('Key'):
        f.color(key_white, fade_time)
        f.dim(int(255 * 0.25), fade_time)

    divoom_on()


# Evening state, used later in the day outside December
# Warm flood, standard white desk + key, blue art/books/board/shelves
def evening():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_name_include('Flood'):
        f.color(flood_warm, fade_time)
        f.dim(255, fade_time)

    main_blue_group = dmx.get_fixtures_by_name_include('Art') \
                      + dmx.get_fixtures_by_name_include('Board') \
                      + dmx.get_fixtures_by_name_include('Books')
    for f in main_blue_group:
        f.dim(255, fade_time)

    Color_Chase.group_apply(main_blue_group, 60 * 1000,
                            colors=[custom_blue, custom_cyan, custom_blue, custom_blue])

    for f in dmx.get_fixtures_by_name_include('Shelf'):
        f.dim(255, fade_time)

    Color_Chase.group_apply(dmx.get_fixtures_by_name_include('Shelf'), 60 * 1000,
                            colors=[custom_blue_2, custom_blue_2, custom_cyan_2, custom_blue_2])

    for f in dmx.get_fixtures_by_name_include('Desk'):
        f.color(custom_white, fade_time)
        f.dim(255, fade_time)

    for f in dmx.get_fixtures_by_name_include('Key'):
        f.color(key_white, fade_time)
        f.dim(int(255 * 0.25), fade_time)


# Late at night state
# No flood + key, warm desk + art/board/shelves, blue books
def late():
    dmx.clear_all_effects()

    for f in dmx.get_fixtures_by_name_include('Flood'):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)

    dim_group = dmx.get_fixtures_by_name_include('Art') \
                + dmx.get_fixtures_by_name_include('Board') \
                + dmx.get_fixtures_by_name_include('Shelf')
    for f in dim_group:
        f.color(Colors.Warm, fade_time)
        f.dim(int(255 * 0.5), fade_time)

    for f in dmx.get_fixtures_by_name_include('Desk'):
        f.color(Colors.Warm, fade_time)
        f.dim(int(255 * 0.75), fade_time)

    books = dmx.get_fixtures_by_name_include('Books')
    for f in books:
        f.dim(255, fade_time)

    Color_Chase.group_apply(books, 60 * 1000,
                            colors=[custom_blue, custom_cyan, custom_blue, custom_blue])

    for f in dmx.get_fixtures_by_name_include('Key'):
        f.color(Colors.Black, fade_time)
        f.dim(0, fade_time)


def divoom_off():
    run(['divoom-control', 'set-brightness', '-a', divoom_address, '-b', '0'], shell=True)
    sleep(2)
    run(['divoom-control', 'set-brightness', '-a', divoom_address, '-b', '0'], shell=True)


def divoom_on():
    run(['divoom-control', 'set-brightness', '-a', divoom_address, '-b', '100'], shell=True)
    sleep(2)
    run(['divoom-control', 'display-custom', '-a', divoom_address], shell=True)
    sleep(2)
    run(['divoom-control', 'set-brightness', '-a', divoom_address, '-b', '100'], shell=True)
    sleep(2)
    run(['divoom-control', 'display-custom', '-a', divoom_address], shell=True)


# Create a time map of states for each day
def get_times() -> List[Dict[int, Callable]]:
    times = [
        {0: night, 900: day, 1800: evening, 2100: late, 2200: night},  # Monday
        {0: night, 900: day, 1800: evening, 2100: late, 2200: night},  # Tuesday
        {0: night, 900: day, 1800: evening, 2100: late, 2200: night},  # Wednesday
        {0: night, 900: day, 1800: evening, 2100: late, 2200: night},  # Thursday
        {0: night, 900: day, 1800: evening, 2100: late, 2200: night},  # Friday
        {0: night, 900: day, 1800: evening, 2100: late, 2200: night},  # Saturday
        {0: night, 900: day, 1800: evening, 2100: late, 2200: night},  # Sunday
    ]
    # Xmas/jingle jam adjustment
    if datetime.today().month == 12:
        for i in range(len(times)):
            del times[i][1800]
            del times[i][2100]
            times[i][900] = xmas
            times[i][2200] = late
            times[i][2300] = night
    return times


last_state = None


# Create the callback to turn lights on/off and change colors at certain times
def callback():
    global last_state

    # Get map for today and current time
    times = get_times()
    time_map = times[datetime.today().weekday()]
    time = int(datetime.today().strftime('%H%M'))

    # Find most recent passed time in the map
    keys = sorted(time_map.keys())
    index = -1
    while index + 1 < len(keys) and keys[index + 1] <= time:
        index += 1
    state = keys[index]

    # Run the mapped state if not previously run
    run_callback = time_map[state]
    if last_state != run_callback:
        run_callback()
        last_state = run_callback


# Enable the callback
dmx.ticker.set_interval(500)
dmx.ticker.set_callback(callback)

# Debug
callbacks = {
    "night": night,
    "day": day,
    "evening": evening,
    "late": late,
    "xmas": xmas,
    "divoom-off": divoom_off,
    "divoom-on": divoom_on,
}
dmx.web_control(callbacks=callbacks, timed_events={
    "you-will-be-found": get_timed_events(dmx)
})
# dmx.debug_control(callbacks)

# Close the controller once we're done
dmx.sleep_till_enter()
dmx.close()
