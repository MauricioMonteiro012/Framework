# Frontend React + Vite

Frontend completo com todas as telas para o sistema de gerenciamento de produtos e vendas.

## ✨ Telas Implementadas

- ✅ Cadastro de vendedor
- ✅ Ativação via código (WhatsApp)
- ✅ Login
- ✅ Dashboard com estatísticas
- ✅ Listagem de produtos
- ✅ Cadastro e edição de produtos
- ✅ Registro de vendas
- ✅ Relatórios

## 🚀 Quick Start

```bash
npm install
npm run dev      # desenvolvimento
npm run build    # produção
```

## 📁 Estrutura

```
src/
├── pages/               # Telas (Register, Login, Dashboard, etc)
├── context/             # AuthContext para gerenciar sessão
├── services/            # API client com axios
├── components/          # ProtectedRoute
└── App.jsx              # Routing com React Router
```

## 🔗 API

Conecta-se ao backend em `http://localhost:5000/api`

## 📖 Mais detalhes

Veja [FRONTEND_SETUP.md](../FRONTEND_SETUP.md) para guia completo.
