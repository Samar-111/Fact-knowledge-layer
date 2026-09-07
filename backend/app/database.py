import sqlite3
import json
import os
import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.config import settings

class FactModel(BaseModel):
    id: str = Field(default_factory=lambda: f"fact_{uuid.uuid4().hex[:8]}")
    doc_id: str
    doc_name: str
    subject: str
    metric_name: str
    value: float
    value_text: Optional[str] = None
    unit: str
    time_period: str
    estimate_stage: Optional[str] = "Standard Outturn / Official"
    geographic_scope: Optional[str] = "India"
    page_number: int
    exact_quote: str
    confidence: float = 0.95
    category: Optional[str] = "Macroeconomic Indicator"
    extraction_method: str = "Hybrid Rules + NLP"

class RelationshipModel(BaseModel):
    id: str = Field(default_factory=lambda: f"rel_{uuid.uuid4().hex[:8]}")
    fact_a_id: str
    fact_b_id: str
    relationship_type: str
    reasoning: str
    context_diff: Optional[Dict[str, Any]] = None
    confidence_score: float = 0.90

class Database:
    def __init__(self, db_path: str = settings.DB_PATH):
        self.db_path = db_path
        self._init_db()

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id TEXT PRIMARY KEY,
                title TEXT,
                filename TEXT,
                file_path TEXT,
                page_count INTEGER,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id TEXT PRIMARY KEY,
                doc_id TEXT,
                doc_name TEXT,
                subject TEXT,
                metric_name TEXT,
                value REAL,
                value_text TEXT,
                unit TEXT,
                time_period TEXT,
                estimate_stage TEXT,
                geographic_scope TEXT,
                page_number INTEGER,
                exact_quote TEXT,
                confidence REAL,
                category TEXT,
                extraction_method TEXT,
                FOREIGN KEY (doc_id) REFERENCES documents (id)
            )
            """)
            
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                fact_a_id TEXT,
                fact_b_id TEXT,
                relationship_type TEXT,
                reasoning TEXT,
                context_diff TEXT,
                confidence_score REAL,
                FOREIGN KEY (fact_a_id) REFERENCES facts (id),
                FOREIGN KEY (fact_b_id) REFERENCES facts (id)
            )
            """)
            conn.commit()

    def add_document(self, doc_id: str, title: str, filename: str, file_path: str, page_count: int):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO documents (id, title, filename, file_path, page_count)
                VALUES (?, ?, ?, ?, ?)
            """, (doc_id, title, filename, file_path, page_count))
            conn.commit()

    def delete_document(self, doc_id: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT file_path FROM documents WHERE id = ?", (doc_id,))
            row = cursor.fetchone()
            if row and row["file_path"] and os.path.exists(row["file_path"]):
                try:
                    os.remove(row["file_path"])
                except Exception:
                    pass
            cursor.execute("DELETE FROM relationships WHERE fact_a_id IN (SELECT id FROM facts WHERE doc_id = ?) OR fact_b_id IN (SELECT id FROM facts WHERE doc_id = ?)", (doc_id, doc_id))
            cursor.execute("DELETE FROM facts WHERE doc_id = ?", (doc_id,))
            cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
            conn.commit()
            return True

    def add_fact(self, fact: FactModel):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO facts (
                    id, doc_id, doc_name, subject, metric_name, value, value_text,
                    unit, time_period, estimate_stage, geographic_scope, page_number,
                    exact_quote, confidence, category, extraction_method
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                fact.id, fact.doc_id, fact.doc_name, fact.subject, fact.metric_name,
                fact.value, fact.value_text or str(fact.value), fact.unit, fact.time_period,
                fact.estimate_stage, fact.geographic_scope, fact.page_number,
                fact.exact_quote, fact.confidence, fact.category, fact.extraction_method
            ))
            conn.commit()

    def add_relationship(self, rel: RelationshipModel):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            context_json = json.dumps(rel.context_diff) if rel.context_diff else "{}"
            cursor.execute("""
                INSERT OR REPLACE INTO relationships (
                    id, fact_a_id, fact_b_id, relationship_type, reasoning, context_diff, confidence_score
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                rel.id, rel.fact_a_id, rel.fact_b_id, rel.relationship_type,
                rel.reasoning, context_json, rel.confidence_score
            ))
            conn.commit()

    def get_all_documents(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM documents ORDER BY uploaded_at DESC")
            return [dict(row) for row in cursor.fetchall()]

    def get_all_facts(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM facts")
            return [dict(row) for row in cursor.fetchall()]

    def get_fact_by_id(self, fact_id: str) -> Optional[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM facts WHERE id = ?", (fact_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_all_relationships(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, 
                       fa.metric_name as fact_a_metric, fa.doc_name as fact_a_doc, fa.value as fact_a_val, fa.unit as fact_a_unit,
                       fb.metric_name as fact_b_metric, fb.doc_name as fact_b_doc, fb.value as fact_b_val, fb.unit as fact_b_unit
                FROM relationships r
                JOIN facts fa ON r.fact_a_id = fa.id
                JOIN facts fb ON r.fact_b_id = fb.id
            """)
            results = []
            for row in cursor.fetchall():
                item = dict(row)
                if item["context_diff"]:
                    try:
                        item["context_diff"] = json.loads(item["context_diff"])
                    except:
                        pass
                results.append(item)
            return results

db = Database()
