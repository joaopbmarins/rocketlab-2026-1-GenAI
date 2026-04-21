# Query Interface - GenAI TextToSQL Agent

Interface web para gerar queries SQL automáticamente usando inteligência artificial. O programa utiliza um agente de IA para converter perguntas em linguagem natural para SQL estruturado.

## Pré-requisitos

- Python 3.8+
- pip ou conda
- API Key do Google (Gemini)

## Instalação

### 1. Clone o repositório
```bash
git clone <repository-url>
cd rocketlab-2026-1-GenAI
```

### 2. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```
GOOGLE_API_KEY=sua_chave_api_aqui
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

## Como Usar

### Inicie o servidor

```bash
python -m app.main
```

O servidor estará disponível em: `http://localhost:8000`

### Acesse a Interface Web

1. Abra seu navegador
2. Navegue até `http://localhost:8000`
3. Digite sua consulta em linguagem natural
4. Clique em "Buscar" ou pressione Enter
5. Veja os resultados em três abas:
   - **💭 Reasoning**: Explicação do raciocínio do agente
   - **💾 SQL**: Query SQL gerada com syntax highlighting
   - **✓ Confiança**: Nível de confiança da resposta

## Estrutura do Projeto

```
rocketlab-2026-1-GenAI/
├── app/
│   ├── agent/
│   │   ├── agent.py       # Lógica do agente de IA
│   │   ├── schema.py      # Schemas Pydantic
│   │   └── tools.py       # Ferramentas do agente
│   ├── templates/
│   │   ├── index.html     # Página HTML
│   │   ├── style.css      # Estilos CSS
│   │   └── script.js      # Lógica JavaScript
│   │
│   ├── main.py            # Servidor FastAPI
│   ├── db.py              # Configuração do banco de dados
│   ├── prompt.py          # Prompts do sistema
│   └── utils.py           # Funções utilitárias
├── .env                   # Variáveis de ambiente
└── README.md              # Este arquivo
```

##  Endpoints da API

### GET `/`
Retorna a página HTML principal.

### GET `/query?q=<consulta>`
Executa uma consulta via agente de IA.

**Parâmetros:**
- `q` (string): Consulta em linguagem natural

**Resposta:**
```json
{
  "reasoning": "Explicação do raciocínio...",
  "sql": "SELECT ... FROM ...",
  "confidence": "high|medium|low"
}
```

## Configuração

### Variáveis de Ambiente (.env)

```
GOOGLE_API_KEY=sua_chave_aqui
```

## Troubleshooting

### Erro: "API Key não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme que a chave está correta em `GOOGLE_API_KEY`
