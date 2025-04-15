# -*- coding: utf-8 -*-
"""
Projeto: FNGame - Bot Educacional Anti Fake News
Autor: Cristian Privat
Apoio: Ricardo Andrade

Descrição:
Este script faz parte do projeto FNGame, uma iniciativa educacional
para combater a desinformação através de um quiz interativo.
Os dados utilizados são obtidos de fontes públicas com fins didáticos.

Licença:
Este projeto é licenciado sob a Licença Pública Geral Affero GNU v3 (AGPLv3).
Qualquer redistribuição deve manter o código-fonte aberto e não pode ter fins comerciais.
Mais informações: https://www.gnu.org/licenses/agpl-3.0.html

classifier.py
Módulo responsável por classificar perguntas por categorias usando palavras-chave.
"""

def classificar_categoria_por_keywords(question_text: str, dicionario_temas: dict) -> str:
    """
    Retorna o nome da categoria mais provável com base nas palavras-chave fornecidas.

    :param question_text: Texto da pergunta
    :param dicionario_temas: Dict no formato {'tema': ['palavra1', 'palavra2']}
    :return: Nome do tema mais adequado ou None
    """
    question_lower = question_text.lower()
    for categoria, palavras_chave in dicionario_temas.items():
        for palavra in palavras_chave:
            if palavra.lower() in question_lower:
                return categoria
    return None
