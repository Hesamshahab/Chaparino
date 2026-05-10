class ChaparinoTemplates:
    # متغیرهای ثابت برای تمام پیام‌ها
    GLOBAL_CONFIG = {
        "company_name": "چاپارینو",
        "support_phone": "۰۲۱-۱۲۳۴۵۶",
    }

    # قالب‌های تعریف شده
    _TEMPLATES = {
        "welcome": "سلام {name} عزیز، به {company_name} خوش آمدید.",
        "otp": "کد تایید شما: {code}\n{company_name}",
        "announcement": "همکار گرامی {name}، جلسه در ساعت {time} برگزار می‌شود.",
    }

    @classmethod
    def render(cls, template_key: str, **kwargs):
        template_text = cls._TEMPLATES.get(template_key)
        if not template_text:
            raise ValueError(f"Template '{template_key}' not found.")
        
        # ترکیب تنظیمات کلی با متغیرهای ورودی کاربر
        full_data = {**cls.GLOBAL_CONFIG, **kwargs}
        return template_text.format(**full_data)