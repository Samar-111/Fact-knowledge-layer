# Fact Knowledge Layer ("FactGraph Engine")

> *A system for extracting, grounding, comparing, and contextually reconciling numerical and semantic facts across complex PDF documents.*

---

## 📌 Project Overview & Problem Explanation

### What Does This Project Do?
Important economic, financial, and organizational facts are scattered across hundreds of pages in unstructured documents (e.g. Economic Surveys, Central Bank Annual Reports, IMF Country Assessments). When analyzing multiple documents, researchers encounter three main challenges:
1. **Fact Fragmentation & Variation**: The same metric is reported in different formats, wording, or tables (e.g., "Real GDP growth is estimated at 6.4%" vs "GDP grew by 6.5%").
2. **Fact Conflicts & Ambiguity**: Numbers appear to contradict one another across sources.
3. **Contextual Nuances**: Many apparent contradictions are actually both true when accounting for metadata context—such as release timeframe, estimate stage (*First Advance Estimates* vs *Second Advance Estimates*), metric scope (*Gross FDI* vs *Net FDI*), or geographic coverage.

### Core Solution
The **Fact Knowledge Layer** is an end-to-end pipeline that:
- **Extracts Atomic Facts**: Converts raw text/tables into structured entities (`subject`, `metric_name`, `value`, `unit`, `time_period`, `estimate_stage`, `geographic_scope`).
- **Source Evidence Grounding**: Every extracted fact is strictly anchored to its source PDF filename, exact page number, and verbatim excerpt text.
- **Automated Relationship Engine**: Compares facts across documents to automatically classify them as:
  - **Corroborated**: Facts that validate each other across independent sources.
  - **Contradicted**: Direct conflicts under identical metric and timeline conditions.
  - **Contextually Reconciled**: Apparent discrepancies explained by time horizon, estimate stage, units, or scope differences.
  - **Extraction/Reasoning Failure**: Flags low-confidence or ambiguous extractions (e.g. Gross vs Net metric confusion) and applies self-correction logic.
- **Interactive UI & REST API**: Provides a modern React web dashboard and FastAPI endpoints to upload custom PDFs dynamically and explore relationships visually.

---

## 🚀 Setup and Run Instructions

### Prerequisites
- **Python 3.10+** installed
- **Node.js 18+** & `npm` installed

### Quick Start (Single Command)

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Samar-111/Fact-knowledge-layer.git
   cd Fact-knowledge-layer
   ```

2. **Install Dependencies**:
   - **Backend Dependencies**:
     ```bash
     pip install -r backend/requirements.txt
     ```
   - **Frontend Dependencies**:
     ```bash
     cd frontend
     npm install
     cd ..
     ```

3. **Launch Application**:
   ```bash
   python run.py
   ```
   *The launcher will automatically start the FastAPI backend server on `http://127.0.0.1:8000` and the React frontend on `http://localhost:5173`.*

