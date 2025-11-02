import os
import json
from pathlib import Path
from typing import List, Dict, Any
from config import Config
import chromadb
from sentence_transformers import SentenceTransformer
import pandas as pd

class KnowledgeRetrieval:
    """RAG-based knowledge retrieval for legal sections"""
    
    def __init__(self, force_reindex: bool = False):
        self.laws_path = Config.LAWS_DATA_PATH
        self.vector_db_path = Config.VECTOR_DB_PATH
        self.embedding_model_name = Config.EMBEDDING_MODEL
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(self.embedding_model_name)
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(path=str(self.vector_db_path))
        self.collection = self._get_or_create_collection()
        
        # Load laws if not already indexed
        self._load_and_index_laws(force_reindex)
    
    def _get_or_create_collection(self):
        """Get or create ChromaDB collection"""
        try:
            return self.client.get_collection("law_sections")
        except:
            return self.client.create_collection("law_sections")
    
    def _load_and_index_laws(self, force: bool = False):
        """Load law sections from CSV/JSON and index them"""
        # Check if already indexed
        if not force and self.collection.count() > 0:
            return
        
        if force:
            try:
                existing_ids = self.collection.get()['ids']
                if existing_ids:
                    self.collection.delete(ids=existing_ids)
            except Exception as exc:
                print(f"Failed clearing existing index: {exc}")
        
        # Load from CSV files
        law_files = list(self.laws_path.glob("*.csv"))
        all_sections = []
        
        for file_path in law_files:
            try:
                df = pd.read_csv(file_path)
                for idx, row in df.iterrows():
                    # Skip empty rows
                    if pd.isna(row.get('text', '')) or str(row.get('text', '')).strip() == '':
                        continue
                    
                    section_text = f"{row.get('title', '')} {row.get('text', '')}"
                    section_code = row.get('section_code', '')
                    jurisdiction = row.get('jurisdiction', 'IN')
                    act_name = row.get('act_name', file_path.stem)
                    title = row.get('title', '')
                    
                    # Create unique ID: act_name + section_code + row_index to handle duplicates
                    unique_id = f"{act_name}_{section_code}_{idx}"
                    
                    all_sections.append({
                        'id': unique_id,
                        'text': section_text,
                        'metadata': {
                            'section_code': section_code,
                            'jurisdiction': jurisdiction,
                            'act_name': act_name,
                            'title': title
                        }
                    })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        # Index in ChromaDB
        if all_sections:
            self.collection.add(
                ids=[s['id'] for s in all_sections],
                documents=[s['text'] for s in all_sections],
                metadatas=[s['metadata'] for s in all_sections]
            )
            print(f"Indexed {len(all_sections)} law sections")
    
    def search(self, query: str, jurisdiction: str = 'IN', limit: int = 5) -> List[Dict]:
        """Search for relevant law sections"""
        # Query ChromaDB
        results = self.collection.query(
            query_texts=[query],
            n_results=limit,
            where={"jurisdiction": jurisdiction} if jurisdiction else None
        )
        
        # Format results
        sections = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                sections.append({
                    'text': doc,
                    'section_code': results['metadatas'][0][i].get('section_code', ''),
                    'jurisdiction': results['metadatas'][0][i].get('jurisdiction', 'IN'),
                    'act_name': results['metadatas'][0][i].get('act_name', ''),
                    'title': results['metadatas'][0][i].get('title', ''),
                    'distance': results['distances'][0][i] if results.get('distances') else None
                })
        
        return sections
    
    def add_section(self, title: str, section_code: str, text: str, jurisdiction: str = 'IN', act_name: str = ''):
        """Add a new law section to the index"""
        doc_id = f"{act_name}_{section_code}"
        self.collection.add(
            ids=[doc_id],
            documents=[f"{title} {text}"],
            metadatas=[{
                'section_code': section_code,
                'jurisdiction': jurisdiction,
                'act_name': act_name,
                'title': title
            }]
        )

    def reindex(self, force: bool = True):
        """Rebuild the vector index from CSV sources"""
        self._load_and_index_laws(force=force)


