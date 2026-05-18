const API_URL = 'http://localhost:8081';

// ====== CADASTRO ======
document.addEventListener('DOMContentLoaded', () => {
  const cadastroForm = document.getElementById('cadastroForm');
  if (cadastroForm) {
    cadastroForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const data = {
        name: document.getElementById('name').value,
        cnpj: document.getElementById('cnpj').value,
        email: document.getElementById('email').value,
        celular: document.getElementById('celular').value,
        password: document.getElementById('password').value
      };

      try {
        const response = await fetch(`${API_URL}/api/sellers`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
          alert('Cadastro realizado! ' + result.mensagem);
          if (result.activation_code) {
            alert('Código de ativação: ' + result.activation_code);
          }
          // Redirecionar para ativação
          setTimeout(() => window.location.href = '/ativacao', 2000);
        } else {
          alert('Erro: ' + (result.erro || 'Tente novamente'));
        }
      } catch (error) {
        alert('Erro de conexão: ' + error.message);
      }
    });
  }

  // ====== ATIVAÇÃO ======
  const ativacaoForm = document.getElementById('ativacaoForm');
  if (ativacaoForm) {
    ativacaoForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const data = {
        email: document.getElementById('email').value,
        celular: document.getElementById('celular').value,
        codigo: document.getElementById('codigo').value
      };

      try {
        const response = await fetch(`${API_URL}/api/sellers/activate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
          alert('Conta ativada com sucesso!');
          setTimeout(() => window.location.href = '/login', 2000);
        } else {
          alert('Erro: ' + (result.erro || 'Código inválido'));
        }
      } catch (error) {
        alert('Erro de conexão: ' + error.message);
      }
    });
  }

  // ====== LOGIN ======
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const data = {
        email: document.getElementById('identifier').value,
        senha: document.getElementById('password').value
      };

      try {
        const response = await fetch(`${API_URL}/api/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
          alert('Login realizado com sucesso!');
          localStorage.setItem('token', result.token);
          setTimeout(() => window.location.href = '/', 2000);
        } else {
          alert('Erro: ' + (result.error || 'Credenciais inválidas'));
        }
      } catch (error) {
        alert('Erro de conexão: ' + error.message);
      }
    });
  }
});
