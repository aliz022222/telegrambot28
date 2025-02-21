from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import os

# ذخیره امتیازات کاربران
user_scores = {}
admin_ids = [1064474542]  # آیدی تلگرام مدیران

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # دریافت توکن از متغیر محیطی
if not TOKEN:
    raise ValueError("توکن ربات تنظیم نشده است. لطفا متغیر محیطی TELEGRAM_BOT_TOKEN را مقداردهی کنید.")

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("سلام! به ربات امتیازدهی خوش آمدید. برای اضافه کردن امتیاز از دستور /add استفاده کنید.")

async def add_score(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("شما اجازه استفاده از این دستور را ندارید.")
        return
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("لطفا یوزرنیم و امتیاز را وارد کنید. مثال: /add @user1 5")
            return

        username = args[0]
        score = int(args[1])

        if username not in user_scores:
            user_scores[username] = 0

        user_scores[username] += score

        await update.message.reply_text(f"به {username} تعداد {score} امتیاز اضافه شد. مجموع امتیازات: {user_scores[username]}")
    except ValueError:
        await update.message.reply_text("لطفا امتیاز را به صورت عدد وارد کنید.")

async def remove_score(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("شما اجازه استفاده از این دستور را ندارید.")
        return
    try:
        args = context.args
        if len(args) < 2:
            await update.message.reply_text("لطفا یوزرنیم و امتیاز را وارد کنید. مثال: /remove @user1 5")
            return

        username = args[0]
        score = int(args[1])

        if username not in user_scores:
            user_scores[username] = 0

        user_scores[username] -= score

        await update.message.reply_text(f"از {username} تعداد {score} امتیاز کم شد. مجموع امتیازات: {user_scores[username]}")
    except ValueError:
        await update.message.reply_text("لطفا امتیاز را به صورت عدد وارد کنید.")

async def show_scores(update: Update, context: CallbackContext) -> None:
    if not user_scores:
        await update.message.reply_text("هنوز امتیازی ثبت نشده است.")
        return

    score_text = "جدول امتیازات کاربران:\n"
    for user, score in sorted(user_scores.items(), key=lambda item: item[1], reverse=True):
        score_text += f"{user}: {score} امتیاز\n"

    await update.message.reply_text(score_text)

async def reset_scores(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("شما اجازه استفاده از این دستور را ندارید.")
        return
    user_scores.clear()
    await update.message.reply_text("تمام امتیازات پاک شدند.")

async def restart(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id not in admin_ids:
        await update.message.reply_text("شما اجازه استفاده از این دستور را ندارید.")
        return
    global user_scores
    user_scores = {}
    await update.message.reply_text("ربات ریستارت شد و امتیازات پاک شدند.")

async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "/start - شروع ربات\n"
        "/add @یوزرنیم امتیاز - اضافه کردن امتیاز\n"
        "/remove @یوزرنیم امتیاز - کم کردن امتیاز\n"
        "/scores - نمایش جدول امتیازات\n"
        "/reset - پاک کردن تمام امتیازات\n"
        "/restart - ریستارت کردن ربات\n"
    )
    await update.message.reply_text(help_text)

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add_score))
app.add_handler(CommandHandler("remove", remove_score))
app.add_handler(CommandHandler("scores", show_scores))
app.add_handler(CommandHandler("reset", reset_scores))
app.add_handler(CommandHandler("restart", restart))
app.add_handler(CommandHandler("help", help_command))

if __name__ == "__main__":
    app.run_polling()