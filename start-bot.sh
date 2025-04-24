#!/bin/bash

source ~/www/faleserio/venv/bin/activate
cd ~/www/faleserio

# Verifica se o processo já está rodando
if pgrep -f "python FNGame-1.4.py" > /dev/null; then
    echo "FaleSério já está rodando. Nenhuma nova instância será iniciada."
else
    echo "Iniciando FaleSério..."
    nohup python FNGame-1.4.py > faleserio.log 2>&1 &
fi

