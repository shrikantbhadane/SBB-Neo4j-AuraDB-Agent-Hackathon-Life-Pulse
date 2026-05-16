# SBB-Neo4j-AuraDB-Agent-Hackathon-Life-Pulse

This repository is part of the **Neo4j AuraDB Agent Hackathon**. It uses a Kaggle dataset on life expectancy and health spending covering the period from **1960 to today**, sourced from the World Bank Open Data, the World Health Organization (WHO) Global Health Observatory, and OECD Health Statistics.

---

## 🤖 Agent Name

**Aura-Health-Bot**

---

## 💡 What It Does

**Aura-Health-Bot** is an intelligent conversational agent powered by Neo4j AuraDB. It loads global health data spanning from **1960 to the present day** (with periodic refreshes as new data becomes available), drawing from three authoritative sources:

- 🌍 **World Bank Open Data** — macroeconomic indicators, healthcare expenditure, and population statistics.
- 🏥 **World Health Organization (WHO) Global Health Observatory** — disease burden, mortality rates, life expectancy, and health system performance metrics.
- 📊 **OECD Health Statistics** — detailed health spending, workforce, and outcomes data for OECD member countries.

The agent is designed to serve a wide range of users, including:

| User Group | Use Case |
|---|---|
| **Healthcare Professionals** | Benchmark health outcomes and spending across countries and years |
| **Scientists & Researchers** | Explore longitudinal trends in longevity, disease, and investment |
| **Policymakers** | Evaluate the return on investment of healthcare expenditure |
| **Students & Educators** | Visualize six decades of global health data interactively |
| **General Public** | Ask plain-language questions and receive fast, accurate answers |

Users can ask questions in natural language such as:
- *"Which countries have the highest life expectancy relative to their healthcare spending?"*
- *"How has life expectancy changed in Sub-Saharan Africa since 1980?"*
- *"What is the average health expenditure per capita in OECD countries over the last decade?"*

The bot translates these questions into graph traversals across Neo4j AuraDB, returning accurate, contextual answers quickly and efficiently.

---

## 🗃️ Dataset and Why a Graph Fits

### About the Dataset

#### Context

Does higher spending always lead to a longer life? This dataset explores the complex relationship between **national healthcare expenditure** and **life expectancy**. Spanning over **six decades** (1960 to today — more than 65 years of data), it allows for a deep dive into how medical advancements, economic shifts, and policy changes have influenced human longevity across different continents and income levels.

#### Sources

The data is aggregated from major global repositories:

- **World Bank Open Data** — [https://data.worldbank.org](https://data.worldbank.org)
- **WHO Global Health Observatory** — [https://www.who.int/data/gho](https://www.who.int/data/gho)
- **OECD Health Statistics** — [https://www.oecd.org/health/health-data.htm](https://www.oecd.org/health/health-data.htm)

#### Inspiration

This dataset was compiled to help researchers and students visualize the **"Return on Investment" in healthcare**. It serves as a foundation for analyzing why some nations achieve high longevity with modest budgets, while others spend significantly more for similar or lesser results.

---

### Why a Graph Database Fits This Dataset

A **graph database like Neo4j AuraDB** is an ideal fit for this dataset for several reasons:

1. **Highly Connected Data**: The dataset involves deeply interconnected entities — countries, regions, income groups, years, health metrics, and expenditure figures. These natural relationships are cumbersome to model in relational tables but are first-class citizens in a graph.

2. **Traversal-Heavy Queries**: Questions like *"Find all low-income countries where life expectancy increased despite low healthcare spending"* require multi-hop traversals across time, geography, and economic groupings — operations that graph databases handle natively and efficiently.

3. **Temporal Patterns**: Tracking how a country's health metrics evolve over 60+ years is naturally represented as a chain of time-linked nodes, enabling intuitive time-series analysis without complex SQL date joins.

4. **Comparative Analysis**: Comparing countries within the same income group, continent, or WHO region is straightforward using graph relationships rather than repeated JOIN operations.

5. **Flexible Schema**: As new data sources or metrics are added (e.g., pandemic indicators, mental health data), the schema-optional nature of Neo4j allows seamless extension without costly migrations.

6. **AI/Agent Integration**: Neo4j AuraDB's vector index and graph traversal capabilities make it easy to build LLM-powered agents that can answer complex, contextual queries over the health data with high accuracy.

**Example Graph Model:**

```
(Country)-[:HAS_METRIC {year}]->(HealthMetric)
(Country)-[:BELONGS_TO]->(Region)
(Country)-[:CLASSIFIED_AS]->(IncomeGroup)
(HealthMetric)-[:REPORTED_BY]->(DataSource)
```

This model allows Aura-Health-Bot to answer questions by traversing relationships between countries, their health indicators, time periods, and data provenance — something a flat table structure simply cannot do as elegantly.

---

## 📸 Screenshots

### Agent in the Aura Console

> *(Screenshot will be attached here soon.)*

### Agent in Action (Demo)

> *(Screenshot or short demo video will be attached here soon.)*

---

## 🔗 Agent Link

> *(Link to the live agent will be shared here once available.)*

---

## 📁 Repository Structure

```
SBB-Neo4j-AuraDB-Agent-Hackathon-Life-Pulse/
├── README.md          # Project documentation (this file)
```

---

## 🏆 Hackathon Submission

This project is submitted as part of the **Neo4j AuraDB Agent Hackathon**. The goal is to demonstrate how Neo4j AuraDB, combined with an AI-powered agent, can unlock insights from complex, highly connected health and economic datasets.
