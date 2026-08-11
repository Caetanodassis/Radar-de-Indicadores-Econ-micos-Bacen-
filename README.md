# 📊 Radar de Indicadores Econômicos — Bacen

> Pipeline automatizado de coleta e tratamento de indicadores macroeconômicos oficiais (Selic, IPCA, Dólar) via API do Banco Central, aplicando **arquitetura medalhão (Bronze → Silver → Gold)**, com histórico acumulando organicamente ao longo do tempo.

---

## 🎯 Objetivo do Projeto

Simular, num ambiente pessoal, o tipo de pipeline de dados que um banco usa internamente para monitorar indicadores macroeconômicos — unindo **automação** (coleta agendada via API), **engenharia de dados** (arquitetura em camadas, versionamento de dados brutos) e **entrega analítica** (indicadores tratados e prontos para BI).

O projeto foi pensado para treinar, na prática:
- Consumo de APIs públicas e tratamento de dados semi-estruturados (JSON);
- Boas práticas de arquitetura de dados (separação em camadas, dados brutos nunca sobrescritos);
- Automação de pipelines (execução agendada, sem intervenção manual);
- Conexão direta com o domínio bancário/financeiro — área de atuação atual do autor.

---

## 🏗️ Arquitetura (Medalhão)

```
API SGS (Banco Central)
        │
        ▼
┌───────────────┐
│    BRONZE     │  Dados brutos, exatamente como a API retorna (JSON)
│               │  Particionado por indicador e data de coleta
└───────┬───────┘
        ▼
┌───────────────┐
│    SILVER     │  Tipos tratados (datas, floats), coluna de indicador
│               │  Salvo em Parquet (fallback CSV)
└───────┬───────┘
        ▼
┌───────────────┐
│     GOLD      │  🔜 Em desenvolvimento
│               │  Indicadores consolidados + métricas derivadas,
│               │  prontos para consumo em BI
└───────────────┘
```

### Por que essa separação importa
- **Bronze nunca é alterado** — se um bug for encontrado na camada Silver, é possível reprocessar do zero sem precisar chamar a API de novo (poupa tempo e evita dependência de disponibilidade externa).
- **Silver** padroniza tipos e formatos, mas ainda é granular (uma tabela por indicador).
- **Gold** vai consolidar tudo num formato analítico, já com as contas de negócio prontas.

---

## 🗃️ Fonte de Dados

**API SGS (Sistema Gerenciador de Séries Temporais) — Banco Central do Brasil**
Pública, gratuita, sem necessidade de autenticação.

```
https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados
```

| Indicador | Código SGS |
|---|---|
| Selic (meta) | `432` |
| IPCA (variação mensal) | `433` |
| Dólar comercial (venda) | `1` |

Período coletado: últimos 10 anos a partir da data de execução (janela móvel).

---

## 🛠️ Stack Técnica

- **Linguagem:** Python
- **Coleta:** `requests`
- **Tratamento:** `Pandas`
- **Armazenamento Silver:** Parquet (`pyarrow`, com fallback automático para CSV se a lib não estiver instalada)
- **Camada Gold:** em definição (provavelmente Parquet consolidado + views para BI)
- **Automação:** 🔜 a definir (GitHub Actions ou APScheduler)
- **Visualização final:** Power BI (planejado)

---

## 📌 Status Atual do Projeto

- [x] **Bronze** — script de ingestão via API SGS (`ingestao_bronze.py`), com particionamento por indicador e data de coleta
- [x] **Silver** — script de tratamento (`processamento_silver.py`): conversão de tipos, tratamento de datas, adição de coluna `indicador`
- [ ] **Gold** — consolidação de todos os indicadores numa tabela única, com cálculos derivados (variação % mês a mês, média móvel, acumulado 12 meses)
- [ ] Ajuste de dependência: garantir `pyarrow` instalado para que a Silver sempre salve em Parquet (hoje há fallback para CSV quando a lib está ausente)
- [ ] Automação da execução diária (GitHub Actions ou `APScheduler`)
- [ ] Lógica incremental — hoje o pipeline sempre busca a janela completa de 10 anos; próxima versão deve buscar apenas dados novos desde a última coleta
- [ ] Conexão com Power BI / dashboard final
- [ ] Alertas (Telegram/Slack) para variações relevantes nos indicadores

---

## 📂 Estrutura do Repositório

```
radar-de-indicadores-economicos-bacen/
├── README.md
├── ingestao_bronze.py           # Coleta dados da API SGS e salva em bronze/
├── processamento_silver.py      # Lê o bronze do dia, trata e salva em silver/
├── bronze/
│   ├── selic/
│   │   └── AAAA-MM-DD.json
│   ├── ipca/
│   │   └── AAAA-MM-DD.json
│   └── dolar/
│       └── AAAA-MM-DD.json
└── silver/
    ├── selic.parquet
    ├── ipca.parquet            # (ou .csv, se pyarrow não estiver instalado)
    └── dolar.parquet
```

*(camada `gold/` será adicionada na próxima etapa)*

---

## 🚀 Como Rodar (setup atual)

1. Instale as dependências:
   ```bash
   pip install requests pandas pyarrow
   ```
2. Execute a ingestão (camada Bronze):
   ```bash
   python ingestao_bronze.py
   ```
3. Execute o processamento (camada Silver):
   ```bash
   python processamento_silver.py
   ```

> ⚠️ **Atenção:** a Silver só processa o arquivo Bronze do **dia atual** (`data_hoje_arquivo`). Rode os dois scripts na mesma execução/dia, ou ajuste o script para apontar para uma data específica se for reprocessar um dia anterior.

---

## 🗺️ Próximos Passos

1. Construir a camada **Gold**: unir os três Parquets da Silver numa tabela única (formato wide: uma coluna por indicador, uma linha por data), calcular variação percentual e médias móveis
2. Automatizar a execução diária via GitHub Actions
3. Tornar a ingestão **incremental** (buscar só o período novo desde a última coleta, em vez de sempre os últimos 10 anos)
4. Conectar a Gold ao Power BI
5. Adicionar alertas de variação relevante

---

## 👤 Autor

**Vinícius Caetano**
Analista de Dados Jr. | Estudante de ADS
[GitHub](https://github.com/Caetanodassis)