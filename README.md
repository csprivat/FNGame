# 🧠 FNGame – Quiz Anti Fake News

Projeto educacional interativo que utiliza um bot no Telegram para promover o pensamento crítico e o combate à desinformação por meio de quizzes temáticos.

---

## 🚀 Visão Geral

O FNGame é um bot gamificado, que apresenta perguntas de múltipla escolha com base em notícias verdadeiras e falsas. O objetivo é estimular a reflexão crítica e fornecer materiais confiáveis para o aprendizado.

---

## 🗂️ Estrutura de Arquivos

```
.
├── FNGame-1.4.py           # Código principal do bot Telegram
├── db.py                   # Funções de acesso ao banco de dados MariaDB
├── FNGame_scraper.py       # Raspador de perguntas a partir do Boatos.org
├── check_env.py            # Verificador de variáveis de ambiente (.env)
├── .env.example            # Exemplo de configuração de variáveis de ambiente
├── requirements.txt        # Dependências do projeto
├── Dockerfile              # Imagem para rodar o bot
├── docker-compose.yml      # Orquestração de app + banco
└── roadmap_anti_fake_news.md # Planejamento do projeto
```

---

## 📊 Funcionalidades

- Escolha de temas com `/temas`
- Perguntas aleatórias via banco MariaDB
- Pontuação e feedback pedagógico por desempenho
- Ranking com `/ranking`
- Comando `/about` para exibir informações
- Raspador de perguntas: `FNGame_scraper.py`

---

## 🎯 Roadmap (v1.4)

- [x] Integração com banco de dados MariaDB
- [x] Escolha de temas
- [x] Pontuação por sessão e ranking
- [x] Feedback por desempenho com links didáticos
- [x] Comando `/reiniciar`, `/temas`, `/pontuacao`, `/ranking`
- [x] Fallback de perguntas offline (JSON – futura versão)

Ver detalhes em [`roadmap_anti_fake_news.md`](./roadmap_anti_fake_news.md)

---

## ⚙️ Instalação Manual

### 1. Requisitos

- Python 3.11+
- MariaDB (pode ser container ou local)
- `pip install -r requirements.txt`

### 2. Configuração

Crie um arquivo `.env` com o seguinte conteúdo:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=usuario
DB_PASSWORD=senha
DB_NAME=anti_fakenews_db
TELEGRAM_BOT_TOKEN=sua_chave_aqui
```

Valide com:

```bash
python check_env.py
```

### 3. Executar o bot

```bash
python FNGame-1.4.py
```

## 📦 Como clonar e executar

```bash
git clone https://github.com/SEU_USUARIO/FNGame.git
cd FNGame
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env
python FNGame-1.4.py
```

---

## 📜 Licença

Este projeto está licenciado sob AGPLv3 – [GNU Affero General Public License v3.0](https://www.gnu.org/licenses/agpl-3.0.html)

Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed.

---

## 🤝 Como contribuir

Contribuições são bem-vindas! Leia o [guia de contribuição](CONTRIBUTING.md) para saber como colaborar com o FNGame.

---

## 🌐 Código de Conduta

Para garantir um ambiente acolhedor e respeitoso, seguimos o [Código de Conduta](CODE_OF_CONDUCT.md) baseado no Contributor Covenant.

---

## 👥 Autoria

Desenvolvido por:
- Criador e principal desenvolvedor: Cristian Privat
- Apoio: Ricardo Andrade
