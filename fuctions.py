from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from Buttons.inline import get_regions_button_inline, get_districts_button_inline
from Buttons.keyboard import get_district_button, get_region_button, phone_button
import database


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    print(context.bot, context.bot_data)
    if not database.check_user_in_table(user.id):
        first_name = user.first_name
        last_name = user.last_name
        username = user.username
        telegram_id = user.id
        database.insert_user_to_table(first_name, last_name, username, telegram_id)
        print("endi bu foydalanuvchini tablega qo'shish kerak", first_name, last_name, username, telegram_id)
    user_data = database.get_user_data_with_telegram_id(user.id)
    if not user_data[0][5]:
        update.message.reply_text("Telefon raqamongizni yuborishingiz kerak:", reply_markup=phone_button())
        return "phone"
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"Assalomu alekum xush kelibsiz{user.full_name}. Quyidagi viloyatlardan birini tanlang",
        reply_markup=get_regions_button_inline()
    )
    return "region"


def command_echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)


def get_region(update: Update, context: CallbackContext):
    text = update.message.text
    region = database.get_region_by_title(text)
    if region:
        region_id = region[0][0]
        districts = database.districts_by_region_id(int(region_id))
        if districts:
            update.message.reply_text("""Quyidagi tumanlardan birini tanlang""",
                                      reply_markup=ReplyKeyboardMarkup(get_district_button(districts),
                                                                       resize_keyboard=True))
            return "district"
        else:
            update.message.reply_text("""Siz tanlagan viloyatda tuman kiritlmagan""")
            return "region"
    else:
        update.message.reply_text("""Siz ko'rsatilgan viloyatlardan birini tanlang""")
        return "region"


def update_contact_info(update: Update, context: CallbackContext):
    contact = update.message.contact
    database.update_profile_contact(contact.user_id, contact.phone_number)
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=f"Sizning telefon raqamingiz muvoffaqiyatli saqlandi.Quyidagi viloyatlardan birini tanlang",
        reply_markup=get_regions_button_inline()
    )
    return "region"



def get_region_inline(update: Update, context: CallbackContext) -> str:
    query = update.callback_query
    data = query.data
    region = database.get_region_by_id(int(data))
    if region:
        context.user_data['region_name'] = region[0][1]
        query.message.edit_text(f"Siz tanlagan Viloyat {region[0][1]}\nQuyidagi tumanlardan birini tanlang",
                                 reply_markup=get_districts_button_inline(int(region[0][0])))
        return "district"
    else:
        query.answer("Siz tanlagan Viloyat topilmadi ko'rsatilgan viloyatlardan birini tanlang :)")
    return "region"


def get_district(update: Update, context: CallbackContext):
    district_title = update.message.text
    district = database.get_district_by_title(district_title)
    if district_title == "<<Ortga":
        update.message.reply_text("""Viloyatlardan birini tanlang""",
                                  reply_markup=ReplyKeyboardMarkup(get_region_button()))
        return "region"
    if district:
        district = district[0]
    else:
        update.message.reply_text("""Iltiomos faqat ko'rsatilgan tumanlardan birini tanlang""")
        return "district"
    message = f"""Tuman id raqami: {district[0]}
Viloyat id raqami: {district[1]}
Tuman nomi: {district[2]}"""
    update.message.reply_text(message)


def get_district_inline(update: Update, context: CallbackContext):
    query = update.callback_query

    data = query.data
    if data == 'back':
        query.message.edit_text(text="Quyidagi viloyatlardan birini tanlang", reply_markup=get_regions_button_inline())
        return "region"
    district = database.get_district_by_id(int(data))
    if data:
        text = f"""Viloyat nomi: {context.user_data['region_name']}
Tuman nomi: {district[0][2]}
Tuman id raqami: {district[0][0]}"""
        query.message.edit_text(text=text, reply_markup=get_districts_button_inline(int(district[0][1])))