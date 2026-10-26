from pathlib import Path
import shutil
import config
from utils import pdfs_to_markdowns, clear_directory_contents

class DocumentManager:

    def __init__(self, rag_system):
        self.rag_system = rag_system
        self.markdown_dir = Path(config.MARKDOWN_DIR)
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        
    @staticmethod
    def _extract_file_info(p):
        path_str = None
        orig_name = None
        if isinstance(p, dict):
            path_str = p.get("path") or p.get("name")
            orig_name = p.get("orig_name")
        elif hasattr(p, "path"):
            path_str = str(p.path)
            orig_name = getattr(p, "orig_name", None)
        elif hasattr(p, "name") and not isinstance(p, (str, Path)):
            path_str = str(p.name)
            orig_name = getattr(p, "orig_name", None)
        elif p:
            path_str = str(p)
            
        if path_str and Path(path_str).suffix.lower() in [".pdf", ".md"]:
            return path_str, orig_name or Path(path_str).name
        return None, None

    def add_documents(self, document_paths, progress_callback=None):
        if not document_paths:
            return 0, 0
            
        raw_list = [document_paths] if isinstance(document_paths, (str, dict, Path)) or hasattr(document_paths, "path") else document_paths
        valid_docs = []
        for p in raw_list:
            fpath, fname = self._extract_file_info(p)
            if fpath:
                valid_docs.append((fpath, fname))
        
        if not valid_docs:
            return 0, 0
            
        added = 0
        skipped = 0
            
        for i, (doc_path, orig_name) in enumerate(valid_docs):
            if progress_callback:
                progress_callback((i + 1) / len(valid_docs), f"Processing {orig_name}")
                
            source_path = Path(doc_path)
            doc_name = Path(orig_name).stem if orig_name else source_path.stem
            md_path = self.markdown_dir / f"{doc_name}.md"
            
            if md_path.exists():
                skipped += 1
                continue
                
            parent_ids = []
            try:
                if source_path.suffix.lower() == ".md":
                    shutil.copy(source_path, md_path)
                else:
                    pdfs_to_markdowns(str(source_path), overwrite=False)
                parent_chunks, child_chunks = self.rag_system.chunker.create_chunks_single(
                    md_path,
                    source_name=orig_name or source_path.name,
                )
                
                if not child_chunks:
                    raise ValueError("No child chunks were created.")
                
                parent_ids = [parent_id for parent_id, _ in parent_chunks]
                self.rag_system.parent_store.save_many(parent_chunks)
                collection = self.rag_system.vector_db.get_collection(self.rag_system.collection_name)
                collection.add_documents(child_chunks)
                
                added += 1
                
            except Exception as e:
                self.rag_system.parent_store.delete_many(parent_ids)
                if md_path.exists():
                    md_path.unlink()
                print(f"Error processing {doc_path}: {e}")
                skipped += 1
            
        return added, skipped
    
    def get_markdown_files(self):
        sources = self.rag_system.parent_store.list_sources()
        if sources:
            return sources
        return sorted(p.name for p in self.markdown_dir.glob("*.md"))
    
    def clear_all(self):
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
        self.rag_system.vector_db.delete_collection(self.rag_system.collection_name)

        clear_directory_contents(self.markdown_dir)
        self.rag_system.parent_store.clear_store()

        self.rag_system.vector_db.create_collection(self.rag_system.collection_name)

    def get_chunk_analytics(self):
        doc_files = self.get_markdown_files()
        total_docs = len(doc_files)
        parent_count = self.rag_system.parent_store.get_count()
        child_count = self.rag_system.vector_db.get_points_count(self.rag_system.collection_name)
        avg_child = round(child_count / total_docs, 1) if total_docs > 0 else 0
        avg_parent = round(parent_count / total_docs, 1) if total_docs > 0 else 0
        source_counts = self.rag_system.parent_store.get_sources_with_counts()

        return {
            "total_docs": total_docs,
            "doc_list": doc_files,
            "parent_chunks": parent_count,
            "child_chunks": child_count,
            "avg_child_per_doc": avg_child,
            "avg_parent_per_doc": avg_parent,
            "source_counts": source_counts,
            "strategy": "Hierarchical Parent-Child Chunking",
            "parent_type": f"Markdown Header Splitter ({', '.join(h[0] for h in config.HEADERS_TO_SPLIT_ON)} | Min: {config.MIN_PARENT_SIZE}, Max: {config.MAX_PARENT_SIZE} chars)",
            "child_type": f"Recursive Character Splitter ({config.CHILD_CHUNK_SIZE} chars | {config.CHILD_CHUNK_OVERLAP} overlap)",
            "dense_model": config.DENSE_MODEL,
            "sparse_model": config.SPARSE_MODEL,
        }

