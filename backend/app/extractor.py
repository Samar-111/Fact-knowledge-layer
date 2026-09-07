import re
import json
import logging
from typing import List, Dict, Any, Optional
from app.database import FactModel, db
from app.config import settings

logger = logging.getLogger("extractor")

class FactExtractor:
    METRIC_PATTERNS = [
        {
            "metric": "Real GDP Growth",
            "regex": r"(?:real\s+(?:gross\s+domestic\s+product|GDP)|GDP)\s*(?:growth|is\s+estimated\s+to\s+grow|grew|expanded|projected\s+at)\s*(?:by|to|at)?\s*(-?\d+(?:\.\d+)?)\s*(per\s*cent|%)",
            "unit": "%",
            "subject": "Economy / National Accounts"
        },
        {
            "metric": "Headline CPI Inflation",
            "regex": r"(?:headline\s+inflation|Consumer\s+Price\s+Index\s+\(CPI\)\s+inflation|retail\s+(?:headline\s+)?inflation|CPI\s+inflation)\s*(?:eased|moderated|stood\s+at|averaged|declined\s+to|was)?\s*(-?\d+(?:\.\d+)?)\s*(per\s*cent|%)",
            "unit": "%",
            "subject": "Inflation & Prices"
        },
        {
            "metric": "Core Inflation",
            "regex": r"(?:core\s+inflation|CPI\s+excluding\s+food\s+and\s+fuel)\s*(?:eased\s+to|moderated\s+to|reached|stood\s+at|was|averaged)?\s*(-?\d+(?:\.\d+)?)\s*(per\s*cent|%)",
            "unit": "%",
            "subject": "Inflation & Prices"
        },
        {
            "metric": "Foreign Exchange Reserves",
            "regex": r"(?:foreign\s+exchange\s+reserves|forex\s+reserves|FX\s+reserves)\s*(?:stood\s+at|increased\s+to|moderated\s+to|reached|at)?\s*(?:USD|\$)?\s*(-?\d+(?:\.\d+)?)\s*billion",
            "unit": "USD Billion",
            "subject": "External Sector"
        },
        {
            "metric": "Gross FDI Inflows",
            "regex": r"gross\s+(?:foreign\s+direct\s+investment|FDI)\s+inflows?\s*(?:increased|rose|reached|stood\s+at|to|at)?\s*(?:USD|\$)?\s*(-?\d+(?:\.\d+)?)\s*billion",
            "unit": "USD Billion",
            "subject": "Foreign Investment"
        },
        {
            "metric": "Net FDI Inflows",
            "regex": r"net\s+(?:foreign\s+direct\s+investment|FDI)\s+(?:inflows?|inflow)\s*(?:declined\s+to|stood\s+at|was|at)?\s*(?:USD|\$)?\s*(-?\d+(?:\.\d+)?)\s*billion",
            "unit": "USD Billion",
            "subject": "Foreign Investment"
        },
        {
            "metric": "Current Account Deficit (CAD)",
            "regex": r"(?:current\s+account\s+deficit|CAD)\s*(?:remains\s+contained\s+at|moderated\s+slightly\s+to|stood\s+at|at|is\s+projected\s+at)\s*(-?\d+(?:\.\d+)?)\s*(per\s*cent|%)\s*of\s*GDP",
            "unit": "% of GDP",
            "subject": "External Sector"
        },
        {
            "metric": "Policy Repo Rate",
            "regex": r"(?:policy\s+repo\s+rate|repo\s+rate)\s*(?:reduced|by\s+25\s+bps\s+to|lowered\s+to|at|stood\s+at)\s*(-?\d+(?:\.\d+)?)\s*(per\s*cent|%)",
            "unit": "%",
            "subject": "Monetary Policy"
        },
        {
            "metric": "Services Export Growth",
            "regex": r"services\s+exports?\s*(?:grew|grew\s+at|increased\s+by)\s*(-?\d+(?:\.\d+)?)\s*(per\s*cent|%)",
            "unit": "%",
            "subject": "Trade & Services"
        }
    ]

    def extract_from_pages(self, doc_id: str, doc_name: str, pages_data: List[Dict[str, Any]]) -> List[FactModel]:
        extracted_facts = []
        
        if settings.GEMINI_API_KEY:
            try:
                extracted_facts = self._extract_with_gemini(doc_id, doc_name, pages_data)
            except Exception as e:
                logger.warning(f"Gemini LLM extraction failed: {e}. Falling back to Rule-based extraction.")
                extracted_facts = self._extract_with_rules(doc_id, doc_name, pages_data)
        else:
            extracted_facts = self._extract_with_rules(doc_id, doc_name, pages_data)

        for fact in extracted_facts:
            db.add_fact(fact)

        return extracted_facts

    def _extract_with_rules(self, doc_id: str, doc_name: str, pages_data: List[Dict[str, Any]]) -> List[FactModel]:
        facts = []
        for page in pages_data:
            text = page["cleaned_text"]
            page_num = page["page_number"]
            
            estimate_stage = "Standard Outturn / Official"
            if "first advance estimate" in text.lower() or "first advanced estimate" in text.lower() or "fae" in text.lower():
                estimate_stage = "First Advance Estimate (MoSPI Jan)"
            elif "second advance estimate" in text.lower() or "sae" in text.lower():
                estimate_stage = "Second Advance Estimate (MoSPI Feb)"
            elif "revised estimate" in text.lower() or "re" in text.lower():
                estimate_stage = "Revised Estimate (RE)"
            elif "projection" in text.lower() or "baseline" in text.lower():
                estimate_stage = "Forecast / Projection"

            time_period = "FY25 (2024-25)"
            if "2023-24" in text or "fy24" in text.lower():
                time_period = "FY24 (2023-24)"
            elif "2025-26" in text or "fy26" in text.lower() or "fy2025/26" in text.lower():
                time_period = "FY26 (2025-26)"
            elif "2024-25" in text or "fy25" in text.lower() or "fy2024/25" in text.lower():
                time_period = "FY25 (2024-25)"
            elif "2024" in text:
                time_period = "CY 2024"

            for pat in self.METRIC_PATTERNS:
                matches = re.finditer(pat["regex"], text, re.IGNORECASE)
                for match in matches:
                    try:
                        val = float(match.group(1))
                        start = max(0, match.start() - 60)
                        end = min(len(text), match.end() + 60)
                        quote = text[start:end].strip()
                        
                        fact = FactModel(
                            doc_id=doc_id,
                            doc_name=doc_name,
                            subject=pat["subject"],
                            metric_name=pat["metric"],
                            value=val,
                            value_text=f"{val} {pat['unit']}",
                            unit=pat["unit"],
                            time_period=time_period,
                            estimate_stage=estimate_stage,
                            geographic_scope="India",
                            page_number=page_num,
                            exact_quote=f"... {quote} ...",
                            confidence=0.92,
                            category="Economic Metric",
                            extraction_method="Rule-based NLP Engine"
                        )
                        facts.append(fact)
                    except Exception as ex:
                        logger.warning(f"Error parsing regex match: {ex}")
                        
        return facts

    def _extract_with_gemini(self, doc_id: str, doc_name: str, pages_data: List[Dict[str, Any]]) -> List[FactModel]:
        from google import genai
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        facts = []
        
        for page in pages_data:
            text = page["cleaned_text"]
            if len(text) < 50:
                continue
                
            prompt = f"""
            You are a financial and economic data extraction AI.
            Extract all key numerical facts from the following text (Source: {doc_name}, Page {page['page_number']}).
            Return a JSON array of objects with the following schema for each fact:
            [
              {{
                "subject": "Category e.g. National Income, Inflation, Trade",
                "metric_name": "Standard Metric Name e.g. Real GDP Growth",
                "value": 6.4,
                "unit": "% or USD Billion or Lakh MT",
                "time_period": "FY25 or 2024-25 or H1 FY25",
                "estimate_stage": "First Advance Estimate or Revised Estimate or Projection",
                "exact_quote": "Verbatim short sentence from text containing the metric"
              }}
            ]
            Text:
            {text[:3000]}
            """
            
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            
            resp_text = response.text.strip()
            if resp_text.startswith("```"):
                resp_text = re.sub(r"^```(?:json)?\n|\n```$", "", resp_text)
                
            data = json.loads(resp_text)
            for item in data:
                if isinstance(item, dict) and "metric_name" in item and "value" in item:
                    fact = FactModel(
                        doc_id=doc_id,
                        doc_name=doc_name,
                        subject=item.get("subject", "Economic Data"),
                        metric_name=item.get("metric_name", "Metric"),
                        value=float(item.get("value", 0.0)),
                        unit=item.get("unit", ""),
                        time_period=item.get("time_period", "FY25"),
                        estimate_stage=item.get("estimate_stage", "Official"),
                        page_number=page["page_number"],
                        exact_quote=item.get("exact_quote", text[:100]),
                        confidence=0.96,
                        extraction_method="Gemini 2.5 Flash LLM"
                    )
                    facts.append(fact)
                    
        return facts
