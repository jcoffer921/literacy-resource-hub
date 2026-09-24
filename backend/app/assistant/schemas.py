"""Data contracts for the assistant module: retrieved chunks and the response shape."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel

# TODO: the ingestion/chunker pipeline must preserve page numbers and section
# headings on each chunk, or page_start/page_end/section will stay None here.


class SourceChunk(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    publisher: str | None = None
    url: str | None = None
    page_start: int | None = None
    page_end: int | None = None
    section: str | None = None
    text: str
    score: float

    @property
    def location(self) -> str:
        if self.page_start is not None:
            if self.page_end is None or self.page_end == self.page_start:
                return f"p. {self.page_start}"
            return f"pp. {self.page_start}–{self.page_end}"
        return self.section or ""


class CitedSource(BaseModel):
    label: str
    chunk_id: str
    title: str
    publisher: str | None = None
    location: str
    excerpt: str
    url: str | None = None


class AssistantResponse(BaseModel):
    answer: str
    coverage: Literal["strong", "weak", "none"]
    sources: list[CitedSource]
