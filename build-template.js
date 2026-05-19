import fs from 'fs'
import path from 'path'

const outDir = path.resolve('static/frontend')
const assetsDir = path.resolve(outDir, 'assets')
const manifestPath = path.resolve(outDir, 'manifest.json')
const templatesDir = path.resolve('templates')

if (!fs.existsSync(manifestPath)) {
  console.error('Manifest não encontrado. Execute npm run build primeiro.')
  process.exit(1)
}

const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'))
const entry = manifest['src/main.jsx'] || manifest['src/main.tsx'] || manifest['src/main.js']

if (!entry) {
  console.error('Entrada principal não encontrada no manifest. Verifique o build do Vite.')
  process.exit(1)
}

const cssLinks = (entry.css || [])
  .map((file) => `    <link rel="stylesheet" href="/static/frontend/${file}" />`)
  .join('\n')

const jsScript = `    <script type="module" src="/static/frontend/${entry.file}"></script>`

const templateContent = `<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Framework React</title>
${cssLinks}
  </head>
  <body>
    <div id="root"></div>
${jsScript}
  </body>
</html>`

if (!fs.existsSync(templatesDir)) {
  fs.mkdirSync(templatesDir, { recursive: true })
}

fs.writeFileSync(path.join(templatesDir, 'react_index.html'), templateContent)
console.log('✓ Arquivo templates/react_index.html gerado com sucesso!')
