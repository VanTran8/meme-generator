"""Module for QuoteModel Class."""

class QuoteModel:
    """Represent models for Quote."""

    def __init__(self, body: str, author: str):
        """Create a QuoteModel object with specific body and author.

        :param body: content of the quote
        :param author: author of the quote
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Retun a string representation of the quote."""
        return f"'{self.body}' - {self.author}"