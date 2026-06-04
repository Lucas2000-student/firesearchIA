# firesearchIA

API de inferência de risco de incêndio florestal baseada em Machine Learning, desenvolvida para o projeto **Global Solution 2026/1 — FIAP**.

## Equipe

| RM | Nome | Matéria
|---|---|
| RM553043 | Daniel Kendi | Banco de dados e .Net
| RM560179 | Lucas da Ressurreição | Java e IOT
| RM560560 | Jonas Kimio | Mobile
| RM560475 | Marcos Vinicius | DevOps e QA

## Sobre

Modelo treinado com o **Algerian Forest Fires Dataset** (UCI Machine Learning Repository) utilizando **Random Forest Classifier**, com acurácia de **95.92%**.

A API recebe leituras de sensores IoT e retorna o nível de risco de incêndio (ALTO, MEDIO, BAIXO) e um score de 0 a 100.

## Endpoints

### `POST /predict`
Recebe dados de sensores e retorna a predição de risco.

**Body:**
```json
{
  "temperatura": 38,
  "umidade": 25,
  "co2": 1200,
  "fumaca": 70,
  "vento": 20,
  "chuva": 0
}
```

**Resposta:**
```json
{
  "prediction": "fire",
  "nivel": "ALTO",
  "score": 100.0,
  "prob_fire": 100.0,
  "features_usadas": { ... }
}
```

### `GET /health`
Verifica se a API está no ar.

## Tecnologias

- Python 3.12
- Flask 3.0
- Scikit-learn 1.3
- Dataset: Algerian Forest Fires (243 amostras)

---

**FIAP — Análise e Desenvolvimento de Sistemas — 2026/1**