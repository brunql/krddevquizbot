#!/usr/bin/env python3
import logging
import os
import random
from datetime import datetime

from telegram import Update, Poll, User
from telegram.constants import ParseMode
from telegram.ext import Application, PollHandler, PollAnswerHandler, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.helpers import escape_markdown

from krddevquizbot.questions import QUESTIONS


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# DB
USERS_STATS = {}
POLLS = {}

ADMINS = ["brunql", "darkdef_pr"]

POLL_OPEN_PERIOD_SECONDS = 10

CURRENT_QUESTION_INDEX = 0
CURRENT_QUESTION_FIRST_RIGHT_ANSWER_USER_ID = 0
CURRENT_MEM_INDEX = 0
MEMS_DIR_PATH = "mems"

SKIPMESSAGES = [
  "Слиться!",
  "Спиться!",
  "Ладно я сдаюсь...",
  "Это же неправильный вопрос!",
  "Вот же правильный ответ!",
  "Галактика в опасносте!",
  "Тыц!",
  "Давай ты сможешь!",
  "Думать лень",
  "Подержите мое пиво!",
]


def get_random_skip_message():
  return random.choice(SKIPMESSAGES)


def is_admin(update: Update) -> bool:
  return update.effective_user.username in ADMINS


def get_name(user_id: int) -> str:
  user = USERS_STATS.get(user_id, {}).get('user')
  return user.name if user else ""


def get_user_score(user_id: int) -> int:
  return USERS_STATS.get(user_id, {}).get('score', 0)


def fmt_score(score: float) -> str:
  return f"{score:.1f}"


def fmt_user_score(user_id: int) -> int:
  return fmt_score(get_user_score(user_id))


def init_user(update: Update):
  user = update.effective_user
  if user.id not in USERS_STATS:
    USERS_STATS[user.id] = {'user': user, 'correct': 0, 'fail': 0, 'score': 0}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  init_user(update)

  user = update.effective_user

  await update.message.reply_text(
    f"""Добро пожаловать в клуб! 👍
    
🔥 Ожидаем подключения всех участников и стартуем! 😎 

Первое правило клуба - правильный ответ всегда скрыт, подглядывать нет смысла - думай сам! 😈

Второе правило клуба - для телеграмма правильный ответ всегда первый, но мы то знаем, что это не так! 🤓

Третье правило клуба - ответил на вопрос - выпил! 🍺

Желаем удачи! 🎃 🤝
""")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  init_user(update)
  await update.message.reply_text("🙈 Помощи не будет можно даже не надеяться. 🤪")  


async def broadcast_message(text: str, context: ContextTypes.DEFAULT_TYPE):
  for user_id in USERS_STATS.keys():
    try:
      await context.bot.send_message(chat_id=user_id, text=f"🐳 broadcast: {text}")
    except Exception as ex:
      logging.error(f"broadcast_message: send_message fail: {ex} name={get_name(user_id)}")


async def broadcast_next_mem(context: ContextTypes.DEFAULT_TYPE):
  global CURRENT_MEM_INDEX
  
  mems = os.listdir(MEMS_DIR_PATH)
  if len(mems) == 0:
    logging.error("broadcast_next_mem: no mems found")
    return
  
  if CURRENT_MEM_INDEX >= len(mems):
    CURRENT_MEM_INDEX = 0

  mem_filename = mems[CURRENT_MEM_INDEX]

  CURRENT_MEM_INDEX += 1

  for user_id in USERS_STATS.keys():
    try:
      await context.bot.send_photo(
        chat_id=user_id, 
        photo=open(os.path.join(MEMS_DIR_PATH, mem_filename), 'rb'), 
        caption="🐳 broadcast: #include <image.h>"
      )
    except Exception as ex:
      logging.error(f"broadcast_next_mem: send_photo fail: {ex} name={get_name(user_id)}")


async def admin_start_quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:  
  global CURRENT_QUESTION_INDEX
 
  init_user(update)

  if not is_admin(update):
    await update.message.reply_text("😭 Запуск доступен только админам.")
    return
  
  CURRENT_QUESTION_INDEX = 0
  await broadcast_message("Приготовьтесь мы начинаем! 🔥", context)


