# Random / Generation-Based Fuzzing para APIs REST

Este repositório contém a implementação completa de testes fuzzing
generation-based aplicados a três cenários diferentes:

1. **API simples** (Swagger Petstore)
2. **API CRUD de médio porte** (FastAPI em Docker)
3. **API com autenticação básica**

Além disso, o repositório inclui:
- Scripts dos fuzzers
- Ambiente CRUD em FastAPI
- Notebook de análise de logs

## 🎯 Objetivo

Testar se o desempenho da abordagem random/generation-based
varia conforme a complexidade da API:

- Estrutura simples (Petstore)
- CRUD com múltiplas operações
- API protegida por autenticação

## 🚀 Rodando a API CRUD local

```bash
cd crud-api
docker compose up --build
```

A API ficará disponível em:

```
http://localhost:8000
```

## 🔥 Rodando os fuzzers

### Petstore
```bash
python fuzzers/fuzzer_petstore.py
```

### CRUD (local)
```bash
python fuzzers/fuzzer_crud.py
```

### Auth Básica
```bash
python fuzzers/fuzzer_auth.py
```

## 📊 Analisando logs

Abra o notebook:

```
analysis/analyze_logs.ipynb
```

E coloque seus logs em: `sample_logs/`

## 📄 Licença
MIT
