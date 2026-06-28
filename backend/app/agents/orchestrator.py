import autogen
from typing import Dict, Any
from backend.app.services.rag_engine import ComplianceRAGEngine
from backend.app.services.memory_manager import CognitiveMemoryManager
from backend.app.services.evaluation import evaluation_agent, EvaluationScorecard
from backend.app.core.config import settings

class GuardShieldMultiAgentOrchestrator:
    """
    Orchestrates collaborative workflows between specialized agents using AutoGen.
    Evaluates final decisions using strict, type-safe Pydantic AI guardrails.
    """
    def __init__(self):
        self.llm_config = {
            "config_list": [{"model": "gpt-4o", "api_key": settings.OPENAI_API_KEY}],
            "temperature": 0.0,
            "cache_seed": None  # Disable historical caching to ensure clean real-time processing
        }
        self.rag_engine = ComplianceRAGEngine()
        self.memory_manager = CognitiveMemoryManager()

    async def process_compliance_audit(self, transaction_ref: str, raw_payload: str) -> EvaluationScorecard:
        # 1. Fetch relevant corporate context and historical behavior data
        historical_context = self.memory_manager.query_long_term_history(entity_id="SYSTEM_ORG", query=raw_payload)
        matched_rules = await self.rag_engine.query_relevant_policies(raw_payload)
        
        combined_context = f"Matched Regulations:\n{chr(10).join(matched_rules)}\n\nPast Historical Violations:\n{historical_context}"

        # 2. Configure AutoGen Agents for multi-turn collaboration
        compliance_analyst = autogen.AssistantAgent(
            name="ComplianceAnalyst",
            llm_config=self.llm_config,
            system_message="You parse transactions to detect regulatory policy violations. Flag specific clauses clearly."
        )

        risk_strategist = autogen.AssistantAgent(
            name="RiskStrategist",
            llm_config=self.llm_config,
            system_message="You evaluate exposure limits, structural impact patterns, and recommend containment steps."
        )

        # 3. Initialize a temporary workspace group chat
        groupchat = autogen.GroupChat(
            agents=[compliance_analyst, risk_strategist], 
            messages=[], 
            max_round=4
        )
        manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=self.llm_config)

        # Trigger group chat execution
        compliance_analyst.initiate_chat(
            manager,
            message=f"Analyze this payload: {raw_payload}\n\nContext Grid:\n{combined_context}"
        )

        # Extract findings from the chat logs
        chat_history_summary = "\n".join([f"{m['name']}: {m['content']}" for m in groupchat.messages])

        # 4. Use the structured Pydantic AI agent to parse findings into a type-safe scorecard
        result = await evaluation_agent.run(
            f"Raw Payload: {raw_payload}\n\nAgent Discussion Summary:\n{chat_history_summary}"
        )
        
        # 5. Persist critical findings to long-term memory if high risk is detected
        if result.data.risk_score > 0.70:
            self.memory_manager.add_long_term_violation_pattern(
                entity_id="SYSTEM_ORG",
                pattern_summary=f"Ref: {transaction_ref} - Score: {result.data.risk_score}. Justification: {result.data.justification}"
            )

        return result.data