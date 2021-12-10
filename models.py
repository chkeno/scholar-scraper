"""Module containing data models"""

from dataclasses import dataclass
from marshmallow import Schema, fields
from typing import List


@dataclass
class Publication:
    """
    Publication object definition
    """
    title: str
    journal_info: str
    publication_link: str
    citation_link: str
    authors_text: str = None
    citations_count: int = None
    citations: List = None


class PublicationSchema(Schema):
    """
    Publication class schema used for deserialization and serialization of objects
    """
    title = fields.Str(required=True)
    journal_info = fields.Str(required=True)
    publication_link = fields.Str(required=True)
    citation_link = fields.Str(required=True)
    authors_text = fields.Str(required=True)
    citations_count = fields.Int(required=False)
    citations = fields.Nested('PublicationSchema', many=True, required=False)
