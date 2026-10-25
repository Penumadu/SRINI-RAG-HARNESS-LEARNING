from typing import List
from pydantic import BaseModel, Field

class QueryAnalysis(BaseModel):
    is_clear: bool = Field(
        description="True if the user's question has sufficient detail to retrieve documents. If it asks about specific topics, files, or notes (e.g. '137notes', '217a'), it is clear (True). Only False if it contains dangling pronouns like 'what is it' with zero context."
    )
    questions: List[str] = Field(
        description="List of 1 to 3 rewritten, self-contained questions for document search."
    )
    clarification_needed: str = Field(
        default="",
        description="Explanation if the question is genuinely ambiguous, otherwise empty string."
    )