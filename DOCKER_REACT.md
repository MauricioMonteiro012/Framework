# Docker + React Build

## O que mudou no Dockerfile

O Dockerfile foi atualizado com **multi-stage build** para compilar o React:

### Stage 1: Node.js (Frontend Build)
- Instala dependências do `package.json`
- Compila o React com Vite
- Gera arquivos em `static/frontend/` e `templates/react_index.html`
- Esta stage é descartada na imagem final (otimiza tamanho)

### Stage 2: Python (Flask)
- Instala dependências Python normalmente
- Copia os arquivos buildados do React da Stage 1
- Executa o Flask como antes

## Como funciona o build

```bash
docker build -t seu-projeto .
```

Ou com docker-compose:

```bash
docker-compose up --build
```

O Docker automaticamente:
1. Compila o React (sem precisar de Node.js na sua máquina)
2. Gera `static/frontend/` e `templates/react_index.html`
3. Copia para a imagem Flask
4. Inicia o servidor na porta 5000

## Sem quebras!

✅ Backend continua funcionando normalmente
✅ Rotas API não foram alteradas
✅ Banco de dados não foi tocado
✅ Apenas a rota `/` agora serve o React em vez do template antigo

## Docker Compose (docker-compose.yml)

Se você estiver usando docker-compose, o build acontece automaticamente. Certifique-se que o arquivo está configurado com:

```yaml
build: .
ports:
  - "5000:5000"
```

## Rebuild se necessário

Se alterar arquivos do React, faça o rebuild:

```bash
docker-compose up --build
```

Ou sem compose:

```bash
docker build -t seu-projeto . && docker run -p 5000:5000 seu-projeto
```

---

**Pronto! Seu Docker agora compila e serve o React automaticamente! 🚀**
