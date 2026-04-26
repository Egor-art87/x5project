"""
Схема ответа GigaChat для скоринга.

Pydantic используется как валидатор: GigaChat прислал JSON, мы парсим
его в эту схему — если поля кривые, упадёт с понятной ошибкой.
"""

from pydantic import BaseModel, Field


class ScoringResult(BaseModel):
    score: int = Field(ge=0, le=100, description="Соответствие 0–100")
    summary: str = Field(min_length=1, max_length=2000)
    strengths: list[str] = Field(default_factory=list, max_length=10)
    gaps: list[str] = Field(default_factory=list, max_length=10)
    red_flags: list[str] = Field(default_factory=list, max_length=10)
