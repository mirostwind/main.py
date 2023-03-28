from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from fuctions import start, get_region, get_region_inline, get_district, get_district_inline, update_contact_info


def main() -> None:
    updater = Updater("6247558900:AAH7P3GGMIbE3W5DD-pCsAIRHoAOxn3YjMg")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("start", start),

            ],
            states={
                "region": [
                    # MessageHandler(Filters.text, get_region),
                    CallbackQueryHandler(get_region_inline)
                ],
                "district": [
                    MessageHandler(Filters.text, get_district),
                    CallbackQueryHandler(get_district_inline)
                ],
                "phone": [
                    MessageHandler(Filters.contact, update_contact_info)
                ]
            },
            fallbacks=[
                CommandHandler("start", start)
            ]
        )
    )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()