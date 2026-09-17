import { Analytics } from '@vercel/analytics/next'
import type { Metadata, Viewport } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'NHJ AI | Construction Intelligence',
  description: 'AI-powered construction management platform for projects, approvals, procurement, and audit control.',
  generator: 'NHJ AI',
}

export const viewport: Viewport = {
  colorScheme: 'dark',
  themeColor: '#020817',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
        {process.env.NODE_ENV === 'production' && <Analytics />}
      </body>
    </html>
  )
}

