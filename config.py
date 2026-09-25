# 🔧 إعدادات بوت TikTok

# توكن البوت
BOT_TOKEN = "8846582392:AAH0mcwRLz16_vn4aL5-L57_zZHGQYeHSU8"

# مجلد تخزين الفيديوهات المحملة
DOWNLOAD_FOLDER = "downloads"

# الحد الأقصى لحجم الملف بالميجابايت
MAX_FILE_SIZE_MB = 50

# إعدادات التحميل
YDL_OPTIONS = {
    'format': 'best',
    'quiet': False,
    'no_warnings': False,
    'socket_timeout': 30,
    'retries': 3,
}

# تفعيل وضع التصحيح (Debug)
DEBUG = False

# رسائل البوت
MESSAGES = {
    'start': (
        "مرحباً! 👋\n\n"
        "أرسل لي رابط فيديو من TikTok وسأقوم بتحميله وإرساله لك.\n\n"
        "مثال: https://www.tiktok.com/@username/video/1234567890"
    ),
    'help': (
        "📋 **الأوامر المتاحة:**\n\n"
        "/start - عرض رسالة الترحيب\n"
        "/help - عرض المساعدة\n\n"
        "**الاستخدام:**\n"
        "أرسل رابط TikTok مباشرة وسيقوم البوت بتحميله وإرساله لك."
    ),
    'invalid_url': (
        "❌ الرجاء إرسال رابط TikTok صحيح.\n"
        "أمثلة على الروابط الصحيحة:\n"
        "• https://www.tiktok.com/@username/video/123456\n"
        "• https://vm.tiktok.com/abc123\n"
        "• https://vt.tiktok.com/abc123"
    ),
    'downloading': "⏳ جاري تحميل الفيديو، يرجى الانتظار...",
    'file_too_large': (
        "❌ حجم الفيديو كبير جداً ({:.2f} MB).\n"
        "الحد الأقصى المسموح به هو {} MB."
    ),
    'success': "✅ تم تحميل الفيديو بنجاح!",
    'error_extraction': (
        "❌ لم أتمكن من استخراج الفيديو من الرابط.\n"
        "تأكد من أن الرابط صحيح وأن الفيديو متاح."
    ),
    'error_connection': (
        "❌ خطأ في الاتصال بـ TikTok.\n"
        "يرجى المحاولة لاحقاً."
    ),
    'error_general': (
        "❌ حدث خطأ: {}\n"
        "يرجى المحاولة مع رابط آخر."
    ),
}
