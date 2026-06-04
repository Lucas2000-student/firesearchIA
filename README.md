# firesearchIA

API de inferência de risco de incêndio florestal para leitura de sensores IoT. Projeto desenvolvido para **FIAP — Análise e Desenvolvimento de Sistemas — 2026/1**.

**Resumo:** modelo Random Forest treinado com o dataset "Algerian Forest Fires" (UCI). A API recebe observações de sensores (temperatura, umidade, vento, chuva, CO2, fumaça) e retorna uma predição (`fire` / `not fire`), um `score` de risco (0–100) e um `nivel` categórico (BAIXO, MEDIO, ALTO).

**Equipe**

- **RM553043:** Daniel Kendi — Banco de dados e .Net
- **RM560179:** Lucas da Ressurreição — Java e IOT
- **RM560560:** Jonas Kimio — Mobile
- **RM560475:** Marcos Vinicius — DevOps e QA

**Conteúdo do repositório**

- `Algerian_forest_fires_dataset.csv` — dataset original (UCI)
- `training_iot.ipynb` — notebook de treinamento e experimentos
- `inference.py` — aplicação Flask para inferência
- `modelo.pkl`, `features.pkl` — artefatos do modelo (não incluídos no repositório)
- `requirements.txt` — dependências

**Requisitos**

- Python 3.8+ (recomendado 3.10+)
- pacotes: ver `requirements.txt`

Instalação rápida:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Observação: garanta que os arquivos `modelo.pkl` e `features.pkl` estejam presentes na raiz do projeto antes de iniciar a API.

Como executar a API (desenvolvimento):

```bash
python inference.py
```

Por padrão a aplicação ouve em `0.0.0.0:8001` (variável de ambiente `PORT` pode ser usada).

**Endpoints**

- `GET /health`
  - Retorno: `{"status": "ok", "model": "Algerian Forest Fires RF"}`

- `POST /predict`
  - Recebe JSON com as leituras de sensores. Campos aceitos (exemplos e valores padrão no mapeamento dentro de `inference.py`):
    - `temperatura` (float)
    - `umidade` (float)
    - `vento` (float)
    - `chuva` (float)
    - `co2` (float)
    - `fumaca` (float)

Exemplo de requisição:

```bash
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{"temperatura":38, "umidade":25, "co2":1200, "fumaca":70, "vento":20, "chuva":0}'
```

Exemplo de resposta (JSON):

```json
{
  "prediction": "fire",
  "score": 100.0,
  "nivel": "ALTO",
  "prob_fire": 100.0,
  "features_usadas": {
    "Temperature": 38.0,
    "RH": 25.0,
    "Ws": 20.0,
    "Rain": 0.0,
    "FFMC": 86.4,
    "DMC": 13.0,
    "DC": 80.0
  }
}
```

Projeto criado para o desafio acadêmico FIAP 2026/1.