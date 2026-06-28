import chromadb
from typing import List, Dict, Any

class ComplianceRAGEngine:
    """
    Vector database context injection engine.
    Stores and retrieves regulatory policy clauses (e.g., FINRA, SEC rule structures).
    """
    def __init__(self):
        self.chroma_client = chromadb.EphemeralClient()
        self.collection = self.chroma_client.get_or_create_collection(name="regulatory_rules")
        self._seed_static_policies()

    def _seed_static_policies(self) -> None:
        """Seeds standard regulatory policy thresholds into memory."""
        self.collection.add(
            documents=[
                "SEC Rule 10b-5: Strict prohibition of material non-public information (MNPI) disclosure or insider trading patterns.",
                "FINRA Anti-Money Laundering Framework: Transactions exceeding $10,000 sourced from unverified or high-risk locations require immediate escalation."
            ],
            ids=["sec_10b5", "finra_aml"],
            metadatas=[{"authority": "SEC"}, {"authority": "FINRA"}]
        )

    async def query_relevant_policies(self, user_prompt: str, max_results: int = 2) -> List[str]:
        """Asynchronously searches vector indices for matching regulatory rules."""
        # Wrap synchronous Chroma query inside an async thread abstraction if needed
        results = self.collection.query(
            query_texts=[user_prompt],
            n_results=max_results
        )
        return results["documents"][0] if results and "documents" in results else []