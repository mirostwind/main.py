from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import database


def get_regions_button_inline() -> InlineKeyboardMarkup:
    regions = database.select_all_regions()
    button = []
    res = []
    for region in regions:
        res.append(InlineKeyboardButton(region[1], callback_data=region[0]))
        if len(res) == 3:
            button.append(res)
            res = []
    if res:
        button.append(res)
    return InlineKeyboardMarkup(button)


def get_districts_button_inline(region_id) -> InlineKeyboardMarkup:
    districts = database.districts_by_region_id(region_id)
    region = database.get_region_by_id(region_id)
    region_name = region[0][1]
    button = [
        [InlineKeyboardButton(region_name, url="https://kun.uz")]
    ]
    res = []
    for i in districts:
        res.append(InlineKeyboardButton(i[2], callback_data=i[0]))
        if len(res) == 2:
            button.append(res)
            res = []
    if res:
        button.append(res)
    button.append([
        InlineKeyboardButton("Otrga", callback_data="back")
    ])
    return InlineKeyboardMarkup(button)
