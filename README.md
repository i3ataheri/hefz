# حلقة تحفيظ القرآن - نظام تسجيل الحضور

نظام تسجيل حضور حلقة القرآن باستخدام Astro + Supabase

## هيكل المشروع

```
hefz/
├── frontend/              # الواجهة الأمامية (Astro + TypeScript + SCSS)
│   ├── src/
│   │   ├── layouts/       # التخطيط
│   │   ├── lib/           # المكتبات المساعدة
│   │   ├── pages/         # الصفحات
│   │   └── styles/        # الأنماط
│   ├── package.json
│   └── astro.config.mjs
├── supabase/
│   ├── schema.sql         # هيكل قاعدة البيانات
│   └── seed.sql           # البيانات الأولية
├── .env.example
└── README.md
```

## الإعداد

### 1. قاعدة البيانات (Supabase)

1. أنشئ مشروع جديد في [supabase.com](https://supabase.com)
2. اذهب إلى SQL Editor وشغّل `supabase/schema.sql`
3. ثم شغّل `supabase/seed.sql`
4. خذ المفاتيح من Project Settings > API

### 2. الواجهة الأمامية

```bash
cd frontend
cp ../.env.example .env
# املأ ملف .env بالقيم من Supabase
npm install
npm run dev
```

## رمز المديرات (PIN)

بعد انتهاء التسجيل، يظهر تقرير اليوم. لنسخ التقرير يجب إدخال رمز المدير.

لتعديل الرمز: Supabase Dashboard → Table Editor → جدول `managers` → عمود `pin`

## الإعدادات في Supabase

### جدول `settings`

| key | value | الوصف |
|-----|-------|-------|
| `is_saturday_enabled` | `false` | هل السبت مفتوح؟ (`true` أو `false`) |

### جدول `managers`

قائمة المديرات. كل مدير لها رمز (pin). لإضافة أو حذف مدير استخدم Table Editor.

### جدول `priority_members`

الأعضاء المميزون (يظهرون بعد المديرات في الترتيب). لإضافة أو حذف عضو مميز استخدم Table Editor.

## منطق النظام

- **وقت التسجيل**: من الساعة 1 ظهرًا إلى 3 عصرًا بتوقيت مكة المكرمة
- **الجمعة**: النظام مغلق
- **السبت**: يمكن التحكم عبر `is_saturday_enabled` في جدول settings
- **بعد الساعة 3**: يظهر تقرير اليوم مع رمز المدير
- **تغيير المديرات**: تدور يوميًا (دورة 9 أيام)
- **التقرير**: المديرات ينسخن التقرير بعد إدخال الرمز ويشاركنه في مجموعة الواتساب
