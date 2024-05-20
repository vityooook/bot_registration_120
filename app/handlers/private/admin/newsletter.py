import asyncio
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from loguru import logger

# * import requests to database
from database import crud
# * import admin id
from config import ADMIN
# * import callback
from handlers.callback.callback_data import AdminWithoutPhotoCallback, AdminAcceptCallback
# * import inline keyboard
from keyboard.inline.admin.inline_without_photo import without_photo
# * import inline keyboard
from keyboard.inline.admin.inline_accept import accept_newsletter
from loader import bot

router = Router()


class Newsletter(StatesGroup):
    """State class created to store state based on data input"""
    # * state waiting for text input
    text = State()
    # * state waiting for photo input
    photo = State()


@logger.catch()
@router.message(Command("newsletter"))
async def cmd_newsletter(msg: Message, state: FSMContext):
    """command /newsletter

    :param msg: message sent by the user
    :param state: inherit fsm

    return:the output is several coroutines
"""
    logger.debug("command newsletter")
    # * admin id check
    if msg.from_user.id == int(ADMIN):
        await msg.answer("напишите текст, для рассылки")
        await state.set_state(Newsletter.text)
    else:
        await msg.answer("вы не являетесь админом")


@logger.catch()
@router.message(Newsletter.text)
async def process_text(msg: Message, state: FSMContext):
    """Handling the state when the admin entered text

     :param msg: message sent by the user
     :param state: inherit fsm

     return:the output is several coroutines
 """
    await state.update_data(text=msg.text)
    # * answer that text accepted
    # * answer with inline keyboard for decline new state
    await msg.answer(
        "текст принят.\nскиньте фото",
        reply_markup=without_photo()
    )
    await state.set_state(Newsletter.photo)


@logger.catch()
@router.callback_query(AdminWithoutPhotoCallback.filter())
async def process_without_photo(query: CallbackQuery, state: FSMContext):
    """working out a callback for a post without a photo

    :param query: this object represents an incoming callback query from a callback button
    :param state: inherit fsm
    :return: the output is several coroutines
    """
    data = await state.get_data()
    # * send the newsletter for accepting
    await query.message.answer(
        f"{data['text']}"
        f"\n\n<i>потвердите текст</i>",
        reply_markup=accept_newsletter()
    )


@logger.catch()
@router.message(Newsletter.photo)
async def process_photo(msg: Message, state: FSMContext):
    """ receive photo from admin

    :param msg: message sent by the user
    :param state: inherit fsm
    :return: the output is several coroutines
    """
    await state.update_data(photo=msg.photo[0].file_id)
    data = await state.get_data()
    # * send the newsletter for accepting
    await msg.answer_photo(
        photo=data["photo"],
        caption=f"{data['text']}\n\n<i>потвердите текст</i>",
        reply_markup=accept_newsletter()
    )


@logger.catch()
@router.callback_query(AdminAcceptCallback.filter())
async def final_stage(
        query: CallbackQuery,
        callback_data: AdminAcceptCallback,
        state: FSMContext
):
    """Admin must decide to start the mailing or cancel it

    :param query: this object represents an incoming callback query from a callback button
    :param callback_data: the callback with some information
    :param state: inherit fsm
    """
    if callback_data.act == "ACCEPT":
        data = await state.get_data()
        logger.debug(data)
        # * start mailing
        await start_newsletter(data=data)
        await state.clear()
    elif callback_data.act == "DECLINE":
        await state.clear()
        await query.message.answer("рассылка отменина")


@logger.catch()
async def start_newsletter(data):
    """ function for mailing

    :param data: the post for mailing
    :return: the output is several coroutines
    """
    logger.debug("mailing has started")
    await bot.send_message(chat_id=ADMIN, text="рассылка началась")
    # * get all users id
    users_id = await crud.user.select_all_users_id()
    max_send = 0
    # * checking if the post has a photo
    if data.get("photo"):
        for i in range(len(users_id) - 1):
            # * every five message sleep 5 sec to avoid ban
            if max_send != 5:
                try:
                    await bot.send_photo(
                        chat_id=users_id[0][i],
                        photo=data["photo"],
                        caption=data["text"]
                    )
                    max_send += 1
                except Exception:
                    continue
            else:
                await asyncio.sleep(1)
    else:
        for i in range(len(users_id)):
            if max_send != 5:
                try:
                    await bot.send_message(
                        chat_id=users_id[0][i],
                        text=data["text"]
                    )
                    max_send += 1
                except Exception:
                    continue
            else:
                await asyncio.sleep(1)
    await bot.send_message(chat_id=ADMIN, text="рассылка закончина")
