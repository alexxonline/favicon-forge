import { useEffect, useState } from 'preact/hooks'
import './app.css'

const DEFAULT_PROMPT = 'A minimalist fox head made of geometric triangles'
const FALLBACK_ENDPOINT = 'http://localhost:8000/generate'

export function App() {
  const [prompt, setPrompt] = useState(DEFAULT_PROMPT)
  const [svg, setSvg] = useState('')
  const [svgUrl, setSvgUrl] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!svg) {
      setSvgUrl(null)
      return undefined
    }

    const blob = new Blob([svg], { type: 'image/svg+xml' })
    const url = URL.createObjectURL(blob)
    setSvgUrl(url)

    return () => URL.revokeObjectURL(url)
  }, [svg])

  const endpoint = import.meta.env.VITE_API_URL ?? FALLBACK_ENDPOINT

  const handleSubmit = async (event: Event) => {
    event.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt }),
      })

      if (!response.ok) {
        const message = await response.text()
        throw new Error(message || 'Failed to generate icon.')
      }

      const data = await response.json()
      setSvg(data.svg ?? '')
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Something went wrong.'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div class="page">
      <header class="hero">
        <p class="eyebrow">Nano Banana → Vector</p>
        <h1>Favicon Forge</h1>
        <p class="subtitle">
          Turn a tiny prompt into a crisp SVG favicon in seconds.
        </p>
      </header>

      <main class="workspace">
        <section class="panel prompt-panel">
          <form onSubmit={handleSubmit} class="prompt-form">
            <label class="label" for="prompt">
              Describe the icon you want
            </label>
            <textarea
              id="prompt"
              name="prompt"
              rows={6}
              value={prompt}
              onInput={(event) => setPrompt((event.target as HTMLTextAreaElement).value)}
              placeholder="e.g. A neon jellyfish with flowing tentacles"
            />
            <button class="primary" type="submit" disabled={isLoading}>
              {isLoading ? 'Forging…' : 'Generate SVG'}
            </button>
            {error ? <p class="status error">{error}</p> : null}
          </form>
        </section>

        <section class="panel preview-panel">
          <div class="preview-header">
            <div>
              <p class="label">SVG Preview</p>
              <p class="meta">Perfect for favicon and app icons.</p>
            </div>
            <a
              class={`download ${svgUrl ? '' : 'disabled'}`}
              href={svgUrl ?? '#'}
              download="favicon.svg"
              aria-disabled={!svgUrl}
            >
              Download
            </a>
          </div>
          <div class="preview-area">
            {svgUrl ? (
              <img src={svgUrl} alt="Generated favicon" />
            ) : (
              <div class="placeholder">
                <p>Generate an icon to see it here.</p>
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  )
}
