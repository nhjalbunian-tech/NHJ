'use client'

import { useMemo, useState } from 'react'
import {
  BarChart3,
  Bell,
  Boxes,
  Building2,
  CheckCircle2,
  ChevronLeft,
  ClipboardList,
  Menu,
  PackageCheck,
  Plus,
  Search,
  Settings,
  ShieldCheck,
  Truck,
  Users,
  X,
} from 'lucide-react'

const stats = [
  { label: 'المشاريع النشطة', value: '12', change: '+8.2%', icon: Building2, tone: 'blue' },
  { label: 'طلبات الشراء', value: '48', change: '+12.5%', icon: ClipboardList, tone: 'amber' },
  { label: 'قيد التحقق', value: '23', change: '-4.1%', icon: ShieldCheck, tone: 'emerald' },
  { label: 'المستخدمون', value: '86', change: '+6.4%', icon: Users, tone: 'violet' },
]

const projects = [
  { name: 'مجمع النخيل السكني', code: 'NHJ-001', owner: 'شركة البناء المتحدة', progress: 78, status: 'قيد التنفيذ', color: 'bg-emerald-500' },
  { name: 'مستشفى المدينة الطبي', code: 'NHJ-002', owner: 'مؤسسة الإعمار', progress: 52, status: 'قيد التنفيذ', color: 'bg-blue-500' },
  { name: 'مركز الأعمال الذكي', code: 'NHJ-003', owner: 'شركة نهج للمقاولات', progress: 31, status: 'تخطيط', color: 'bg-amber-500' },
]

const activities = [
  ['تم اعتماد طلب شراء #PR-1048', 'منذ 12 دقيقة', 'bg-emerald-100 text-emerald-700'],
  ['إضافة عضو جديد: أحمد العتيبي', 'منذ 38 دقيقة', 'bg-blue-100 text-blue-700'],
  ['اكتمل التحقق من مشروع NHJ-001', 'منذ ساعة', 'bg-violet-100 text-violet-700'],
  ['استلام شحنة المواد #GRN-220', 'منذ ساعتين', 'bg-amber-100 text-amber-700'],
]

