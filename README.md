# BetSavior

Assistente de IA para apoiar pessoas em recuperação de vício em apostas, oferecendo chat com memória, análise de uploads e acompanhamento de progresso.

## Estrutura do projeto
```
/betsavior
  /api            # Backend FastAPI
    main.py       # Inicialização da aplicação
    /routes       # Rotas da API
      chat.py
      uploads.py
      users.py
  /models         # Modelos de banco (SQLAlchemy)
    user.py
    session.py
    upload.py
  /utils          # Utilitários (OCR, cliente OpenAI)
    ocr.py
    openai_client.py
  /frontend       # Placeholder para frontend React
  /db             # Artefatos de banco
    schema.sql
.env.example       # Variáveis de ambiente
requirements.txt   # Dependências
```

## Requisitos
- Python 3.11+
- PostgreSQL disponível e acessível
- Tesseract OCR instalado para processamento de imagem

## Configuração rápida
1. Copie o arquivo `.env.example` para `.env` e preencha as variáveis.
2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Aplique o schema inicial no banco PostgreSQL (ou use `Base.metadata.create_all` na inicialização):
   ```bash
   psql "$DATABASE_URL" -f betsavior/db/schema.sql
   ```
4. Execute o servidor:
   ```bash
   uvicorn betsavior.api.main:app --reload
   ```

## Endpoints iniciais
- `POST /chat` – envia mensagem ao assistente, grava no histórico e retorna resposta.
- `POST /uploads` – recebe arquivo de imagem (multipart/form-data), processa via OCR e salva no banco.
- `GET /users/{user_id}/progress` – retorna indicadores básicos do usuário (dias sem apostar, mensagens e uploads).
