import logging
import argparse

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import executor
from Bio import Entrez


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--telegram_api_token', required=True, help='Telegram API Token')
    parser.add_argument('--pubmed_api_email', required=True, help='PubMed API Email')
    parser.add_argument('--pubmed_api_key', required=True, help='PubMed API Key')
    return parser.parse_args()


args = parse_args()

bot = Bot(token=args.telegram_api_token)
dp = Dispatcher(bot, storage=MemoryStorage())

Entrez.email = args.pubmed_api_email
Entrez.api_key = args.pubmed_api_key


class PubmedSearchStates(StatesGroup):
    waiting_for_query = State()


MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton("/pubmed_search")
MARKUP.add(button)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply(
        "Привет! Я могу найти статьи на PubMed по Вашему запросу",
        reply_markup=MARKUP,
    )


@dp.message_handler(state=PubmedSearchStates.waiting_for_query)
async def process_query(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["query"] = message.text
        await message.reply("Поиск...")

        handle = Entrez.esearch(
            db="pubmed", term=data["query"], retmax=3, sort="relevance"
        )
        record = Entrez.read(handle)
        handle.close()

        if int(record["Count"]) == 0:
            await bot.send_message(
                message.from_user.id,
                "Сформулируйте запрос конкретнее, используйте ключевые слова",
            )

        else:
            for i in range(len(record["IdList"])):
                handle = Entrez.esummary(
                    db="pubmed", id=record["IdList"][i], retmode="xml"
                )
                summaries = Entrez.read(handle)
                handle.close()
                for summary in summaries:
                    pmid = summary["Id"]
                    title = summary["Title"]
                    handle = Entrez.efetch(
                        db="pubmed", id=pmid, rettype="abstract", retmode="text"
                    )
                    abstract = handle.read()
                    await bot.send_message(
                        message.from_user.id,
                        f"Статья: {title}\n"
                        f"Link: https://pubmed.ncbi.nlm.nih.gov/{pmid}/\n\n\n"
                        f"Abstract: {abstract}",
                        reply_markup=MARKUP,
                    )

            await state.finish()


@dp.message_handler(commands=["pubmed_search"])
async def pubmed_search_command(message: types.Message):
    try:
        await message.reply(
            "Отправьте ключевые слова для поиска статей в базе PubMed:"
        )
        await PubmedSearchStates.waiting_for_query.set()
    except Exception as e:
        logging.exception(e)


if __name__ == "__main__":
    executor.start_polling(dp)
