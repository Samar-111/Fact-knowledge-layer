import logging
from app.database import db, FactModel, RelationshipModel

logger = logging.getLogger("sample_data")

def seed_benchmark_dataset():
    doc1_id = "doc_econ_survey_2025"
    doc2_id = "doc_rbi_annual_2025"
    doc3_id = "doc_imf_article_iv_2025"

    db.add_document(
        doc_id=doc1_id,
        title="Economic Survey 2024-25",
        filename="Economic_Survey_2024-25.pdf",
        file_path="starter_docs/Economic_Survey_2024-25.pdf",
        page_count=89
    )

    db.add_document(
        doc_id=doc2_id,
        title="RBI Annual Report 2024-25",
        filename="RBI_Annual_Report_2024-25.pdf",
        file_path="starter_docs/RBI_Annual_Report_2024-25.pdf",
        page_count=100
    )

    db.add_document(
        doc_id=doc3_id,
        title="IMF Country Report No. 25/314 - India Article IV",
        filename="IMF_India_Article_IV_2025.pdf",
        file_path="starter_docs/IMF_India_Article_IV_2025.pdf",
        page_count=95
    )

    facts_data = [
        FactModel(
            id="fact_cpi_es",
            doc_id=doc1_id,
            doc_name="Economic Survey 2024-25",
            subject="Inflation & Prices",
            metric_name="Headline CPI Inflation",
            value=4.6,
            value_text="4.6 per cent",
            unit="%",
            time_period="FY25 (2024-25)",
            estimate_stage="Annual Average Outturn",
            geographic_scope="India",
            page_number=25,
            exact_quote="Retail headline inflation, as measured by the change in the Consumer Price Index (CPI), has softened to an average of 4.6 per cent in 2024-25 compared to 5.4 per cent in FY24.",
            confidence=0.98,
            category="Macroeconomic Indicator",
            extraction_method="NLP Grounding Parser"
        ),
        FactModel(
            id="fact_cpi_rbi",
            doc_id=doc2_id,
            doc_name="RBI Annual Report 2024-25",
            subject="Inflation & Prices",
            metric_name="Headline CPI Inflation",
            value=4.6,
            value_text="4.6 per cent",
            unit="%",
            time_period="FY25 (2024-25)",
            estimate_stage="Official Annual Average",
            geographic_scope="India",
            page_number=9,
            exact_quote="Headline inflation moderated to an average of 4.6 per cent during 2024-25 from 5.4 per cent in the previous year, largely driven by a moderation in core inflation to 3.5 per cent.",
            confidence=0.99,
            category="Macroeconomic Indicator",
            extraction_method="NLP Grounding Parser"
        ),
        FactModel(
            id="fact_cpi_imf",
            doc_id=doc3_id,
            doc_name="IMF Country Report 2025",
            subject="Inflation & Prices",
            metric_name="Headline CPI Inflation",
            value=4.6,
            value_text="4.6 percent",
            unit="%",
            time_period="FY25 (2024-25)",
            estimate_stage="Staff Estimate (Period Average)",
            geographic_scope="India",
            page_number=5,
            exact_quote="Consumer prices - Combined (period average, percent change): 2023/24 = 5.4%, 2024/25 Est. = 4.6%.",
            confidence=0.97,
            category="Macroeconomic Indicator",
            extraction_method="Table Structural Extractor"
        ),

        FactModel(
            id="fact_gdp_fy26_es",
            doc_id=doc1_id,
            doc_name="Economic Survey 2024-25",
            subject="National Growth",
            metric_name="FY26 GDP Growth Projection",
            value=6.55,
            value_text="6.3 to 6.8 per cent",
            unit="%",
            time_period="FY26 (2025-26)",
            estimate_stage="MoF Budget Projection Range",
            geographic_scope="India",
            page_number=33,
            exact_quote="On balance of these considerations, we expect that the growth in FY26 would be between 6.3 and 6.8 per cent.",
            confidence=0.94,
            category="Economic Growth",
            extraction_method="NLP Grounding Parser"
        ),
        FactModel(
            id="fact_gdp_fy26_rbi",
            doc_id=doc2_id,
            doc_name="RBI Annual Report 2024-25",
            subject="National Growth",
            metric_name="FY26 GDP Growth Projection",
            value=6.5,
            value_text="6.5 per cent",
            unit="%",
            time_period="FY26 (2025-26)",
            estimate_stage="MPC Benchmark Projection",
            geographic_scope="India",
            page_number=17,
            exact_quote="Taking into account these factors, real GDP growth for 2025-26 is projected at 6.5 per cent, with risks evenly balanced.",
            confidence=0.96,
            category="Economic Growth",
            extraction_method="NLP Grounding Parser"
        ),
        FactModel(
            id="fact_gdp_fy26_imf",
            doc_id=doc3_id,
            doc_name="IMF Country Report 2025",
            subject="National Growth",
            metric_name="FY26 GDP Growth Projection",
            value=6.6,
            value_text="6.6 percent",
            unit="%",
            time_period="FY26 (2025-26)",
            estimate_stage="IMF Article IV Baseline (Tariff Model)",
            geographic_scope="India",
            page_number=3,
            exact_quote="Under the baseline assumption of prolonged 50 percent U.S. tariffs, real GDP is projected to grow at 6.6 percent in FY2025/26 before moderating to 6.2 percent in FY2026/27.",
            confidence=0.95,
            category="Economic Growth",
            extraction_method="NLP Grounding Parser"
        ),

        FactModel(
            id="fact_gdp_fy25_fae",
            doc_id=doc1_id,
            doc_name="Economic Survey 2024-25",
            subject="National Accounts",
            metric_name="FY25 Real GDP Growth",
            value=6.4,
            value_text="6.4 per cent",
            unit="%",
            time_period="FY25 (2024-25)",
            estimate_stage="First Advance Estimates (MoSPI Jan 2025)",
            geographic_scope="India",
            page_number=4,
            exact_quote="As per the first advance estimates of national accounts, India's real GDP is estimated to grow by 6.4 per cent in FY25.",
            confidence=0.99,
            category="National Accounts",
            extraction_method="NLP Grounding Parser"
        ),
        FactModel(
            id="fact_gdp_fy25_sae",
            doc_id=doc2_id,
            doc_name="RBI Annual Report 2024-25",
            subject="National Accounts",
            metric_name="FY25 Real GDP Growth",
            value=6.5,
            value_text="6.5 per cent",
            unit="%",
            time_period="FY25 (2024-25)",
            estimate_stage="Second Advance Estimates (MoSPI Feb 28, 2025)",
            geographic_scope="India",
            page_number=8,
            exact_quote="Although real gross domestic product (GDP) growth moderated to 6.5 per cent in 2024-25, India remained the fastest growing major economy. (Footnote 3: Based on Second Advance Estimates released Feb 28, 2025).",
            confidence=0.99,
            category="National Accounts",
            extraction_method="NLP Grounding Parser"
        ),

        FactModel(
            id="fact_gross_fdi_rbi",
            doc_id=doc2_id,
            doc_name="RBI Annual Report 2024-25",
            subject="Capital Flow",
            metric_name="Foreign Direct Investment (FDI)",
            value=81.0,
            value_text="$81.0 Billion (Gross Inflows)",
            unit="USD Billion",
            time_period="FY25 (2024-25)",
            estimate_stage="Gross Direct Capital Inflows",
            geographic_scope="India",
            page_number=85,
            exact_quote="Gross foreign direct investment (FDI) inflows remained resilient, rising by 13.7 per cent y-o-y to US$ 81.0 billion during 2024-25.",
            confidence=0.92,
            category="Foreign Investment",
            extraction_method="Table Structural Extractor"
        ),
        FactModel(
            id="fact_net_fdi_rbi",
            doc_id=doc2_id,
            doc_name="RBI Annual Report 2024-25",
            subject="Capital Flow",
            metric_name="Foreign Direct Investment (FDI)",
            value=0.4,
            value_text="$0.4 Billion (Net Inflows)",
            unit="USD Billion",
            time_period="FY25 (2024-25)",
            estimate_stage="Net Balance of Payments Impact",
            geographic_scope="India",
            page_number=85,
            exact_quote="Net FDI flows at US$ 0.4 billion during 2024-25 were, however, below US$ 10.1 billion a year ago, dragged down by higher repatriation/disinvestment ($51.5B) and net outward FDI ($29.2B).",
            confidence=0.88,
            category="Foreign Investment",
            extraction_method="Table Structural Extractor"
        )
    ]

    for f in facts_data:
        db.add_fact(f)

    db.add_relationship(RelationshipModel(
        id="rel_case_1_corroboration",
        fact_a_id="fact_cpi_es",
        fact_b_id="fact_cpi_rbi",
        relationship_type="CORROBORATED",
        reasoning=(
            "DEMONSTRATION CASE 1 (Corroborated Fact Across Documents):\n"
            "Both 'Economic Survey 2024-25' (p. 25) and 'RBI Annual Report 2024-25' (p. 9) "
            "independently state that India's retail headline CPI inflation for FY2024-25 averaged 4.6 per cent, "
            "moderating from 5.4 per cent in FY2023-24. IMF Country Report 2025 (p. 5) further confirms this identical 4.6% figure."
        ),
        context_diff={
            "case_number": 1,
            "title": "Headline CPI Inflation FY25 Corroboration",
            "metric": "Headline CPI Inflation",
            "value_a": "4.6%",
            "value_b": "4.6%",
            "status": "Verified Corroboration across 3 Independent Institutions"
        },
        confidence_score=0.99
    ))

    db.add_relationship(RelationshipModel(
        id="rel_case_2_contradiction",
        fact_a_id="fact_gdp_fy26_es",
        fact_b_id="fact_gdp_fy26_imf",
        relationship_type="CONTRADICTED",
        reasoning=(
            "DEMONSTRATION CASE 2 (Genuine Forecast Contradiction):\n"
            "For the upcoming fiscal year FY2025-26, the Economic Survey (p. 33) projects growth between 6.3% and 6.8% (midpoint ~6.55%), "
            "RBI Annual Report (p. 17) projects 6.5%, while the IMF Country Report (p. 3) projects 6.6% under a baseline tariff scenario. "
            "Under identical metric scopes and target periods, these represent conflicting institutional point forecasts."
        ),
        context_diff={
            "case_number": 2,
            "title": "FY26 Growth Forecast Divergence",
            "metric": "FY26 GDP Growth Projection",
            "value_a": "6.3% - 6.8% (MoF Range)",
            "value_b": "6.6% (IMF Baseline)",
            "status": "Institutional Model & Baseline Policy Contradiction"
        },
        confidence_score=0.93
    ))

    db.add_relationship(RelationshipModel(
        id="rel_case_3_reconciliation",
        fact_a_id="fact_gdp_fy25_fae",
        fact_b_id="fact_gdp_fy25_sae",
        relationship_type="RECONCILED",
        reasoning=(
            "DEMONSTRATION CASE 3 (Apparent Contradiction Explained by Context):\n"
            "Economic Survey 2024-25 (p. 4) states FY25 Real GDP growth is 6.4%, whereas RBI Annual Report 2024-25 (p. 8) states 6.5%.\n"
            "RECONCILIATION: This apparent discrepancy is fully explained by temporal metadata and release stage. "
            "The Economic Survey relied on MoSPI's 'First Advance Estimates (FAE)' published in January 2025 (6.4%). "
            "In contrast, the RBI Annual Report incorporates MoSPI's 'Second Advance Estimates (SAE)' released on Feb 28, 2025 (6.5%), "
            "which integrated revised Q3 actual data. Both numbers are correct within their respective release contexts."
        ),
        context_diff={
            "case_number": 3,
            "title": "FY25 Real GDP Growth (6.4% vs 6.5%)",
            "metric": "Real GDP Growth FY25",
            "fact_a_context": "First Advance Estimates (FAE) - MoSPI Jan 2025",
            "fact_b_context": "Second Advance Estimates (SAE) - MoSPI Feb 28, 2025",
            "reconciliation_key": "Release Stage & Data Horizon Revision"
        },
        confidence_score=0.98
    ))

    db.add_relationship(RelationshipModel(
        id="rel_case_4_failure_handled",
        fact_a_id="fact_gross_fdi_rbi",
        fact_b_id="fact_net_fdi_rbi",
        relationship_type="EXTRACTION_FAILURE",
        reasoning=(
            "DEMONSTRATION CASE 4 (Extraction / Reasoning Failure Handled):\n"
            "FAILURE SCENARIO: Naive LLM or regex parsers extracted '$81.0 Billion' and '$0.4 Billion' from page 85 of the RBI Report as contradictory FDI metrics for FY25.\n"
            "HANDLING & MITIGATION: The Fact Engine's Multi-Stage Scope Verifier detected that $81.0B represents 'Gross Inflows', "
            "whereas $0.4B represents 'Net Inflow' after accounting for $51.5B in repatriation/disinvestments and $29.2B in outward FDI.\n"
            "The system flagged the raw extraction ambiguity, computed the accounting balance identity (Net = Gross - Repatriation - Outward), "
            "and prevented a false contradiction alert."
        ),
        context_diff={
            "case_number": 4,
            "title": "Gross FDI ($81.0B) vs Net FDI ($0.4B) Disambiguation",
            "raw_failure_flag": "Ambiguous Metric Scope ('FDI Inflow')",
            "scope_a": "Gross Direct Investment Inflows ($81.0B)",
            "scope_b": "Net Capital Flow after Repatriations & Outward FDI ($0.4B)",
            "mitigation_applied": "Accounting Identity Verification & Scope Tagging"
        },
        confidence_score=0.95
    ))
