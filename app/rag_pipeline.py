"""
RAG Pipeline for Chatbot - semantic retrieval over SQLite using simple keyword search.
Note: Groq does not provide embeddings, so semantic vector search is disabled.
Retrieval falls back to keyword matching and text similarity.
"""

import json
import logging
import math
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

DEFAULT_CHAT_MODEL = "llama3-8b-8192"
MAX_CONTEXT_CHARS = 12000

# Prefer the real project location first, then legacy fallback.
KB_CANDIDATE_PATHS = [
    Path(__file__).parent.parent / "data" / "Knowledge base",
    Path(__file__).parent.parent / "Knowledge base",
]
GUARDRAILS_PATH = Path(__file__).parent.parent / "CHATBOT_GUARDRAILS.txt"


class RAGPipeline:
    """Retrieval-Augmented Generation pipeline using SQLite for keyword search.
    
    Note: Embeddings are disabled since Groq does not provide embedding models.
    For hackathon purposes, retrieval falls back to keyword matching.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.chat_model = DEFAULT_CHAT_MODEL
        self._disable_embeddings = True  # Always disabled - Groq has no embeddings
        self.kb_path = self._resolve_kb_path()
        self.guardrails = self._load_guardrails()

        self._init_vector_db()
        self._load_knowledge_base()

    def _resolve_kb_path(self) -> Path:
        for candidate in KB_CANDIDATE_PATHS:
            if candidate.exists():
                return candidate
        return KB_CANDIDATE_PATHS[0]

    def _load_guardrails(self) -> str:
        try:
            if GUARDRAILS_PATH.exists():
                return GUARDRAILS_PATH.read_text(encoding="utf-8")
            return ""
        except Exception as exc:
            logger.error("Failed loading guardrails: %s", exc)
            return ""

    def _init_vector_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vector (
                id INTEGER PRIMARY KEY,
                source_file TEXT NOT NULL,
                content_id TEXT NOT NULL,
                content_type TEXT NOT NULL,
                title TEXT,
                content TEXT NOT NULL,
                embedding TEXT,
                embedding_summary TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Safe migration for older schema versions.
        table_cols = {row[1] for row in cursor.execute("PRAGMA table_info(vector)").fetchall()}
        if "embedding" not in table_cols:
            cursor.execute("ALTER TABLE vector ADD COLUMN embedding TEXT")
        if "embedding_summary" not in table_cols:
            cursor.execute("ALTER TABLE vector ADD COLUMN embedding_summary TEXT")

        cursor.execute("CREATE INDEX IF NOT EXISTS idx_vector_source_file ON vector(source_file)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_vector_content_type ON vector(content_type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_vector_content_id ON vector(content_id)")

        conn.commit()
        conn.close()

    def _load_knowledge_base(self) -> None:
        try:
            if not self.kb_path.exists():
                logger.warning("Knowledge base path not found: %s", self.kb_path)
                return

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM vector")
            total_rows = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM vector WHERE embedding IS NOT NULL AND embedding != ''")
            embedded_rows = cursor.fetchone()[0]

            # Rebuild once if we have old rows without embeddings.
            if total_rows > 0 and embedded_rows == total_rows:
                conn.close()
                return
            if total_rows > 0 and embedded_rows < total_rows:
                cursor.execute("DELETE FROM vector")
                conn.commit()

            kb_files = [
                ("course_structure.json", "courses"),
                ("assessments.json", "assessments"),
                ("certifications.json", "certifications"),
                ("progress_tracking.json", "progress_tracking"),
                ("learning_paths.json", "learning_paths"),
                ("ai_enriched.json", "ai_enriched"),
            ]

            total_chunks = 0
            for filename, content_type in kb_files:
                kb_file = self.kb_path / filename
                if not kb_file.exists():
                    continue

                try:
                    with kb_file.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                except Exception as exc:
                    logger.error("Failed to parse %s: %s", kb_file, exc)
                    continue

                chunks = self._extract_chunks(filename, content_type, data)
                for chunk in chunks:
                    self._store_chunk(cursor, chunk)
                total_chunks += len(chunks)

            conn.commit()
            conn.close()
            logger.info("RAG KB indexed with %s chunks", total_chunks)

        except Exception as exc:
            logger.error("Error loading knowledge base: %s", exc)

    def _extract_chunks(self, filename: str, content_type: str, data: Dict[str, Any]) -> List[Dict[str, str]]:
        chunks: List[Dict[str, str]] = []

        # Build one logical document per entity, then split into retrievable chunks.
        entities: List[Tuple[str, str, str]] = []

        if content_type == "courses":
            for item in data.get("courses", []):
                entities.append((item.get("id", ""), "course", self._entity_to_text("course", item)))

        elif content_type == "assessments":
            for item in data.get("assessments", []):
                entities.append((item.get("assessment_id", ""), "assessment", self._entity_to_text("assessment", item)))

        elif content_type == "certifications":
            for item in data.get("certifications", []):
                entities.append((item.get("certification_id", ""), "certification", self._entity_to_text("certification", item)))

        elif content_type == "learning_paths":
            for item in data.get("learning_paths", []):
                entities.append((item.get("path_id", ""), "learning_path", self._entity_to_text("learning_path", item)))

        elif content_type == "progress_tracking":
            entity = data.get("progress_tracking", data)
            entities.append(("progress_tracking", "system_feature", self._entity_to_text("system_feature", entity, title="Progress Tracking")))

        elif content_type == "ai_enriched":
            for item in data.get("ai_generated_courses", []):
                entities.append((item.get("id", ""), "course", self._entity_to_text("course", item)))
            for item in data.get("ai_generated_assessments", []):
                entities.append((item.get("assessment_id", ""), "assessment", self._entity_to_text("assessment", item)))
            for item in data.get("ai_generated_certifications", []):
                entities.append((item.get("certification_id", ""), "certification", self._entity_to_text("certification", item)))
            for item in data.get("ai_generated_learning_paths", []):
                entities.append((item.get("path_id", ""), "learning_path", self._entity_to_text("learning_path", item)))

        for raw_id, entity_type, doc_text in entities:
            safe_id = raw_id or f"{entity_type}_{abs(hash(doc_text))}"
            for idx, piece in enumerate(self._chunk_text(doc_text, max_chars=900, overlap=120)):
                lines = [ln.strip() for ln in piece.splitlines() if ln.strip()]
                title = lines[0][:180] if lines else f"{entity_type} {safe_id}"
                chunks.append(
                    {
                        "source_file": filename,
                        "content_id": f"{safe_id}::chunk_{idx}",
                        "content_type": entity_type,
                        "title": title,
                        "content": piece,
                    }
                )

        return chunks

    def _entity_to_text(self, entity_type: str, item: Dict[str, Any], title: Optional[str] = None) -> str:
        resolved_title = title or item.get("title") or item.get("name") or f"{entity_type.title()} Item"
        flattened = self._flatten_json(item)

        return (
            f"Type: {entity_type}\n"
            f"Title: {resolved_title}\n"
            f"Details:\n{flattened}"
        )

    def _flatten_json(self, value: Any, prefix: str = "") -> str:
        lines: List[str] = []

        if isinstance(value, dict):
            for key, val in value.items():
                key_name = f"{prefix}.{key}" if prefix else str(key)
                lines.append(self._flatten_json(val, key_name))
        elif isinstance(value, list):
            for idx, val in enumerate(value):
                key_name = f"{prefix}[{idx}]"
                lines.append(self._flatten_json(val, key_name))
        else:
            if value is None:
                return ""
            text = str(value).strip()
            if not text:
                return ""
            lines.append(f"{prefix}: {text}")

        return "\n".join([ln for ln in lines if ln])

    def _chunk_text(self, text: str, max_chars: int = 900, overlap: int = 120) -> List[str]:
        text = " ".join(str(text).split())
        if not text:
            return []
        if len(text) <= max_chars:
            return [text]

        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(start + max_chars, len(text))
            if end < len(text):
                split_at = text.rfind(" ", start, end)
                if split_at > start + max_chars // 2:
                    end = split_at
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end >= len(text):
                break
            start = max(0, end - overlap)
        return chunks

    def _embed_text(self, text: str) -> List[float]:
        # Embeddings disabled - Groq does not provide embedding models
        # For hackathon, retrieval falls back to keyword matching
        return []

    def _store_chunk(self, cursor, chunk: Dict[str, str]) -> None:
        embedding = self._embed_text(chunk["content"])
        embedding_json = json.dumps(embedding) if embedding else ""

        cursor.execute(
            """
            INSERT INTO vector (source_file, content_id, content_type, title, content, embedding, embedding_summary)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                chunk["source_file"],
                chunk["content_id"],
                chunk["content_type"],
                chunk["title"],
                chunk["content"],
                embedding_json,
                chunk["title"],
            ),
        )

    def _cosine_similarity(self, a: List[float], b: List[float]) -> float:
        if not a or not b or len(a) != len(b):
            return -1.0

        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(y * y for y in b))
        if norm_a == 0 or norm_b == 0:
            return -1.0
        return dot / (norm_a * norm_b)

    def retrieve_relevant_chunks(self, user_query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        top_k = max(1, min(int(top_k), 5))
        query_embedding = self._embed_text(user_query)
        if not query_embedding:
            return []

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT source_file, content_id, content_type, title, content, embedding
            FROM vector
            WHERE embedding IS NOT NULL AND embedding != ''
            """
        )
        rows = cursor.fetchall()
        conn.close()

        scored: List[Dict[str, Any]] = []
        for source_file, content_id, content_type, title, content, embedding_text in rows:
            try:
                doc_embedding = json.loads(embedding_text)
            except Exception:
                continue
            score = self._cosine_similarity(query_embedding, doc_embedding)
            if score < 0.2:
                continue
            scored.append(
                {
                    "source_file": source_file,
                    "content_id": content_id,
                    "content_type": content_type,
                    "title": title,
                    "content": content,
                    "score": score,
                }
            )

        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

    def retrieve_relevant_context(self, user_query: str, top_k: int = 4) -> str:
        chunks = self.retrieve_relevant_chunks(user_query=user_query, top_k=top_k)
        if not chunks:
            return ""

        context_parts: List[str] = []
        total_chars = 0
        for idx, item in enumerate(chunks, start=1):
            block = (
                f"[Chunk {idx}]\n"
                f"Source: {item['source_file']}\n"
                f"Type: {item['content_type']}\n"
                f"Title: {item['title']}\n"
                f"Relevance: {item['score']:.3f}\n"
                f"Content: {item['content']}\n"
            )
            if total_chars + len(block) > MAX_CONTEXT_CHARS:
                break
            context_parts.append(block)
            total_chars += len(block)

        return "\n".join(context_parts)

    def preprocess_query_for_rag(self, user_query: str) -> Tuple[str, str]:
        """Compatibility wrapper used by routes and examples."""
        return user_query, self.retrieve_relevant_context(user_query=user_query, top_k=4)

    def get_guardrails_for_llm(self) -> str:
        return self.guardrails or ""

    # Legacy compatibility shim. We intentionally return empty content to avoid full KB prompt injection.
    def get_full_knowledge_base_for_llm(self) -> str:
        return ""


def get_rag_pipeline(database_path: str) -> RAGPipeline:
    """Get or create RAG pipeline singleton instance."""
    global _rag_instance
    if "_rag_instance" not in globals() or getattr(_rag_instance, "db_path", None) != database_path:
        _rag_instance = RAGPipeline(database_path)
    return _rag_instance
