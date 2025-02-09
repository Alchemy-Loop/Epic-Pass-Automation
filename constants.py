import os

TIMEZONE = str(os.environ.get("TIMEZONE", "MST"))
WEB_LINK = (
    "https://www.epicpass.com/Plan-Your-Trip/Lift-Access/Reservations?reservation=true"
)
RESORT_ID_DICT = {
    "AFTON ALPS": 2,
    "ALPINR VALLEY": 3,
    "ATTITASH MOUNTAIN": 4,
    "BEAVER CREEK": 5,
    "BOSTON MILLS BRANDYWINE": 6,
    "BRECKENRIDGE": 7,
    "CRESTED BUTTE": 8,
    "CROTCHED MOUNTAIN": 9,
    "HEAVENLY": 10,
    "HIDDEN VALLEY": 11,
    "HUNTER": 12,
    "JACK FROST BIG BOULDER": 13,
    "KEYSTONE": 14,
    "KIRKWOOD": 15,
    "LIBERTY MOUNTAIN": 16,
    "MAD RIVER MOUNTAIN": 17,
    "MOUNT SUNAPEE": 18,
    "MT BRIGHTON": 19,
    "MT SNOW": 20,
    "NORTHSTAR": 21,
    "OKEMO": 22,
    "PAOLI PEAKS": 23,
    "PARK CITY": 24,
    "ROUNDTOP MOUNTAIN": 25,
    "SNOW CREEK": 26,
    "STEVENS PASS": 27,
    "STOWE": 28,
    "VAIL": 29,
    "WHISTLER BLACKCOMB": 30,
    "WHITETAIL": 31,
    "WILDCAT MOUNTAIN": 32,
    "WILMOT MOUNTAIN": 33,
}