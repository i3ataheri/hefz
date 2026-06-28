# 📖 حلقة القرآن - نظام تسجيل الحضور

سیستم ثبت‌نام حلقه قرآن با فرانت‌اند Astro + دیتابیس Supabase + بک‌اند Python

## ساختار پروژه

```
hefz/
├── frontend/              # فرانت‌اند (Astro + TypeScript + SCSS)
│   ├── src/
│   │   ├── components/    # کامپوننت‌ها
│   │   ├── layouts/       # قالب‌بندی
│   │   ├── lib/           # ماژول‌های کمکی
│   │   ├── pages/         # صفحات
│   │   └── styles/        # استایل‌ها
│   ├── package.json
│   └── astro.config.mjs
├── backend/               # بک‌اند (Python)
│   ├── main.py            # زمان‌بندی کارها
│   ├── supabase_client.py # اتصال به Supabase
│   ├── report.py          # تولید گزارش
│   ├── whatsapp.py        # ارسال به واتس‌اپ
│   ├── cleanup.py         # پاکسازی دیتابیس
│   └── requirements.txt
├── supabase/
│   ├── schema.sql         # دیتابیس
│   └── seed.sql           # داده‌های اولیه
├── .env.example
└── README.md
```

## راه‌اندازی سریع

### 1. دیتابیس (Supabase)

1. یک پروژه در [supabase.com](https://supabase.com) بسازید
2. به SQL Editor بروید و `supabase/schema.sql` را اجرا کنید
3. سپس `supabase/seed.sql` را اجرا کنید (اسامی مدیران را به‌روز کنید)
4. از Project Settings > API کلیدها را بردارید

### 2. فرانت‌اند

```bash
cd frontend
cp ../.env.example .env
# .env را با مقادیر واقعی از Supabase پر کنید
npm install
npm run dev
```

### 3. بک‌اند

```bash
cd backend
cp ../.env.example .env
# .env را با مقادیر واقعی پر کنید
pip install -r requirements.txt
python main.py
```

### 4. راه‌اندازی Meta WhatsApp Cloud API

۱. به [developers.facebook.com](https://developers.facebook.com) بروید
۲. یک **WhatsApp App** بسازید
۳. در بخش **API Setup** شماره تلفن مجازی بگیرید
۴. **Permanent Access Token** بسازید (توکن ۶۰ روزه)
۵. شماره تجاری را به گروه واتس‌اپ خود اضافه کنید
۶. `META_ACCESS_TOKEN`, `META_PHONE_NUMBER_ID`, `WHATSAPP_GROUP_ID` را در `.env` پر کنید

> مصرف شما ~۲۵ پیام در ماه → کاملاً رایگان (تا ۱,۰۰۰ conversation ماهانه)

## تنظیمات در Supabase

### جدول `settings`

| key | value | توضیح |
|-----|-------|-------|
| `is_saturday_enabled` | `false` | شنبه باز باشد؟ (`true` یا `false`) |
| `timezone` | `"Asia/Riyadh"` | منطقه زمانی |
| `registration_open_hour` | `13` | ساعت شروع (به وقت عربستان) |
| `registration_close_hour` | `15` | ساعت پایان |
| `whatsapp_group_id` | `""` | آیدی گروه واتس‌اپ |

### جدول `managers`

لیست ۵ مدیر حلقه.
**توجه**: نام مدیران باید **دقیقاً** مطابق نامی باشد که هنگام ثبت‌نام وارد می‌کنند، چون سیستم برای تشخیص مدیران از طریق تطبیق اسم عمل می‌کند.

## منطق سیستم

- **زمان ثبت‌نام**: ۱۳:۰۰ تا ۱۵:۰۰ به وقت عربستان
- **جمعه**: سیستم بسته است
- **شنبه**: قابل کنترل با flag `is_saturday_enabled` در settings
- **حضور**: فقط کسانی که ثبت‌نام کردند در گزارش می‌آیند. غایبان و معذوران در لیست نیستند
- **چرخش مدیران**: از بین مدیرانی که **ثبت‌نام کرده‌اند**، ترتیب چرخشی اعمال می‌شود (هر روز یک نفر اول، چرخه ۵ روزه)
- **گزارش روزانه**: ساعت ۱۵:۰۰ به واتس‌اپ ارسال می‌شود
- **پاکسازی**: هر شب ساعت ۰۰:۰۰ دیتابیس خالی می‌شود

## استقرار (Deployment)

- فرانت‌اند: قابل استقرار روی [Cloudflare Pages](https://pages.cloudflare.com) یا [Netlify](https://netlify.com)
- بک‌اند: روی یک سرور مجازی (VPS) یا [Railway](https://railway.app) / [Heroku](https://heroku.com)