async def admin_next_question_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  global CURRENT_QUESTION_INDEX
  global CURRENT_QUESTION_FIRST_RIGHT_ANSWER_USER_ID

  CURRENT_QUESTION_FIRST_RIGHT_ANSWER_USER_ID = 0

  init_user(update)

  if not is_admin(update):
    await update.message.reply_text("💊 Ваша заявка принята. Ожидайте на линии.")
    return

  if CURRENT_QUESTION_INDEX >= len(QUESTIONS):
    await broadcast_message("Ура! 🍾 Quiz завершен! 🦄", context)
    await update.message.reply_text("Посмотреть статистику: /admin_stats")
    return

  question = QUESTIONS[CURRENT_QUESTION_INDEX]

  question['answers_count'] = 0
  
  for user_id in USERS_STATS.keys():
    try:
      msg = await context.bot.send_poll(
        user_id, 
        question=f"{CURRENT_QUESTION_INDEX+1} / {len(QUESTIONS)}. {question['question']}", 
        options=[get_random_skip_message()] + question["options"], 
        type=Poll.QUIZ, 
        correct_option_id=0, # always set zero
        protect_content=True,
        open_period=POLL_OPEN_PERIOD_SECONDS,
      )

      POLLS[msg.poll.id] = {"user_id": user_id, "message_id": msg.id, "start_time": datetime.now()}

    except Exception as ex:
      logging.error(f"admin_next_question_command: broadcast send_poll fail: {ex} name={get_name(user_id)}")

  CURRENT_QUESTION_INDEX += 1

  context.job_queue.run_once(show_first_right_answered_user, POLL_OPEN_PERIOD_SECONDS + 2)


async def show_first_right_answered_user(context: ContextTypes.DEFAULT_TYPE):
  prefix = [
      "Оппа! {name} уже ответил! 🔥", 
      "У {name} самая быстрая 🦾 лапка на диком востоке!", 
      "Так держать username! request_id={name} traceback=not found", 
      "Кажется {name} нас вломал, ну и ладно... 🍺 \n# docker kill krddevquizbot", 
      "А {name} то молодец! ⚡️", 
      "{name}, случайно нажал? 🧐",
      "Уважаемый, {name}! Ваш запрос находится в обработке, ближайший освободившийся робот вам не ответит. 🙈",
      "{name}, права купил? 😱 Пристегнитесь тут взлетают! 🛫",
      "Думается мне что у {name} есть все шансы на победу ведь это - 🤖",
      "{name}, освободился? С тебя мемасик! 👻",
      "{name}, псс! 🐍 бро, давай всем скажем, что этот бот написан на PHP?",
    ]

  msg = random.choice(prefix)
  user_id = CURRENT_QUESTION_FIRST_RIGHT_ANSWER_USER_ID
  if user_id:
    text = msg.format(name=get_name(user_id))    
    await broadcast_message(text, context)
    await broadcast_next_mem(context)
  else:
    await broadcast_message("🤖 К великому сожалению никто правильно не ответил. Мемов не будет.", context)


async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  global CURRENT_QUESTION_FIRST_RIGHT_ANSWER_USER_ID

  if update.poll.is_closed:
    logging.error("receive_quiz_answer: poll.is_closed")
    return

  poll = POLLS.get(update.poll.id, {})
  user_id = poll.get("user_id", 0)
  if not user_id:
    logging.error(f"receive_quiz_answer: poll for user not found: name={get_name(user_id)}")
    return

    
  qs = list(filter(lambda x: x["question"] in update.poll.question, QUESTIONS))
  if len(qs) != 1:
    logging.error(f"receive_quiz_answer: question not found: {update.poll.question} name={get_name(user_id)}")
    return

  question = qs[0]

  # Found real correct option id
  correct_option_id = question["correct_option_number"]

  is_correct = update.poll.options[correct_option_id].voter_count > 0

  user_info = USERS_STATS.get(user_id, {})  
  if not user_info:
    logging.error(f"receive_quiz_answer: user in USERS_STATS not found: user_id={user_id}")
    return

  start_time = poll.get("start_time")
  if not start_time:
    logging.error(f"receive_quiz_answer: start_time in poll for user not found: name={get_name(user_id)}")
    return
  
  score = 100 - (datetime.now() - start_time).total_seconds()
  if score < 0:
    score = 1

  if is_correct:
    user_info['correct'] += 1
    USERS_STATS[user_id]['score'] += score
    
    if not CURRENT_QUESTION_FIRST_RIGHT_ANSWER_USER_ID:
      CURRENT_QUESTION_FIRST_RIGHT_ANSWER_USER_ID = user_id
  else:
    user_info['fail'] += 1

  await context.bot.delete_message(chat_id=user_id, message_id=poll.get("message_id", 0))

  if 'answers_count' not in question:
    question['answers_count'] = 0

  question['answers_count'] += 1
  

