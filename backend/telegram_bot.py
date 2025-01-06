from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User ,Competition
from . import models 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TELEGRAM_TOKEN = "7821421257:AAHoEA1EBjIqCDBNoMhdiQKFrNaPSh88ZXg"

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def check_and_award_badges(user, context):
    db = next(get_db())
    if user.points >= 10 and "10_points_badge" not in user.badges:
        user.badges += "10_points_badge,"
        db.commit()
        await context.bot.send_message(chat_id=user.telegram_id, text="Поздравляем! Вы получили бейдж за 10 баллов!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Открыть приложение", web_app={"url": "https://yourdomain.com/webapp"})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Нажмите кнопку, чтобы открыть приложение:", reply_markup=reply_markup)

async def create_competition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Использование: /create_competition <тип спорта> <название события>")
        return
    sport_type = args[0]
    event_name = " ".join(args[1:])
    db = next(get_db())
    competition = models.Competition(sport_type=sport_type, event_name=event_name)
    db.add(competition)
    db.commit()
    await update.message.reply_text(f"Соревнование '{event_name}' создано!")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Использование: /predict <id соревнования> <прогноз>")
        return
    competition_id = int(args[0])
    predicted_result = " ".join(args[1:])
    user = update.message.from_user
    db = next(get_db())

    # Проверяем, существует ли соревнование
    competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
    if not competition:
        await update.message.reply_text("Соревнование не найдено.")
        return

    # Проверяем, зарегистрирован ли пользователь
    db_user = db.query(models.User).filter(models.User.telegram_id == user.id).first()
    if not db_user:
        await update.message.reply_text("Сначала зарегистрируйтесь с помощью команды /start.")
        return

    # Создаем прогноз
    prediction = models.Prediction(
        user_id=db_user.id,
        competition_id=competition_id,
        predicted_result=predicted_result
    )
    db.add(prediction)
    db.commit()
    await update.message.reply_text(f"Ваш прогноз на соревнование '{competition.event_name}' сохранен!")

async def finish_competition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Использование: /finish_competition <id соревнования> <результат>")
        return
    competition_id = int(args[0])
    actual_result = " ".join(args[1:])
    db = next(get_db())

    # Находим соревнование
    competition = db.query(models.Competition).filter(models.Competition.id == competition_id).first()
    if not competition:
        await update.message.reply_text("Соревнование не найдено.")
        return

    # Обновляем результат соревнования
    competition.is_finished = True
    db.commit()

    # Находим все прогнозы для этого соревнования
    predictions = db.query(models.Prediction).filter(models.Prediction.competition_id == competition_id).all()
    for prediction in predictions:
        if prediction.predicted_result == actual_result:
            prediction.is_correct = True
            user = prediction.user
            user.points += 1  # Начисляем балл за правильный прогноз
    db.commit()

    await update.message.reply_text(f"Соревнование '{competition.event_name}' завершено. Баллы начислены!")
    await check_and_award_badges(user, context)

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    db = next(get_db())
    db_user = db.query(models.User).filter(models.User.telegram_id == user.id).first()
    if db_user:
        await update.message.reply_text(f"Профиль: {db_user.username}, Бейджи: {db_user.badges}, Баллы: {db_user.points}")
    else:
        await update.message.reply_text("Пользователь не найден.")

# Запуск бота
def run_bot():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).read_timeout(30).write_timeout(30).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", profile))
    app.add_handler(CommandHandler("create_competition", create_competition))
    app.add_handler(CommandHandler("predict", predict))
    app.add_handler(CommandHandler("finish_competition", finish_competition))
    app.run_polling()