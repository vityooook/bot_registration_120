from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loguru import logger

# import main menu reply keyboard
from keyboard.default.reply_menu import menu_reply
# import requests to database
from database import crud


router = Router()


class UserInfo(StatesGroup):
    user_group = State()


@logger.catch()
@router.message(CommandStart())
async def cmd_start_handler(msg: Message, state: FSMContext):
    """Handler for the /start command.

    Responds to the user based on whether their ID is verified or not.

    Args:
        msg (Message): Message sent by the user.
        state (FSMContext): FSM context.

    """
    logger.info("command /start")
    await msg.answer("привествую тебя брат")
