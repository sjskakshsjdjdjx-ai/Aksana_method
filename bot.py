import asyncio
import logging
import os
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, Message

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

FAQ_TEXT = """<b>"Какие настройки графики сильнее всего повышают FPS в Rust?"</b>
Снижение качества теней (Shadow Quality), дальности прорисовки (Draw Distance, обычно до 1500–2000), качества воды и отключённые эффекты вроде Motion Blur, Depth of Field и Bloom.

<b>"Зачем ставить Draw Distance (дальность прорисовки) в районе 1500–2000?"</b>
Чтобы игра не тратила ресурсы процессора и видеокарты на отрисовку удалённых объектов и баз, при этом оставляя достаточный обзор для стрельбы и навигации.

<b>"Что делает команда gc.buffer и какое значение выбрать?"</b>
Она увеличивает буфер сборки мусора Unity, чтобы реже происходили микрофризы при очистке памяти; при 16 ГБ ОЗУ часто ставят 2048 или 4096 (в байтах/мегабайтах в зависимости от актуальной версии клиента, проверяйте в консоли через gc.buffer).

<b>"Почему Rust критично нужен SSD и достаточно оперативной памяти?"</b>
Игра постоянно подгружает карту, объекты и текстуры в реальном времени: с HDD появляются долгие загрузки и жёсткие статтеры, а при нехватке ОЗУ (меньше 16–32 ГБ) система начинает активно использовать файл подкачки.

<b>"Зачем отключать Motion Blur, Depth of Field, Bloom и VSync?"</b>
Они добавляют визуальные эффекты или задержку ввода ценой лишней нагрузки на GPU и инпут-лага, а в соревновательном шутере важнее чёткая картинка и минимальная задержка.

<b>"Как сохранить консольные команды, чтобы не вводить их каждый раз?"</b>
Прописать нужные команды в файл конфигурации client.cfg (в папке cfg внутри директории Rust) или в параметры запуска / автозагрузку конфига.

<b>"Влияет ли частота опроса мыши (Polling Rate) на фризы и FPS?"</b>
Сверхвысокая частота опроса (4000–8000 Гц) может нагружать процессор и вызывать просадки FPS на слабых или загруженных CPU; для стабильности часто достаточно 1000–2000 Гц.

<b>"Зачем включать XMP / EXPO в BIOS и режим производительности в Windows?"</b>
XMP/EXPO запускает оперативную память на заявленной высокой частоте вместо базовой медленной, а профиль производительности Windows снижает энергосберегающие задержки CPU.

<b>"Стоит ли снижать Render Scale ниже 1.0 для повышения FPS?"</b>
Только как крайний вариант, если видеокарта совсем не вывозит: картинка становится заметно мыльнее, а дальних противников хуже видно.

<b>"Почему FPS падает рядом с огромными базами и во время рейдов?"</b>
Из-за резкого роста числа сущностей, строительных блоков, источников света, частиц взрывов и расчётов физики/сети на стороне клиента и сервера."""


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


async def main() -> None:
    if not BOT_TOKEN:
        raise SystemExit("Задайте токен: переменная окружения BOT_TOKEN")
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
