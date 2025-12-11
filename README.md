# 🧪 Projeto de Fuzzing em APIs REST

Este projeto foi desenvolvido para a disciplina de **Teste de Validação de Software** e tem como objetivo aplicar três abordagens de fuzzing em APIs REST:

* **Random / Generation-based (Black-box)**
* **Schema-based Fuzzing** (utilizando **Schemathesis**)
* **Mutation-based Fuzzing** (utilizando **Swagger UI**)

As três técnicas foram executadas sobre a API pública **Swagger Petstore**, permitindo comparar o comportamento das abordagens e observar como a complexidade e o tipo de interação da API influenciam o resultado.

---

## 📌 1. Arquitetura do Projeto

O repositório contém:

* Scripts de execução para o fuzzing Random
* Execução via Schemathesis para Schema-based
* Execução manual via Swagger UI para Mutation-based

---

## 🎯 2. Objetivo

Aplicar três abordagens de fuzzing para avaliar:

* Robustez da API
* Tipos de erros encontrados
* Diferenças entre técnicas (random, mutation e schema-based)
* Relação entre complexidade da API e eficácia do fuzzer

---

## ⚙️ 3. Abordagens Utilizadas

### **3.1 Random / Generation-based Fuzzing**

**Descrição:**
Gera inputs totalmente aleatórios e envia requisições sem considerar a estrutura da API.

**Como foi feito:**

* Foi criado um script em **JavaScript** que envia requisições HTTP com dados aleatórios.
* Os endpoints testados incluem POST, PUT, GET e DELETE da API Petstore.
* O foco foi observar códigos inesperados (4xx/5xx), erros 415, falhas de processamento etc.

**Como executar:**

```bash
npm install axios @faker-js/faker
node fuzz-petstore.js
```

---

### **3.2 Schema-based Fuzzing (Schemathesis)**

**Ferramenta:** `schemathesis`

**Descrição:**
Utiliza o **OpenAPI Specification (Swagger)** para gerar requisições válidas com base no esquema da API.

**Por que usar?**

* A ferramenta consegue entender formatos, tipos de dados e dependências.
* Gera sequências de chamadas válidas.
* Encontra falhas estruturais mais profundas.

**Como foi feito:**
Foi usado o comando:

```bash
schemathesis run https://petstore.swagger.io/v2/swagger.json
```

**Como instalar:**

```bash
pip install schemathesis
```

**Como executar:**

```bash
schemathesis run https://petstore.swagger.io/v2/swagger.json --checks all --report report.json
```

---

### **3.3 Mutation-based Fuzzing (Swagger UI)**

**Ferramenta:** Swagger UI

**Descrição:**
A abordagem mutation-based modifica entradas válidas para gerar variações inesperadas.

**Como foi feito:**
* Foram enviadas requisições válidas e, em seguida, mutações manuais:

  * Strings muito longas
  * Tipos inesperados
  * Campos omitidos
  * Valores fora do padrão
* Registramos como a API reagiu a entradas parcialmente válidas.

**Por que mutation-based?**
Permite observar falhas de validação e inconsistências lógicas quando a API recebe algo quase correto.

---

---

## 📝 5. Relatórios

O projeto inclui relatórios que descrevem:

* Metodologia usada
* Execução dos testes
* Análise comparativa dos resultados
* Trabalhos relacionados
* Referências em ABNT

---

## 🚀 6. Como Reproduzir o Projeto

### **Requisitos:**

* Node.js (para Random)
* Python 3.9+ (para Schemathesis)
* Navegador (para Swagger UI)

### **Passo a passo:**

1. Clone o repositório:

```bash
git clone https://github.com/mairatscabral/testedesoftware
cd testedesoftware
```

2. Execute o fuzzer Random:

```bash
node fuzz-petstore.js
```

---

## 📚 8. Referências

As referências completas em ABNT estão no relatório principal, seção 9.

