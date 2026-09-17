'use client'

import { useEffect, useMemo, useState } from 'react'
import { Clock3, Globe2, MapPin, RefreshCw } from 'lucide-react'

type Zone = {
  city: string
  country: string
  timeZone: string
}

const zones: Zone[] = [
  { city: 'Riyadh', country: 'Saudi Arabia', timeZone: 'Asia/Riyadh' },
  { city: 'London', country: 'United Kingdom', timeZone: 'Europe/London' },
  { city: 'New York', country: 'United States', timeZone: 'America/New_York' },
  { city: 'Tokyo', country: 'Japan', timeZone: 'Asia/Tokyo' },
  { city: 'Sydney', country: 'Australia', timeZone: 'Australia/Sydney' },
  { city: 'Dubai', country: 'United Arab Emirates', timeZone: 'Asia/Dubai' },
]

function formatTime(date: Date, timeZone: string, options: Intl.DateTimeFormatOptions) {
  return new Intl.DateTimeFormat('en-US', { ...options, timeZone }).format(date)
}

export default function Page() {
  const [now, setNow] = useState<Date | null>(null)
  const [is24Hour, setIs24Hour] = useState(false)

  useEffect(() => {
    const updateTime = () => setNow(new Date())
    updateTime()
    const timer = window.setInterval(updateTime, 1000)
    return () => window.clearInterval(timer)
  }, [])

  const localZone = useMemo(() => Intl.DateTimeFormat().resolvedOptions().timeZone, [])
  const currentTime = now || new Date()
  const timeOptions: Intl.DateTimeFormatOptions = {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: !is24Hour,
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl px-6 py-6 lg:px-8">
        <header className="panel flex items-center justify-between rounded-2xl px-5 py-4">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/15 text-emerald-300 ring-1 ring-emerald-400/30">
              <Clock3 size={20} />
            </div>
            <div>
              <p className="text-lg font-semibold tracking-tight text-white">WorldTime</p>
              <p className="text-xs text-slate-400">A live clock for every team</p>
            </div>
          </div>
          <div className="flex items-center gap-3 text-sm text-slate-400">
            <Globe2 size={17} className="text-emerald-300" />
            <span className="hidden sm:inline">Your zone: {localZone}</span>
          </div>
        </header>

        <section className="relative mt-8 overflow-hidden rounded-[32px] border border-slate-800 bg-slate-900/80 p-6 shadow-2xl shadow-slate-950/40 md:p-10">
          <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(16,185,129,0.2),_transparent_34%),radial-gradient(circle_at_bottom_right,_rgba(59,130,246,0.14),_transparent_34%)]" />
          <div className="relative flex flex-col justify-between gap-8 md:flex-row md:items-end">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-emerald-300">Current local time</p>
              <h1 className="mt-4 font-mono text-5xl font-black tracking-tight text-white sm:text-7xl md:text-8xl">
                {formatTime(currentTime, localZone, timeOptions)}
              </h1>
              <p className="mt-4 text-lg text-slate-300">
                {formatTime(currentTime, localZone, { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' })}
              </p>
            </div>
            <button
              type="button"
              onClick={() => setNow(new Date())}
              className="inline-flex items-center gap-2 self-start rounded-full border border-slate-700 bg-slate-950/60 px-4 py-2 text-sm font-medium text-slate-200 transition hover:border-slate-500 hover:text-white md:self-auto"
            >
              <RefreshCw size={16} /> Sync now
            </button>
          </div>

          <div className="relative mt-8 flex items-center justify-between gap-4 border-t border-slate-800 pt-5">
            <p className="text-sm text-slate-400">Updates every second</p>
            <button
              type="button"
              aria-pressed={is24Hour}
              onClick={() => setIs24Hour((value) => !value)}
              className="rounded-full bg-emerald-500 px-4 py-2 text-sm font-semibold text-slate-950 transition hover:bg-emerald-400"
            >
              {is24Hour ? '24-hour format' : '12-hour format'}
            </button>
          </div>
        </section>

        <section className="mt-10">
          <div className="mb-5 flex items-end justify-between gap-4">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-cyan-300">Time zones</p>
              <h2 className="mt-2 text-3xl font-black text-white">Stay in sync worldwide</h2>
            </div>
            <p className="hidden text-sm text-slate-500 sm:block">Live from your device clock</p>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {zones.map((zone) => (
              <article key={zone.timeZone} className="panel rounded-3xl p-5 transition hover:-translate-y-1 hover:border-slate-600">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="text-xl font-bold text-white">{zone.city}</h3>
                    <p className="mt-1 text-sm text-slate-400">{zone.country}</p>
                  </div>
                  <MapPin size={18} className="text-emerald-300" />
                </div>
                <p className="mt-7 font-mono text-3xl font-bold tracking-tight text-emerald-300">
                  {formatTime(currentTime, zone.timeZone, timeOptions)}
                </p>
                <p className="mt-3 text-sm text-slate-400">
                  {formatTime(currentTime, zone.timeZone, { weekday: 'short', month: 'short', day: 'numeric' })}
                </p>
                <p className="mt-4 border-t border-slate-800 pt-3 text-xs text-slate-500">{zone.timeZone}</p>
              </article>
            ))}
          </div>
        </section>
      </div>
    </main>
  )
}

