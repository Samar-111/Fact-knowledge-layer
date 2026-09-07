import logging
from typing import List, Dict, Any
from app.database import FactModel, RelationshipModel, db

logger = logging.getLogger("reconciler")

class FactReconciler:
    METRIC_ALIASES = {
        "real gdp growth": ["real gdp growth", "gdp growth", "real gross domestic product growth"],
        "headline cpi inflation": ["headline cpi inflation", "headline inflation", "cpi inflation", "retail inflation"],
        "core inflation": ["core inflation", "cpi excluding food and fuel", "non-food non-fuel inflation"],
        "foreign exchange reserves": ["foreign exchange reserves", "forex reserves", "fx reserves"],
        "gross fdi inflows": ["gross fdi inflows", "gross foreign direct investment inflows", "gross fdi"],
        "net fdi inflows": ["net fdi inflows", "net foreign direct investment", "net fdi"],
        "current account deficit (cad)": ["current account deficit", "cad", "current account deficit (cad)", "current account balance"]
    }

    def process_all_relationships(self, facts: List[Dict[str, Any]]) -> List[RelationshipModel]:
        relationships = []
        n = len(facts)
        
        for i in range(n):
            for j in range(i + 1, n):
                fact_a = facts[i]
                fact_b = facts[j]
                
                if fact_a["doc_id"] == fact_b["doc_id"] and fact_a["page_number"] == fact_b["page_number"]:
                    continue
                    
                rel = self.compare_fact_pair(fact_a, fact_b)
                if rel:
                    relationships.append(rel)
                    db.add_relationship(rel)
                    
        return relationships

    def compare_fact_pair(self, fact_a: Dict[str, Any], fact_b: Dict[str, Any]) -> RelationshipModel | None:
        metric_a = fact_a["metric_name"].lower().strip()
        metric_b = fact_b["metric_name"].lower().strip()
        
        is_same_metric = self._are_metrics_equivalent(metric_a, metric_b)
        if not is_same_metric:
            return None
            
        val_a = float(fact_a["value"])
        val_b = float(fact_b["value"])
        unit_a = fact_a.get("unit", "").lower()
        unit_b = fact_b.get("unit", "").lower()
        period_a = fact_a.get("time_period", "")
        period_b = fact_b.get("time_period", "")
        stage_a = fact_a.get("estimate_stage", "")
        stage_b = fact_b.get("estimate_stage", "")
        
        val_diff = abs(val_a - val_b)
        
        if val_diff < 0.15 and period_a == period_b and unit_a == unit_b:
            return RelationshipModel(
                fact_a_id=fact_a["id"],
                fact_b_id=fact_b["id"],
                relationship_type="CORROBORATED",
                reasoning=(
                    f"Both '{fact_a['doc_name']}' (p. {fact_a['page_number']}) and '{fact_b['doc_name']}' (p. {fact_b['page_number']}) "
                    f"corroborate that {fact_a['metric_name']} for {period_a} is {val_a}{fact_a['unit']}."
                ),
                context_diff={
                    "period_match": True,
                    "unit_match": True,
                    "val_difference": round(val_diff, 4)
                },
                confidence_score=0.98
            )
            
        if stage_a != stage_b or "h1" in period_a.lower() or "h1" in period_b.lower():
            reasoning = (
                f"Apparent contradiction between {val_a}{fact_a['unit']} ({fact_a['doc_name']}) and {val_b}{fact_b['unit']} ({fact_b['doc_name']}) "
                f"is RECONCILED by contextual metadata. '{fact_a['doc_name']}' uses {stage_a} ({period_a}), "
                f"whereas '{fact_b['doc_name']}' reflects {stage_b} ({period_b})."
            )
            return RelationshipModel(
                fact_a_id=fact_a["id"],
                fact_b_id=fact_b["id"],
                relationship_type="RECONCILED",
                reasoning=reasoning,
                context_diff={
                    "stage_a": stage_a,
                    "stage_b": stage_b,
                    "period_a": period_a,
                    "period_b": period_b,
                    "reconciliation_type": "Estimate Stage & Timeline Revision"
                },
                confidence_score=0.95
            )
            
        if val_diff >= 0.15 and period_a == period_b and stage_a == stage_b:
            return RelationshipModel(
                fact_a_id=fact_a["id"],
                fact_b_id=fact_b["id"],
                relationship_type="CONTRADICTED",
                reasoning=(
                    f"Direct contradiction detected: '{fact_a['doc_name']}' states {val_a}{fact_a['unit']} "
                    f"whereas '{fact_b['doc_name']}' states {val_b}{fact_b['unit']} for {fact_a['metric_name']} in {period_a} under identical estimate conditions."
                ),
                context_diff={
                    "val_a": val_a,
                    "val_b": val_b,
                    "diff": round(val_diff, 2)
                },
                confidence_score=0.91
            )
            
        return None

    def _are_metrics_equivalent(self, m1: str, m2: str) -> bool:
        if m1 == m2:
            return True
        for key, aliases in self.METRIC_ALIASES.items():
            if m1 in aliases and m2 in aliases:
                return True
        return False
