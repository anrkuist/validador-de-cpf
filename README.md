# CPF Validator - Azure Functions

Validador de CPF que consulta diretamente na base da Receita Federal.

## 🚀 Como usar

**Query String (GET):**

```bash
curl "https://sua-function.azurewebsites.net/api/validarcpf?code=SUA_KEY&cpf=12345678901"
```

**JSON Body (POST):**

```bash
curl -X POST "https://sua-function.azurewebsites.net/api/validarcpf?code=SUA_KEY" \
     -H "Content-Type: application/json" \
     -d '{"cpf": "123.456.789-01"}'
```

**Aceita CPF com ou sem formatação:**

- `12345678901`
- `123.456.789-01`
- `123 456 789 01`

## 📋 Respostas da API

### ✅ CPF Válido (200)
CPF com dígitos corretos E encontrado na Receita Federal:
```json
{
  "cpf": "123.456.789-01",
  "valido": true,
  "mensagem": "CPF encontrado na Receita Federal"
}
```

### ❌ CPF com Dígitos Inválidos (400)
Falha na validação matemática:
```json
{
  "cpf": "123.456.789-01",
  "valido": false,
  "error": "CPF invalido (digitos nao conferem)"
}
```

### ❌ CPF Não Encontrado (400)
Dígitos corretos mas não existe na Receita Federal:
```json
{
  "cpf": "123.456.789-01",
  "valido": false,
  "error": "CPF nao encontrado na Receita Federal"
}
```

### 🔥 Erro de Conexão (500)
```json
{
  "error": "Erro na consulta: timeout"
}
```

### ⚠️ Parâmetro Faltando (400)
```
Passe um CPF na query string (?cpf=123456789) ou no corpo da requisição.
```

## 🛠️ Desenvolvimento Local

### Pré-requisitos

- Python 3.12+
- Azure Functions Core Tools
- VS Code com extensão Azure Functions

### Setup

```bash
# Clonar repositório
git clone https://github.com/SEU_USUARIO/cpf-validator-azure.git
cd cpf-validator-azure

# Criar ambiente virtual
python3.12 -m venv .venv
source .venv/bin/activate  # Mac/Linux
# ou
.venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar localmente
func start
```

### Testar Localmente

```bash
# Testar endpoint local
curl "http://localhost:7071/api/validarcpf?cpf=12345678901"

# Com JSON
curl -X POST "http://localhost:7071/api/validarcpf" \
     -H "Content-Type: application/json" \
     -d '{"cpf": "12345678901"}'
```

## 🔒 Autenticação

Esta API usa **Function Key** para autenticação. A key é **obrigatória** em todas as requisições.

### Obter Function Key:

1. **Portal Azure** → Function App → Functions → validarcpf → Function Keys
2. **VS Code** → Clique direito na função → Copy Function URL (já inclui a key)

### Usar a Key:

```bash
# Na URL
?code=SUA_FUNCTION_KEY

# Ou no header
-H "x-functions-key: SUA_FUNCTION_KEY"
```

## 📡 API Externa

Esta função utiliza a API pública do SCPA (Sistema de Cadastro de Prestadores de Ações de Saúde) do Ministério da Saúde:

```
https://scpa-backend.saude.gov.br/public/scpa-usuario/validacao-cpf/{cpf}
```

**Importante:** Deve ser usado apenas para fins educacionais.

## 🏗️ Arquitetura

```
Cliente → Azure Function → API SCPA → Receita Federal
```

1. Cliente faz requisição com CPF
2. Azure Function valida formato
3. Consulta API SCPA do Ministério da Saúde
4. SCPA consulta Receita Federal
5. Retorna resultado ao cliente

## 🤝 Contribuições

1. Fork do projeto
2. Criar branch para feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit das mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para branch (`git push origin feature/nova-funcionalidade`)
5. Abrir Pull Request

## ⚠️ Disclaimer

Este projeto é para fins educacionais e de aprendizado. A API do SCPA é pública, mas use com responsabilidade e respeite os limites de uso.

---

**Desenvolvido para aprendizado de Azure Functions + Python** 🐍☁️
