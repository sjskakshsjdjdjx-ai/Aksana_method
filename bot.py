import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, LinkPreviewOptions, InlineKeyboardButton, InlineKeyboardMarkup, Message

# Токен берём из переменной окружения BOT_TOKEN (не храните токен в коде!)
BOT_TOKEN = os.getenv("BOT_TOKEN")

URL_BUY = "https://t.me/aksana_lok"
URL_REVIEWS = "https://t.me/aksana_metod/7"
URL_SUPPORT = "https://t.me/aksana_lok"

WELCOME_TEXT = (
    "Добро пожаловать в Aksana Method! ⚡️\n"
    "Помогаем выжать максимум FPS, убрать фризы и input lag в играх — "
    "без потери стабильности системы"
)
LOGO_PATH = Path(__file__).parent / "logo.png"

FAQ_TEXT = """<b>"Где купить оптимизацию?"</b>
Оформить покупку можно напрямую в личных сообщениях: @aksana_lok. Напишите туда, чтобы выбрать подходящий тариф и получить доступ.

<b>"Сколько стоит оптимизация?"</b>
Актуальные цены и список доступных тарифов можно узнать в личных сообщениях у @aksana_lok.

<b>"Как происходит процесс оптимизации?"</b>
После оплаты в личных сообщениях (@aksana_lok) вы получите подробную инструкцию, необходимые файлы или доступ к настройке специалистом.

<b>"Безопасно ли это для ПК и аккаунтов?"</b>
Да, используются только проверенные методы настройки системы без вмешательства в файлы игр. Никакого риска получить бан или повредить Windows нет.

<b>"Насколько сильно вырастет FPS и снизится инпут-лаг?"</b>
Результат зависит от вашего железа, но в среднем FPS становится значительно стабильнее, пропадают фризы и заметно уменьшается задержка ввода.

<b>"Подойдет ли оптимизация для слабого ПК или ноутбука?"</b>
Да, настройка эффективна на любых конфигурациях: на слабых системах она убирает фризы и освобождает ресурсы, а на мощных — раскрывает весь потенциал железа и убирает инпут-лаг.

<b>"Нужно ли переустанавливать Windows перед покупкой?"</b>
Не обязательно, но для достижения максимального результата рекомендуется чистая система. Все детали можно уточнить перед покупкой у @aksana_lok.

<b>"Какие способы оплаты доступны?"</b>
Доступны переводы на карту и другие популярные способы. Уточнить реквизиты можно в личных сообщениях: @aksana_lok.

<b>"Есть ли отзывы от других покупателей?"</b>
Да, примеры работ, тесты до/после и отзывы клиентов можно посмотреть в основном канале или запросить напрямую у @aksana_lok.

<b>"Что делать, если после настройки возникнут вопросы?"</b>
После покупки вы получаете поддержку. Если что-то пойдет не так или потребуется помощь, всегда можно написать @aksana_lok."""


LEGAL_TEXT = (
    "Самозанятый Кирсанов Никита Андреевич (плательщик НПД)\n"
    "ИНН: 762706749201\n"
    "E-mail: n48417606@gmail.com | Telegram: @aksana_lok\n"
    '<a href="https://www.consultant.ru/document/cons_doc_LAW_5142/892c4b89172aef07157d5d6c0e5dcde6e37b3a83/">Публичная оферта</a>\n'
    '<a href="https://02.rkn.gov.ru/directions/p4172/p18331/">Политика обработки персональных данных</a>'
)


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Купить", url=URL_BUY),
                InlineKeyboardButton(text="Отзывы", url=URL_REVIEWS),
            ],
            [
                InlineKeyboardButton(text="Поддержка", url=URL_SUPPORT),
                InlineKeyboardButton(text="Вопросы", callback_data="faq"),
            ],
            [
                InlineKeyboardButton(text="Юридическая информация", callback_data="legal"),
            ],
        ]
    )


dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer_photo(
        FSInputFile(LOGO_PATH), caption=WELCOME_TEXT, reply_markup=main_menu()
    )


@dp.callback_query(F.data == "faq")
async def show_faq(callback: CallbackQuery) -> None:
    await callback.message.answer(FAQ_TEXT, reply_markup=main_menu())
    await callback.answer()


@dp.callback_query(F.data == "legal")
async def show_legal(callback: CallbackQuery) -> None:
    await callback.message.answer(
        LEGAL_TEXT,
        reply_markup=main_menu(),
        link_preview_options=LinkPreviewOptions(is_disabled=True),
    )
    await callback.answer()


async def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("Задайте токен: переменная окружения BOT_TOKEN")
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
