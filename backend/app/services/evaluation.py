from pydantic import BaseModel, Field
from pydantic_ai import Agent

class EvaluationScorecard(BaseModel):
    """Structured response schema for deterministic agent outputs."""
    is_compliant: bool = Field(..., description="True if no severe policy violations are detected.")
    risk_score: float = Field(..., description="Calculated risk score from 0.00 (Safe) to 1.00 (Critical Failure).")
    justification: str = Field(..., description="Detailed analytical reasoning for the score.")

# Instantiate a Pydantic AI Evaluation Agent using standard models
evaluation_agent = Agent(
    'openai:gpt-4o',
    result_type=EvaluationScorecard,
    system_prompt=(
        "You are an expert financial compliance auditor. Analyze the transaction logs "
        "and contextual data against regulatory rules to produce a structured scorecard."
    )
)