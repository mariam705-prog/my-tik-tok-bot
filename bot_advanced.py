import logging
import os
from config import (
    BOT_TOKEN, DOWNLOAD_FOLDER, MAX_FILE_SIZE_MB, 
    YDL_OPTIONS, DEBUG, MESSAGES
)
import yt_dlp
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ChatAction

# تفعيل logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG if DEBUG else logging.INFO
)
logger = logging.getLogger(__name__)

# إنشاء مجلد التحميل إذا لم يكن موجوداً
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)
    logger.info(f"تم إنشاء مجلد: {DOWNLOAD_FOLDER}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /start"""
    await update.message.reply_text(MESSAGES['start'])
    logger.info(f"المستخدم {update.effective_user.id} استخدم /start")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج أمر /help"""
    await update.message.reply_text(MESSAGES['help'], parse_mode='Markdown')
    logger.info(f"المستخدم {update.effective_user.id} استخدم /help")

async def download_tiktok_video(url: str) -> str:
    """تحميل فيديو TikTok باستخدام yt-dlp"""
    try:
        ydl_opts = {
            **YDL_OPTIONS,
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logger.info(f"جاري تحميل الفيديو من: {url}")
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            logger.info(f"تم التحميل بنجاح: {video_path}")
            return video_path
    
    except Exception as e:
        logger.error(f"خطأ في التحميل: {str(e)}")
        raise

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج الرسائل التي تحتوي على روابط"""
    message_text = update.message.text
    user_id = update.effective_user.id
    
    logger.info(f"رسالة من {user_id}: {message_text}")
    
    # التحقق من وجود رابط TikTok
    tiktok_domains = ["tiktok.com", "vm.tiktok.com", "vt.tiktok.com"]
    is_valid_url = any(domain in message_text for domain in tiktok_domains)
    
    if not is_valid_url:
        await update.message.reply_text(MESSAGES['invalid_url'])
        return
    
    try:
        # إظهار حالة "جاري الكتابة"
        await update.message.chat.send_action(ChatAction.TYPING)
        await update.message.reply_text(MESSAGES['downloading'])
        
        # تحميل الفيديو
        video_path = await download_tiktok_video(message_text)
        
        # التحقق من حجم الملف
        file_size = os.path.getsize(video_path)
        file_size_mb = file_size / (1024 * 1024)
        
        if file_size_mb > MAX_FILE_SIZE_MB:
            os.remove(video_path)
            logger.warning(f"الملف أكبر من الحد المسموح به: {file_size_mb:.2f} MB")
            await update.message.reply_text(
                MESSAGES['file_too_large'].format(file_size_mb, MAX_FILE_SIZE_MB)
            )
            return
        
        # إرسال الفيديو
        logger.info(f"جاري إرسال الفيديو للمستخدم {user_id}")
        await update.message.chat.send_action(ChatAction.UPLOAD_VIDEO)
        
        with open(video_path, 'rb') as video_file:
            await update.message.reply_video(
                video=video_file,
                caption=MESSAGES['success']
            )
        
        # حذف الملف بعد الإرسال
        os.remove(video_path)
        logger.info(f"تم حذف الملف: {video_path}")
    
    except Exception as e:
        error_message = str(e)
        logger.error(f"خطأ: {error_message}")
        
        # رسالة خطأ مفصلة
        if "unable to extract" in error_message.lower():
            await update.message.reply_text(MESSAGES['error_extraction'])
        elif "http" in error_message.lower():
            await update.message.reply_text(MESSAGES['error_connection'])
        else:
            await update.message.reply_text(
                MESSAGES['error_general'].format(error_message[:100])
            )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """معالج الأخطاء العامة"""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    """دالة رئيسية لتشغيل البوت"""
    logger.info("🚀 جاري بدء تشغيل البوت...")
    
    # إنشاء التطبيق
    application = Application.builder().token(BOT_TOKEN).build()

    # إضافة معالجات الأوامر
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # معالج الرسائل النصية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # معالج الأخطاء
    application.add_error_handler(error_handler)

    # تشغيل البوت
    print("🚀 البوت قيد التشغيل...")
    logger.info("البوت قيد التشغيل والانتظار للرسائل...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
