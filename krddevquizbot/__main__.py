#!/usr/bin/env python3
import logging
import os
import random

from telegram import Update, Poll, User
from telegram.ext import Application, PollHandler, PollAnswerHandler, CommandHandler, ContextTypes, MessageHandler, filters

from krddevquizbot.questions import QUESTIONS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TOTAL_VOTER_COUNT = 3

# DB
USERS = {
  # 123: {'user': User(123, "First1", False, "Last1", "username1"), 'correct': 2, 'fail': 10},
  # 124: {'user': User(124, "First2", False, "Last2", "username2"), 'correct': 15, 'fail': 33},
}
POLLS = {}

ADMINS = ["brunql", "darkdef_pr"]

CURRENT_QUESTION_INDEX = 0
 
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
  user = USERS.get(user_id, {}).get('user')
  return user.name if user else ""


def init_user(update: Update):
  user = update.effective_user
  if user.id not in USERS:
    USERS[user.id] = {'user': user, 'correct': 0, 'fail': 0}


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  init_user(update)

  user = update.effective_user

  await update.message.reply_text(
    f"""Добро пожаловать в клуб! 👍
    
🔥 Ожидаем подключения всех участников и стартуем! 😎 

Первое правило клуба - правильный ответ всегда скрыт, подглядывать нет смысла - думай сам! 😈

Второе правило клуба - для телеграмма правильный ответ всегда первый, но мы то знаем, что это не так! 🤓

Третье правило клуба - ответил на вопрос - выпил! 🍾

Желаем удачи! 🎃 🤝

USERNAME={user.username}
FULLNAME={user.full_name}
""")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  init_user(update)
  await update.message.reply_text("🙈 Помощи не будет можно даже не надеяться. 🤪")


async def broadcast_message(text: str, context: ContextTypes.DEFAULT_TYPE):
  for user_id in USERS.keys():
    try:
      await context.bot.send_message(chat_id=user_id, text=f"🐳 broadcast: {text}")
    except Exception as ex:
      logging.error(f"admin_start_quiz_command: broadcast send_message fail: {ex} name={get_name(user_id)}")


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

  init_user(update)

  if not is_admin(update):
    await update.message.reply_text("💊 Ваша заявка принята. Ожидайте на линии.")
    return

  if CURRENT_QUESTION_INDEX >= len(QUESTIONS):
    await broadcast_message("Ура! 🍾 Quiz завершен! 🦄", context)
    await update.message.reply_text("Посмотреть статистику: /admin_stats")
    return

  question = QUESTIONS[CURRENT_QUESTION_INDEX]
  
  for user_id in USERS.keys():
    try:
      msg = await context.bot.send_poll(
        user_id, 
        question=f"{CURRENT_QUESTION_INDEX+1} / {len(QUESTIONS)}. {question['question']}", 
        options=[get_random_skip_message()] + question["options"], 
        type=Poll.QUIZ, 
        correct_option_id=0, # always set zero
        protect_content=True,
      )

      POLLS[msg.poll.id] = {"user_id": user_id, "message_id": msg.id}

    except Exception as ex:
      logging.error(f"admin_next_question_command: broadcast send_poll fail: {ex} name={get_name(user_id)}")

  CURRENT_QUESTION_INDEX += 1
   

async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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

  if is_correct:
    USERS[user_id]['correct'] += 1
  else:
    USERS[user_id]['fail'] += 1

  await context.bot.delete_message(chat_id=user_id, message_id=poll.get("message_id", 0))


async def admin_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  init_user(update)
  
  if not is_admin(update):
    await update.message.reply_text("✍️ Арифметические операции выполняются вручную, это вам не джейсоны в крудах перекладывать! 🌭 😱")
    return

  users_sorted = list(sorted(USERS.values(), key=lambda x: x["correct"], reverse=True))

  stats = ""
  for i, x in enumerate(users_sorted):
    if i == 0: stats += "🤓 "
    if i == 1: stats += "🔥 "
    if i == 2: stats += "👾 "
    stats += f"{i+1}: {x['user'].full_name} @{x['user'].username}  {x['correct']}👍  {x['fail']}👎\n"

  msg = f"""
Победила дружба! 🤝 😇

{stats}

Для сброса статистики напишите от админа "Сбросить счетчики".

{CURRENT_QUESTION_INDEX } / {len(QUESTIONS)}
"""

  await update.message.reply_text(msg)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  if not is_admin(update):
    await update.message.reply_text("Линия занята! Зайдите позже 🤡")
    return
  
  if update.message.text == "Сбросить счетчики":
    for user_id in USERS.keys():
      USERS[user_id]["correct"] = 0
      USERS[user_id]["fail"] = 0

  await update.message.reply_text("Готово")


if __name__ == "__main__":
  BOT_TOKEN = os.environ.get("BOT_TOKEN")
  application = Application.builder().token(BOT_TOKEN).build()

  application.add_handler(CommandHandler("start", start_command))
  application.add_handler(CommandHandler("help", help_command))

  application.add_handler(CommandHandler("admin_start_quiz", admin_start_quiz_command))
  application.add_handler(CommandHandler("admin_next_question", admin_next_question_command))
  application.add_handler(CommandHandler("admin_stats", admin_stats_command))
  
  application.add_handler(MessageHandler(filters.TEXT, message_handler))

  application.add_handler(PollHandler(receive_quiz_answer))

  application.run_polling(allowed_updates=Update.ALL_TYPES)
