import database
from telegram import KeyboardButton, ReplyKeyboardMarkup

def get_region_button():
    button = []
    regions = database.select_all_regions()
    res = []
    for i in regions:
        res.append(i[1])
        if len(res) == 2:
            button.append(res)
            res = []
    if len(res) > 0:
        button.append(res)
    return button


def get_district_button(districts):
    button = []
    res = []
    for i in districts:
        res.append(i[2])
        if len(res) == 2:
            button.append(res)
            res = []
    if len(res) > 0:
        button.append(res)
    button.append(
        ["<<Ortga"]
    )
    return button


def phone_button():
    button = [
        [
            KeyboardButton("Telefon raqamingizni yuboring", request_contact=True)
        ]
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True)


def location_button():
    button = [
        [
            KeyboardButton("Lokatsiyani yuborish", request_location=True)
        ]
    ]
    return ReplyKeyboardMarkup(button, resize_keyboard=True)