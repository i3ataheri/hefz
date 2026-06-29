# حلقة القرآن - نظام تسجيل الحضور

سیستم ثبت‌نام حلقه قرآن با فرانت‌اند Astro + دیتابیس Supabase

## ساختار پروژه

```
hefz/
├── frontend/              # فرانت‌اند (Astro + TypeScript + SCSS)
│   ├── src/
│   │   ├── layouts/       # قالب‌بندی
│   │   ├── lib/           # ماژول‌های کمکی
│   │   ├── pages/         # صفحات
│   │   └── styles/        # استایل‌ها
│   ├── package.json
│   └── astro.config.mjs
├── supabase/
│   ├── schema.sql         # دیتابیس
│   └── seed.sql           # داده‌های اولیه
├── .env.example
└── README.md
```

## راه‌اندازی

### 1. دیتابیس (Supabase)

1. یک پروژه در [supabase.com](https://supabase.com) بسازید
2. به SQL Editor بروید و `supabase/schema.sql` را اجرا کنید
3. سپس `supabase/seed.sql` را اجرا کنید
4. از Project Settings > API کلیدها را بردارید

### 2. فرانت‌اند

```bash
cd frontend
cp ../.env.example .env
# .env را با مقادیر واقعی از Supabase پر کنید
npm install
npm run dev
```

## PIN کد مدیران

بعد از بسته شدن ثبت‌نام، بخش گزارش روزانه ظاهر می‌شه. برای دیدن و کپی گزارش، باید PIN مدیر وارد بشه.

PIN های پیش‌فرض:
- أولياء: 1234
- دعاء: 2345
- منيرة: 3456
- مريم: 4567
- عائشة أبوعقيل: 5678
- طيف: 6789
- دانا: 7891
- حنان: 8912
- إيمان أحمد: 9123

برای تغییر PIN: Supabase Dashboard → Table Editor → جدول `managers` → ستون `pin`

## تنظیمات در Supabase

### جدول `settings`

| key | value | توضیح |
|-----|-------|-------|
| `is_saturday_enabled` | `false` | شنبه باز باشد؟ (`true` یا `false`) |

### جدول `managers`

لیست ۹ مدیر حلقه. هر مدیر یک `pin` دارد. برای اضافه/حذف مدیر از Table Editor استفاده کنید.

## منطق سیستم

- **زمان ثبت‌نام**: ۱۳:۰۰ تا ۱۵:۰۰ به وقت عربستان
- **جمعه**: سیستم بسته است
- **شنبه**: قابل کنترل با `is_saturday_enabled` در settings
- **بعد از ساعت ۳**: بخش گزارش با PIN مدیر فعال می‌شود
- **چرخش مدیران**: هر روز یک مدیر به عنوان مدیر روز (چرخش ۹ روزه)
- **گزارش**: مدیران می‌توانند با وارد کردن PIN، گزارش روزانه را کپی کرده و در گروه واتساپ بچسبانند

## استقرار (Deployment)

- فرانت‌اند روی [Vercel](https://vercel.com) مستقر شده - https://hefz.vercel.app
