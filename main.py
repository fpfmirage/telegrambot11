import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

TOKEN = "TOKEN_BOT"
CHANNEL = "@CHANNEL_USERNAME"

ADMIN_ID = 123456789

bot = Bot(TOKEN)
dp = Dispatcher()

songs = {}


def join_button():
    kb = InlineKeyboardBuilder()

    kb.button(
        text="📢 عضویت در کانال",
        url=f"https://t.me/{CHANNEL.replace('@','')}"
    )

    kb.button(
        text="✅ عضویت کردم",
        callback_data="check_join"
    )

    kb.adjust(1)

    return kb.as_markup()



@dp.message(CommandStart())
async def start(message: types.Message):

    args = message.text.split()

    if len(args) > 1:

        code = args[1]

        try:
            member = await bot.get_chat_member(
                CHANNEL,
                message.from_user.id
            )

            if member.status in ["left", "kicked"]:

                await message.answer(
                    "❌ اول عضو کانال شو\nبعد روی دکمه بزن",
                    reply_markup=join_button()
                )

                return

        except:
            pass


        if code in songs:

            await message.answer_audio(
                songs[code],
                caption="🎵 موزیک شما"
            )


    else:
        await message.answer("سلام 👋")




@dp.callback_query(lambda c: c.data=="check_join")
async def check(callback: types.CallbackQuery):

    try:

        member = await bot.get_chat_member(
            CHANNEL,
            callback.from_user.id
        )

        if member.status not in ["left","kicked"]:

            await callback.message.answer(
                "✅ تایید شد\nحالا لینک آهنگ رو دوباره باز کن"
            )

        else:

            await callback.answer(
                "هنوز عضو کانال نشدی ❌",
                show_alert=True
            )

    except:
        pass




@dp.message()
async def upload(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return


    if message.audio:

        file_id = message.audio.file_id

        code = message.audio.file_unique_id

        songs[code] = file_id


        link = f"https://t.me/{(await bot.get_me()).username}?start={code}"


        await message.answer(
            f"✅ لینک آماده شد:\n\n{link}"
        )



async def main():
    await dp.start_polling(bot)


asyncio.run(main())