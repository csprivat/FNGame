"""
Projeto: FNGame - Bot Educacional Anti Fake News
Autor: Comunidade Raul Hacker Club / UFBA

Descrição:
Este script faz parte do projeto FNGame, uma iniciativa educacional
para combater a desinformação através de um quiz interativo.
Os dados utilizados são obtidos de fontes públicas com fins didáticos.

Licença:
Este projeto é licenciado sob a Licença Pública Geral Affero GNU v3 (AGPLv3).
Qualquer redistribuição deve manter o código-fonte aberto e não pode ter fins comerciais.
Mais informações: https://www.gnu.org/licenses/agpl-3.0.html
"""

import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_ENV_VARS = [
    "DB_HOST",
    "DB_PORT",
    "DB_USER",
    "DB_PASSWORD",
    "DB_NAME",
    "TELEGRAM_BOT_TOKEN"
]

missing = [var for var in REQUIRED_ENV_VARS if not os.getenv(var)]

if missing:
    print("❌ Variáveis ausentes no .env:")
    for var in missing:
        print(f" - {var}")
    exit(1)
else:
    print("✅ Todas as variáveis de ambiente estão configuradas corretamente.")