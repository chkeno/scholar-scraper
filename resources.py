"""Flask-restful resource module"""
from flask_restful import Resource, reqparse

from models import PublicationSchema
from repositories import ScholarRepository


class SearchResource(Resource):
    """
    Endpoint for searching scraped Google Scholar data
    """

    def __init__(self):
        """
        Constructor for SearchResource. Sets up any required Repository classes used by Resources
        """
        self.scholar_repository = ScholarRepository()
        self.publication_schema = PublicationSchema(many=True)

    def get(self):
        """
        GET endpoint for searching sqlite DB by article title (cap-insensitive substring search)
        :return: JSON representation of citation tree for articles matching searched title.
        """
        publications = []
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('citation_tree_depth', type=int)

        arguments = parser.parse_args()
        title = arguments.get('title')
        citation_tree_depth = arguments.get('citation_tree_depth')

        if citation_tree_depth is None:
            citation_tree_depth = 1

        if title is not None:
            publications = self.scholar_repository.search_by_title(title, citation_tree_depth)

        return self.publication_schema.dump(publications)
