<p align="center"> <img src="assets/logo.png" width="200" alt="Chaparino Logo"> </p>


## 🕊️ Chaparino (چاپارینو)

سرویس **Chaparino** یک سرویس سبک (Lightweight) و ماژولار برای مدیریت و ارسال پیام از طریق درگاه‌های **[SMS.ir](http://SMS.ir)** و پیام‌رسان **Bale** است. این پروژه تمرکز خود را بر سرعت ارسال، مدیریت قالب‌های پویا (Dynamic Templates) و قابلیت ارسال گروهی گذاشته است.


---

## ✨ ویژگی‌های کلیدی

ویژگی **Multi-Provider Support:** پشتیبانی همزمان از پنل پیامک [SMS.ir](http://SMS.ir) و پلتفرم بله (Bale API). 

ویژگی  **Dynamic Templating:** مدیریت متمرکز قالب‌ها با قابلیت جایگذاری متغیرهای دلخواه (مثل نام، کد تخفیف و ...). ویژگی\*   **Bulk Dispatch:** قابلیت ارسال گروهی پیام از طریق فایل‌های **CSV** و **Excel**.

 ویژگی **Phone Normalization:** هوشمندسازی شماره تماس‌ها (تبدیل خودکار به فرمت بین‌المللی برای بله و فرمت داخلی برای پیامک).

 ویژگی **FastAPI Powered:** ارائه API‌های استاندارد و سریع برای یکپارچگی با سایر پروژه‌ها.

ویژگی **Docker Ready:** آماده استقرار سریع در محیط‌های Containerized.


---

## 🛠 ساختار پروژه

```text
.
├── app
│   ├── main.py          # نقطه ورود API (FastAPI)
│   ├── core.py          # منطق اصلی ارسال و نرمال‌سازی
│   ├── templates.py     # مدیریت متغیرها و متن پیام‌ها
│   └── utils.py         # پردازش فایل‌های گروهی (CSV/Excel)
├── data                 # محل فایل‌های ورودی (اختیاری)
├── .env                 # تنظیمات حساس (Keys & Tokens)
└── Dockerfile           # فایل استقرار داکر
```


---

## 🚀 راه اندازی سریع

### ۱. تنظیمات محیطی

ابتدا فایل `.env` را در ریشه پروژه ایجاد کرده و مقادیر مربوطه را وارد کنید:

```env

BALE_ACCESS_KEY=your_access_key

BALE_BOT_ID=your_bot_id

SMS_IR_KEY=your_api_key

SMS_IR_LINE=your_line_number
```

### ۲. اجرا با Docker (پیشنهادی)

```bash

docker build -t chaparino .
docker run -p 8000:8000 --env-file .env chaparino
```

### ۳. اجرا به صورت محلی

```bash

pip install -r requirements.txt

uvicorn app.main:app --reload
```


---

## 📖 راهنمای استفاده از API

### ارسال تک پیام

برای ارسال پیام تکی، از Endpoint زیر استفاده کنید: `POST /send/single`

**پارامترهای ورودی (Form-Data):**

| پارامتر | نوع | توضیحات |
|:---|:---|:---|
| `provider` | string | مقدار `sms` یا `bale` |
| `template` | string | نام قالب (مثلاً `welcome` یا `otp`) |
| `phone` | string | شماره موبایل مقصد |
| `params` | JSON string | متغیرهای قالب: `{"name": "امیر"}` |

### ارسال گروهی (Bulk)

`POST /send/bulk`

فایل ارسالی (CSV/Excel) باید دارای ستونی به نام `phone` باشد. سایر ستون‌ها بر اساس نامشان در قالب پیام جایگذاری می‌شوند.


---

## 📝 مدیریت قالب‌ها (Templates)

قالب‌های خود را در فایل `app/templates.py` مدیریت کنید. شما می‌توانید از متغیرهای ثابت (مثل نام شرکت) و متغیرهای متغیر (پاس داده شده در لحظه ارسال) استفاده کنید:

```python
# نمونه قالب
"welcome": "سلام {name} عزیز، به {company_name} خوش آمدید."
```


---

## نمونه cURL:

```
curl -X 'POST' \ 
'http://localhost:8000/send/single' \
-H 'Content-Type: multipart/form-data' \
 -F 'provider=bale' \
 -F 'template=otp' \
 -F 'phone=0912XXXXXXX' \
 -F 'params={"code": "2829","company_name":"چاپارینو"}'
```

```
curl -X 'POST' \
  'http://localhost:8000/send/bulk' \
  -H 'Content-Type: multipart/form-data' \
  -F 'provider=sms' \
  -F 'template=announcement' \
  -F 'file=@/path/to/your/users.csv'
```

### 📂 فایل‌های نمونه جهت ارسال گروهی

سیستم به‌طور خودکار سرتیتر (Header) ستون‌ها را با متغیرهای قالب (Template Variables) تطبیق می‌دهد.

**مثال ۱ (اطلاع‌رسانی):**

| phone | name | time |
|:---|:---|:---|
| 09121111111 | علی علوی | ۱۰:۳۰ |
| 09122222222 | سارا ساروی | ۱۱:۰۰ |

**مثال ۲ (کد تایید - بدون صفر اول):**

| phone | code |
|:---|:---|
| 912XXXXXXX | 8713 |
| 936XXXXXXX | 9034 |

> **نکته:** Chaparino هوشمند است! اگر فایل شما به دلیل تنظیمات اکسل فاقد صفر اول در شماره تماس باشد، سیستم در زمان ارسال آن را بازیابی و اصلاح می‌کند.


---

## 🤝 مشارکت

اگر پیشنهادی برای اضافه کردن پروایدرهای جدید (مثل Telegram یا سرویس‌های دیگر) دارید، خوشحال می‌شویم Pull Request ارسال کنید یا در بخش Issues مطرح کنید.


---

**Chaparino** - *سریع مثل چاپار، مدرن مثل تکنولوژی.*


---

## LICENSE

MIT No Attribution

Copyright 2026 Amirhesamshahab (<https://hesamshahab.com>)

Permission is hereby granted, free of charge, to any person obtaining a copy

of this software and associated documentation files (the "Software"), to deal

in the Software without restriction, including without limitation the rights

to use, copy, modify, merge, publish, distribute, sublicense, and/or sell

copies of the Software, and to permit persons to whom the Software is

furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR

IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE

AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE

SOFTWARE.


---