export default function Page() {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [notice, setNotice] = useState('')
  const filteredProjects = useMemo(() => projects.filter((project) => project.name.includes(query) || project.code.includes(query)), [query])

  function showNotice(message: string) {
    setNotice(message)
    window.setTimeout(() => setNotice(''), 3000)
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      {notice && <div className="fixed left-6 top-6 z-50 rounded-xl bg-slate-900 px-5 py-3 text-sm text-white shadow-lg">{notice}</div>}
      <aside className={`${sidebarOpen ? 'translate-x-0' : 'translate-x-full'} fixed inset-y-0 right-0 z-40 w-72 border-l border-slate-200 bg-white p-5 transition-transform lg:translate-x-0`}>
        <div className="mb-10 flex items-center justify-between">
          <div><div className="text-2xl font-black text-blue-700">نهج</div><div className="text-xs text-slate-400">NHJ AI PLATFORM</div></div>
          <button className="lg:hidden" onClick={() => setSidebarOpen(false)} aria-label="إغلاق القائمة"><X size={20} /></button>
        </div>
        <nav className="space-y-2 text-sm">
          <a className="flex items-center gap-3 rounded-xl bg-blue-50 px-4 py-3 font-semibold text-blue-700" href="#dashboard"><BarChart3 size={19} /> لوحة التحكم</a>
          <a className="flex items-center gap-3 rounded-xl px-4 py-3 text-slate-600 hover:bg-slate-50" href="#projects"><Building2 size={19} /> المشاريع</a>
          <a className="flex items-center gap-3 rounded-xl px-4 py-3 text-slate-600 hover:bg-slate-50" href="#procurement"><Boxes size={19} /> المشتريات والمخزون</a>
          <a className="flex items-center gap-3 rounded-xl px-4 py-3 text-slate-600 hover:bg-slate-50" href="#verification"><ShieldCheck size={19} /> التحقق والجودة</a>
          <a className="flex items-center gap-3 rounded-xl px-4 py-3 text-slate-600 hover:bg-slate-50" href="#team"><Users size={19} /> الفريق والصلاحيات</a>
        </nav>
        <div className="absolute bottom-5 left-5 right-5 border-t border-slate-100 pt-4"><button onClick={() => showNotice('الإعدادات ستكون متاحة قريبًا')} className="flex w-full items-center gap-3 rounded-xl px-4 py-3 text-sm text-slate-500 hover:bg-slate-50"><Settings size={19} /> الإعدادات</button></div>
      </aside>

      <main className="lg:mr-72">
        <header className="sticky top-0 z-30 flex h-20 items-center justify-between border-b border-slate-200 bg-white/90 px-5 backdrop-blur lg:px-10">
          <button className="lg:hidden" onClick={() => setSidebarOpen(true)} aria-label="فتح القائمة"><Menu /></button>
          <div className="hidden text-sm text-slate-500 sm:block">السبت، 19 سبتمبر 2026</div>
          <div className="flex items-center gap-3"><button onClick={() => showNotice('لا توجد إشعارات جديدة')} className="relative rounded-xl p-2 text-slate-500 hover:bg-slate-100" aria-label="الإشعارات"><Bell size={20} /><span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-red-500" /></button><div className="flex items-center gap-3 border-r border-slate-200 pr-4"><div className="hidden text-left sm:block"><div className="text-sm font-semibold">مدير النظام</div><div className="text-xs text-slate-400">مسؤول المنصة</div></div><div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 font-bold text-blue-700">م</div></div></div>
        </header>
        <div id="dashboard" className="space-y-8 p-5 lg:p-10">
          <section className="flex flex-col justify-between gap-4 sm:flex-row sm:items-end"><div><p className="mb-2 text-sm font-medium text-blue-700">مرحبًا بك في نهج</p><h1 className="text-3xl font-black tracking-tight text-slate-900">نظرة عامة على المنصة</h1><p className="mt-2 text-sm text-slate-500">تابع أداء مشاريعك وعملياتك من مكان واحد.</p></div><button onClick={() => showNotice('تم فتح نموذج إنشاء مشروع جديد')} className="flex items-center justify-center gap-2 rounded-xl bg-blue-700 px-5 py-3 text-sm font-semibold text-white shadow-sm hover:bg-blue-800"><Plus size={18} /> مشروع جديد</button></section>
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{stats.map(({ label, value, change, icon: Icon, tone }) => <div key={label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><div className="flex items-start justify-between"><div className={`rounded-xl p-3 ${tone === 'blue' ? 'bg-blue-50 text-blue-700' : tone === 'amber' ? 'bg-amber-50 text-amber-700' : tone === 'emerald' ? 'bg-emerald-50 text-emerald-700' : 'bg-violet-50 text-violet-700'}`}><Icon size={21} /></div><span className={`text-xs font-semibold ${change.startsWith('+') ? 'text-emerald-600' : 'text-rose-600'}`}>{change}</span></div><div className="mt-5 text-3xl font-black">{value}</div><div className="mt-1 text-sm text-slate-500">{label}</div></div>)}</section>
          <section className="grid gap-6 xl:grid-cols-[1.5fr_1fr]">
            <div id="projects" className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div className="mb-6 flex items-center justify-between"><div><h2 className="font-bold">المشاريع الحالية</h2><p className="mt-1 text-xs text-slate-400">آخر تحديث منذ 5 دقائق</p></div><a href="#projects" className="text-sm font-semibold text-blue-700">عرض الكل</a></div><div className="relative mb-5"><Search className="absolute right-3 top-3 text-slate-400" size={18} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="البحث في المشاريع..." className="w-full rounded-xl border border-slate-200 bg-slate-50 py-2.5 pr-10 pl-4 text-sm outline-none focus:border-blue-500" /></div><div className="space-y-5">{filteredProjects.map((project) => <div key={project.code} className="rounded-xl border border-slate-100 p-4"><div className="flex items-start justify-between gap-3"><div><div className="font-semibold">{project.name}</div><div className="mt-1 text-xs text-slate-400">{project.code} · {project.owner}</div></div><span className="rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">{project.status}</span></div><div className="mt-4 flex items-center gap-3"><div className="h-2 flex-1 overflow-hidden rounded-full bg-slate-100"><div className={`h-full rounded-full ${project.color}`} style={{ width: `${project.progress}%` }} /></div><span className="text-xs font-semibold text-slate-500">{project.progress}%</span></div></div>)}</div></div>
            <div id="procurement" className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div className="mb-6 flex items-center justify-between"><div><h2 className="font-bold">النشاط الأخير</h2><p className="mt-1 text-xs text-slate-400">حركة المنصة اليوم</p></div><CheckCircle2 className="text-emerald-500" size={20} /></div><div className="space-y-5">{activities.map(([title, time, style]) => <div key={title} className="flex gap-3"><div className={`mt-0.5 rounded-lg p-2 ${style}`}><PackageCheck size={16} /></div><div><div className="text-sm font-medium">{title}</div><div className="mt-1 text-xs text-slate-400">{time}</div></div></div>)}</div><button onClick={() => showNotice('تم تحميل جميع الأنشطة')} className="mt-7 w-full rounded-xl border border-slate-200 py-2.5 text-sm font-semibold text-slate-600 hover:bg-slate-50">عرض جميع الأنشطة</button></div>
          </section>
          <section id="verification" className="grid gap-6 md:grid-cols-3"><div className="rounded-2xl bg-gradient-to-br from-blue-700 to-indigo-800 p-6 text-white md:col-span-2"><div className="flex items-start justify-between"><div><div className="mb-3 inline-flex rounded-lg bg-white/15 p-2"><Truck size={20} /></div><h2 className="text-xl font-bold">مركز العمليات الذكي</h2><p className="mt-2 max-w-lg text-sm leading-6 text-blue-100">استخدم أدوات نهج لمتابعة التوريد، وتدقيق الكميات، وتقليل التأخير في مواقع العمل.</p></div><div className="hidden rounded-2xl bg-white/10 p-4 sm:block"><div className="text-3xl font-black">94%</div><div className="mt-1 text-xs text-blue-100">كفاءة العمليات</div></div></div><button onClick={() => showNotice('جاري فتح مركز العمليات')} className="mt-6 rounded-xl bg-white px-4 py-2.5 text-sm font-bold text-blue-700 hover:bg-blue-50">فتح المركز <ChevronLeft className="mr-1 inline" size={16} /></button></div><div id="team" className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="font-bold">حالة النظام</h2><div className="mt-5 space-y-4 text-sm"><div className="flex items-center justify-between"><span className="text-slate-500">خدمة API</span><span className="flex items-center gap-1.5 text-emerald-600"><span className="h-2 w-2 rounded-full bg-emerald-500" /> تعمل</span></div><div className="flex items-center justify-between"><span className="text-slate-500">قاعدة البيانات</span><span className="flex items-center gap-1.5 text-emerald-600"><span className="h-2 w-2 rounded-full bg-emerald-500" /> مستقرة</span></div><div className="flex items-center justify-between"><span className="text-slate-500">آخر نسخة احتياطية</span><span className="font-medium">منذ 2 ساعة</span></div></div></div></section>
        </div>
      </main>
    </div>
  )
}
