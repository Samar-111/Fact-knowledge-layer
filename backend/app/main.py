import os
import shutil
import uuid
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import db, FactModel, RelationshipModel
from app.pdf_processor import PDFProcessor
from app.extractor import FactExtractor
from app.reconciler import FactReconciler
from app.sample_data import seed_benchmark_dataset

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Fact Knowledge Layer API for extracting, grounding, comparing, and reconciling economic/semantic facts across PDFs."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    seed_benchmark_dataset()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

@app.get("/api/documents")
def get_documents():
    return db.get_all_documents()

@app.delete("/api/documents/{doc_id}")
def delete_document(doc_id: str):
    success = db.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"message": "Document and associated facts successfully deleted.", "doc_id": doc_id}

@app.get("/api/facts")
def get_facts(
    subject: Optional[str] = None,
    metric_name: Optional[str] = None,
    doc_name: Optional[str] = None
):
    facts = db.get_all_facts()
    if subject:
        facts = [f for f in facts if subject.lower() in f.get("subject", "").lower()]
    if metric_name:
        facts = [f for f in facts if metric_name.lower() in f.get("metric_name", "").lower()]
    if doc_name:
        facts = [f for f in facts if doc_name.lower() in f.get("doc_name", "").lower()]
    return facts

@app.get("/api/relationships")
def get_relationships(rel_type: Optional[str] = None):
    rels = db.get_all_relationships()
    if rel_type:
        rels = [r for r in rels if r["relationship_type"].upper() == rel_type.upper()]
    return rels

@app.get("/api/showcase")
def get_showcase_cases():
    seed_benchmark_dataset()
    rels = db.get_all_relationships()
    showcase = []
    
    for r in rels:
        c_diff = r.get("context_diff", {})
        if isinstance(c_diff, dict) and "case_number" in c_diff:
            fact_a = db.get_fact_by_id(r["fact_a_id"])
            fact_b = db.get_fact_by_id(r["fact_b_id"])
            showcase.append({
                "case_number": c_diff["case_number"],
                "title": c_diff.get("title", f"Case {c_diff['case_number']}"),
                "relationship_type": r["relationship_type"],
                "reasoning": r["reasoning"],
                "confidence_score": r["confidence_score"],
                "fact_a": fact_a,
                "fact_b": fact_b,
                "context_diff": c_diff
            })
            
    showcase.sort(key=lambda x: x["case_number"])
    return showcase

@app.get("/api/graph")
def get_knowledge_graph():
    facts = db.get_all_facts()
    relationships = db.get_all_relationships()
    
    nodes = []
    for f in facts:
        nodes.append({
            "id": f["id"],
            "label": f"{f['metric_name']}: {f['value']}{f['unit']}",
            "doc_name": f["doc_name"],
            "page": f["page_number"],
            "subject": f["subject"],
            "period": f["time_period"],
            "estimate_stage": f["estimate_stage"]
        })
        
    edges = []
    for r in relationships:
        edges.append({
            "id": r["id"],
            "source": r["fact_a_id"],
            "target": r["fact_b_id"],
            "label": r["relationship_type"],
            "reasoning": r["reasoning"]
        })
        
    return {"nodes": nodes, "edges": edges}

@app.post("/api/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    save_path = os.path.join(settings.UPLOADS_DIR, f"{doc_id}_{file.filename}")
    
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    processor = PDFProcessor()
    pages_data = processor.extract_document_pages(save_path)
    
    db.add_document(
        doc_id=doc_id,
        title=file.filename.replace(".pdf", "").replace("_", " "),
        filename=file.filename,
        file_path=save_path,
        page_count=len(pages_data)
    )
    
    extractor = FactExtractor()
    new_facts = extractor.extract_from_pages(doc_id, file.filename, pages_data)
    
    all_facts = db.get_all_facts()
    reconciler = FactReconciler()
    new_rels = reconciler.process_all_relationships(all_facts)
    
    return {
        "message": f"Successfully processed {file.filename}",
        "doc_id": doc_id,
        "page_count": len(pages_data),
        "extracted_facts_count": len(new_facts),
        "new_relationships_found": len(new_rels)
    }
