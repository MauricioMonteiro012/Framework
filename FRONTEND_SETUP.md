# 🚀 Guia Rápido - Frontend React Implementado

Seu frontend React com todas as telas foi criado! Aqui está como usar:

## 📋 Requisitos
- Node.js 16+ instalado
- Backend rodando em `http://localhost:5000`

## 🏃 Inicialização Rápida

### 1. Instalar dependências
```bash
npm install
```

### 2. Modo desenvolvimento (com HMR)
```bash
npm run dev
```
Acesse `http://localhost:5173`

### 3. Build para produção
```bash
npm run build
```
Isso vai:
- Compilar o React com Vite
- Gerar assets em `static/frontend/`
- Criar `templates/react_index.html` automaticamente

## 📁 Estrutura de Pastas

```
frontend/
├── src/
│   ├── pages/          # Telas do sistema
│   ├── context/        # Contexto de autenticação
│   ├── services/       # Chamadas de API
│   ├── components/     # Componentes reutilizáveis
│   ├── App.jsx         # Componente principal com rotas
│   └── main.jsx        # Ponto de entrada
├── index.html          # HTML base para Vite
└── vite.config.js      # Configuração Vite
```

## 🎯 Telas Implementadas

✅ **Autenticação:**
- Cadastro de vendedor
- Ativação via código (WhatsApp)
- Login

✅ **Produtos:**
- Listagem com grid responsivo
- Cadastro de novo produto
- Edição de produto
- Inativação de produto

✅ **Vendas:**
- Formulário para registrar venda
- Validação de estoque e status

✅ **Dashboard:**
- Estatísticas (total de produtos, estoque, vendas, receita)
- Tabelas de últimos produtos e vendas

## 🔌 Integração com Backend

A aplicação se conecta automaticamente ao backend em `http://localhost:5000/api`.

**Endpoints utilizados:**
- `POST /api/sellers` - Cadastro
- `POST /api/sellers/activate` - Ativação
- `POST /api/auth/login` - Login
- `GET/POST /api/products` - Gerenciar produtos
- `POST /api/sales` - Registrar vendas

## 🔐 Autenticação

- Tokens JWT são salvos em `localStorage`
- Rotas protegidas redirecionam para login se não autenticado
- Logout limpa os dados da sessão

## 🛠️ Troubleshooting

**Erro de CORS:**
Certifique-se que o backend retorna headers CORS corretos:
```python
cors = CORS(app, origins=["http://localhost:5173"])
```

**Porta 5173 já em uso:**
```bash
npm run dev -- --port 5174
```

**Build não gera templates/react_index.html:**
Certifique-se que Node.js e npm estão instalados corretamente.

## 📱 Responsividade

Todas as telas foram desenvolvidas com design responsivo:
- Desktop: grid layout completo
- Tablet: 2-3 colunas
- Mobile: 1 coluna, navegação em abas

## 🚀 Deploy

1. Execute `npm run build` localmente
2. Faça commit de `static/frontend/` e `templates/react_index.html`
3. Configure o backend para servir `templates/react_index.html` na rota raiz
4. Os assets estáticos são servidos automaticamente de `static/frontend/`

---

**Pronto para apresentação? Rode `npm run build` e teste no backend!** 🎉
