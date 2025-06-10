from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv(8014228833: AAF-Z3bWg9kcgCwJpwzERrXtsch2AnF0EKA)

ratings_db = {}

def convert_rating(score):
    stars = ["✴️", "⭐️", "⭐️✴️", "⭐️⭐️", "⭐️⭐️✴️", "⭐️⭐️⭐️", "⭐️⭐️⭐️✴️", "⭐️⭐️⭐️⭐️", "⭐️⭐️⭐️⭐️✴️", "⭐️⭐️⭐️⭐️⭐️"]
    labels = ["Unwatchable", "Terrible", "Bad", "Poor", "Weak", "Average", "Good", "Very Good", "Excellent", "Masterpiece"]
    return {
        "out_of_5": round(score / 2, 1),
        "stars": stars[score - 1],
        "percent": score * 10,
        "label": labels[score - 1]
    }

async def rate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        movie = context.args[0]
        score_text = context.args[1]
        comment = " ".join(context.args[2:]) if len(context.args) > 2 else ""

        if "/10" not in score_text:
            await update.message.reply_text("⚠️ Use format: /rate MovieName 8/10 \"optional comment\"")
            return

        score = int(score_text.replace("/10", ""))
        if not (1 <= score <= 10):
            await update.message.reply_text("⚠️ Rating must be between 1 and 10.")
            return

        conv = convert_rating(score)
        ratings_db[movie.lower()] = {
            "score": score,
            "comment": comment,
            **conv
        }

        reply = f"🎬 {movie}\n🔢 Rating: {score}/10\n🌟 {conv['out_of_5']}/5 → {conv['stars']}\n📊 {conv['percent']}%\n📌 Category: {conv['label']}"
        if comment:
            reply += f"\n💬 My take: {comment}"

        await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

async def myratings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not ratings_db:
        await update.message.reply_text("📭 No ratings yet.")
        return

    msg = "🗂 Your Ratings:\n"
    for title, data in ratings_db.items():
        msg += f"• 🎬 {title.title()} – {data['score']}/10 – {data['stars']} – {data['label']}\n"
    await update.message.reply_text(msg)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("rate", rate))
app.add_handler(CommandHandler("myratings", myratings))

print("✅ Bot is running...")
app.run_polling()

