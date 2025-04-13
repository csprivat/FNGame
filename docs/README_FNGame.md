# 🧠 FNGame – Anti Fake News

## ✅ Atualizações recentes

### 12/04/2025 – Otimização de desempenho

**Arquivo alterado:** `db.py`

**Modificações realizadas:**
- Substituição do uso de `ORDER BY RAND()` na função `fetch_questions()` por `ORDER BY id DESC LIMIT 100` para melhorar performance.
- Implementação de sorteio aleatório das perguntas via `random.shuffle()` no Python.
- Redução para 50 perguntas após o shuffle, preservando comportamento anterior.
- Adição do import de `random` ao início do arquivo.
- Compatibilidade total preservada com `FNGame-1.4.py`.

**Recomendação:** executar o seguinte comando SQL para garantir índice no campo `theme_id`:
```sql
CREATE INDEX idx_theme_id ON questions(theme_id);
```

---

