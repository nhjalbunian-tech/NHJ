:root {
  color-scheme: dark;
  --background: #020817;
  --foreground: #e2e8f0;
}

html {
  scroll-behavior: smooth;
  background: var(--background);
}

body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at top, rgba(16, 185, 129, 0.1), transparent 30%),
    radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.08), transparent 28%),
    #020817;
  color: var(--foreground);
  font-family: Arial, Helvetica, sans-serif;
}

* {
  box-sizing: border-box;
}

button,
a {
  transition: all 180ms ease;
}

::selection {
  background: rgba(16, 185, 129, 0.35);
  color: #f8fafc;
}

.panel {
  background: rgba(15, 23, 42, 0.72);
  border: 1px solid rgba(148, 163, 184, 0.16);
  box-shadow: 0 20px 60px rgba(2, 6, 23, 0.35);
  backdrop-filter: blur(16px);
}

.glow {
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.04),
    0 20px 80px rgba(35, 208, 168, 0.1);
}