async def admin_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  init_user(update)
  
  if not is_admin(update):
    await update.message.reply_text("✍️ Арифметические операции выполняются вручную, это вам не джейсоны в крудах перекладывать! 🌭 😱")
    return

  users_sorted = USERS_STATS.values()
  users_sorted = list(sorted(users_sorted, key=lambda x: x["score"], reverse=True))
  users_sorted = list(sorted(users_sorted, key=lambda x: x["correct"], reverse=True))

  stats = ""
  for i, x in enumerate(users_sorted):
    if i == 0: stats += "🤓 "
    if i == 1: stats += "🔥 "
    if i == 2: stats += "👾 "
    stats += f"{i+1}: {x['user'].full_name} @{x['user'].username}  {x['correct']}👍  {x['fail']}👎 (score: {fmt_score(x['score'])})\n"

  msg = f"""
Победила дружба! 🤝 😇

{stats}

Для сброса статистики напишите от админа "Сбросить счетчики".

{CURRENT_QUESTION_INDEX } / {len(QUESTIONS)}
"""

  await update.message.reply_text(msg)


async def admin_answers_count_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  init_user(update)

  if not is_admin(update):
    await update.message.reply_text("🧾 У вас плохой кредитный скоринг, обратитесь в другой банк.")
    return
  
  msg = "```\n"

  for i, q in enumerate(QUESTIONS):
    msg += f"{str(i+1).zfill(2)}. Получено ответов: {q.get('answers_count', 0)}\n"

  msg += "```"

  await update.message.reply_text(msg, parse_mode=ParseMode.MARKDOWN_V2)


async def admin_next_mem(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  init_user(update)

  if not is_admin(update):
    await update.message.reply_text("No. Just no.")
    return

  await broadcast_next_mem(context)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if not is_admin(update):
    await update.message.reply_text("Линия занята! Зайдите позже 🤡")
    return
  
  if update.message.text == "Сбросить счетчики":
    for user_id in USERS_STATS.keys():
      USERS_STATS[user_id]["correct"] = 0
      USERS_STATS[user_id]["fail"] = 0

    await update.message.reply_text("Готово")

  global POLL_OPEN_PERIOD_SECONDS
  if update.message.text == "Переключить скорость":
    if POLL_OPEN_PERIOD_SECONDS == 10:
      POLL_OPEN_PERIOD_SECONDS = 60
    else:
      POLL_OPEN_PERIOD_SECONDS = 10

    await update.message.reply_text(f"Готово POLL_OPEN_PERIOD_SECONDS={POLL_OPEN_PERIOD_SECONDS}")


if __name__ == "__main__":
  BOT_TOKEN = os.environ.get("BOT_TOKEN")
  application = Application.builder().token(BOT_TOKEN).build()

  application.add_handler(CommandHandler("start", start_command))
  application.add_handler(CommandHandler("help", help_command))

  application.add_handler(CommandHandler("admin_start_quiz", admin_start_quiz_command))
  application.add_handler(CommandHandler("admin_next_question", admin_next_question_command))
  application.add_handler(CommandHandler("admin_stats", admin_stats_command))
  application.add_handler(CommandHandler("admin_answers_count", admin_answers_count_command))
  application.add_handler(CommandHandler("admin_next_mem", admin_next_mem))
  
  application.add_handler(MessageHandler(filters.TEXT, message_handler))

  application.add_handler(PollHandler(receive_quiz_answer))

  application.run_polling(allowed_updates=Update.ALL_TYPES)
