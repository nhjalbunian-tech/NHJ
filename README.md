# NHJ AI

منصة نهج لإدارة مشاريع الإنشاءات والمشتريات والتحقق.

## التشغيل المحلي

### الواجهة

```bash
corepack enable
pnpm install
pnpm dev
```

افتح http://localhost:3000

### الـ Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

افتح http://127.0.0.1:8000/docs

## API

- `GET /health`
- `GET /api/dashboard`
- `GET|POST /api/projects`
- `GET|POST /api/procurement`

## النشر

- الواجهة: اربط المستودع بخدمة Vercel، وسيكتشف Next.js تلقائيًا.
- الـ Backend: اربط المستودع بخدمة Render؛ ملف `render.yaml` جاهز ويستخدم مجلد `backend`.

> البيانات الحالية داخل الذاكرة للتجربة. قبل الإنتاج يجب إضافة PostgreSQL ومصادقة حقيقية ومتغيرات سرية.