4. **Access in Browser**:
   - **Web Interface**: [http://localhost:5173](http://localhost:5173)
   - **Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🎥 Video Demo Link

- **Demo Video (3 Minutes or less)**: [Watch Product Video Demo Here](https://youtu.be/your-demo-video-link-placeholder) *(Replace with actual video link prior to final submission)*

---

## 📊 The Four Required Cases (Benchmark Dataset)

Our system processes the three starter documents (*Economic Survey 2024-25*, *RBI Annual Report 2024-25*, and *IMF Country Report No. 25/314*) and extracts the following benchmark cases:

### Case 1: Corroborated Fact Across Documents
- **Metric**: Headline CPI Inflation for FY2024-25 (**4.6%**)
- **Source Evidence**:
  - **Economic Survey 2024-25 (Page 25)**: *"Retail headline inflation, as measured by the change in the Consumer Price Index (CPI), has softened to an average of 4.6 per cent in 2024-25 compared to 5.4 per cent in FY24."*
  - **RBI Annual Report 2024-25 (Page 9)**: *"Headline inflation moderated to an average of 4.6 per cent during 2024-25 from 5.4 per cent in the previous year..."*
  - **IMF Country Report 2025 (Page 5, Table 1)**: *"Consumer prices - Combined (period average, percent change): 2023/24 = 5.4%, 2024/25 Est. = 4.6%."*
- **System Reasoning**: All three independent institutional reports (Ministry of Finance, Reserve Bank of India, and International Monetary Fund) corroborate that India's average retail CPI inflation for FY2024-25 stood at **4.6%**, down from 5.4% in FY2023-24.

---

### Case 2: Genuine or Likely Contradiction (Forecast Divergence)
- **Metric**: Real GDP Growth Forecast for FY2025-26 (**6.3%-6.8% vs 6.5% vs 6.6%**)
- **Source Evidence**:
  - **Economic Survey 2024-25 (Page 33)**: *"On balance of these considerations, we expect that the growth in FY26 would be between 6.3 and 6.8 per cent."*
  - **RBI Annual Report 2024-25 (Page 17)**: *"Taking into account these factors, real GDP growth for 2025-26 is projected at 6.5 per cent, with risks evenly balanced."*
  - **IMF Country Report 2025 (Page 3 & 13)**: *"Under the baseline assumption of prolonged 50 percent U.S. tariffs, real GDP is projected to grow at 6.6 percent in FY2025/26."*
- **System Reasoning**: Under identical timeframes (FY2025-26), the institutions project different point growth estimates: MoF provides a range of 6.3%-6.8%, RBI projects 6.5%, and IMF projects 6.6%. This reflects a genuine policy/model contradiction stemming from different underlying econometric baseline assumptions regarding global tariff impacts and monsoon transmission.

---

### Case 3: Apparent Contradiction Explained by Context (Time / Release Stage)
- **Metric**: India Real GDP Growth for FY2024-25 (**6.4% vs 6.5%**)
- **Source Evidence**:
  - **Economic Survey 2024-25 (Page 4)**: *"As per the first advance estimates of national accounts, India's real GDP is estimated to grow by 6.4 per cent in FY25."*
  - **RBI Annual Report 2024-25 (Page 6 & 8)**: *"Although real gross domestic product (GDP) growth moderated to 6.5 per cent in 2024-25, India remained the fastest growing major economy. (Footnote 3: Based on Second Advance Estimates released Feb 28, 2025)."*
- **System Reasoning**: The apparent discrepancy between 6.4% and 6.5% is **reconciled by context (Release Date & Estimate Stage)**. The Economic Survey was drafted using MoSPI's *First Advance Estimates (FAE)* released in early January 2025 (6.4%), whereas the RBI Annual Report incorporated MoSPI's revised *Second Advance Estimates (SAE)* published on February 28, 2025 (6.5%), which integrated updated Q3 QNA data.

---

### Case 4: Extraction / Reasoning Failure & Mitigation
- **Failure Scenario**: Disambiguating **Gross FDI Inflows ($81.0B)** vs **Net FDI Inflows ($0.4B)** for FY2024-25.
- **Initial Failure Mode**: Naive LLM or regex extractions extracted "$81.0 Billion" and "$0.4 Billion" as contradictory FDI figures for FY25 from Page 85 of the RBI Report, or misattributed repatriation subtractions ($51.5 Billion) as a negative growth rate (-96%).
- **Handling & Mitigation**: Implemented a **Multi-Stage Fact Sanitizer and Accounting Scope Verifier**. The system:
  1. Detects metric scope tags (`Gross_Inflow` vs `Net_Inflow` vs `Repatriation`).
  2. Validates the accounting identity equation: $\text{Net FDI} = \text{Gross Inflows} - \text{Repatriations/Disinvestments} - \text{Outward FDI}$.
  3. Automatically re-classifies the relationship from a naive "Contradiction" alert to a **Validated Scope Decomposition**, flagging low-confidence raw extractions and preventing false-positive contradiction alerts.

---

## 🏗️ Architecture, Approach & Engineering Decisions

```
┌─────────────────┐       ┌──────────────────────┐       ┌────────────────────────┐
│  Uploaded PDFs  │ ────> │  PDF Processor       │ ────> │  Fact Extractor        │
│  (Dynamic input)│       │  (pypdf / pdfplumber)│       │  (Hybrid LLM + Rules)  │
└─────────────────┘       └──────────────────────┘       └────────────────────────┘
                                                                     │
                                                                     ▼
┌─────────────────┐       ┌──────────────────────┐       ┌────────────────────────┐
│  React Web UI   │ <──── │  FastAPI REST Server │ <──── │  Reconciliation Engine │
│  (Tailwind/Vite)│       │  (Endpoints & Graph) │       │  (NetworkX + SQLite)   │
└─────────────────┘       └──────────────────────┘       └────────────────────────┘
```

### Important Engineering Decisions & Trade-offs

1. **Hybrid LLM + Deterministic Fallback Engine**:
   - *Decision*: Combine Google Gemini 2.5 Flash API with a zero-dependency NLP Regex & Pattern Matcher.
   - *Trade-off*: While pure LLM extraction handles unstructured prose gracefully, API rate limits or missing API keys can break evaluation. The hybrid fallback guarantees 100% offline, reproducible execution without external API dependencies.

2. **Rich Metadata Entity Representation**:
   - *Decision*: Facts are represented as structured schemas with explicit `estimate_stage`, `time_period`, `unit`, `geographic_scope`, and `exact_quote`.
   - *Trade-off*: Increases extraction complexity compared to simple key-value pairs, but enables automatic contextual reconciliation (Case 3) and scope disambiguation (Case 4).

3. **Lightweight Portable Storage (SQLite + NetworkX)**:
   - *Decision*: Use SQLite and NetworkX rather than heavy graph databases (e.g. Neo4j).
   - *Trade-off*: Keeps system deployment trivial (runs in a single Python process), while preserving full graph query capability for nodes and relationship edges.

### AI Tools Used
- **Google Antigravity AI Agent** for pair-programming and architecture structuring.
- **Google Gemini 2.5 Flash API** for structured JSON extraction.
- **Python NLP Heuristics** for regex metric pattern matching.

---

## ⚠️ Limitations and Next Steps

### Current Limitations
- **Visual Chart Reading**: OCR/text parsing from graphic charts (e.g. dot plots or stacked bar charts without text labels) can miss raw data points unless OCR text is embedded in PDF layers.
- **Complex Multi-Table Joins**: Cross-page table continuations occasionally lose column header context if tables break across page boundaries.

### Next Steps & Future Extensions (Brownie Points)
1. **Dynamic Schema Evolution**: Allow the LLM to dynamically invent new metric taxonomies and attribute properties as new types of documents (e.g. legal contracts or ESG reports) are uploaded.
2. **Incremental Knowledge Graph Updates**: Perform graph diffing to update existing node links without re-computing the full knowledge layer when a new PDF is added.
3. **Vector Embeddings for Semantic Fact Search**: Integrate FAISS / ChromaDB vector search to allow semantic retrieval of facts via natural language queries.

---

## ✅ Submission Checklist Verification

- [x] Project runs from instructions and accepts new PDFs dynamically through UI and REST API.
- [x] Extracted results contain grounded facts, source document evidence, page numbers, and exact verbatim quotes.
- [x] System demonstrates the 4 required cases (Corroboration, Contradiction, Contextual Reconciliation, Failure Handling).
- [x] Documented approach, engineering trade-offs, architecture, and included video demo link section.

---

## 📄 License & Attribution
Built with Python, FastAPI, React, and Tailwind CSS.
