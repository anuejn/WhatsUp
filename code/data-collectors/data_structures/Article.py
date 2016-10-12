class Article:
    """
    This class represents an basic article and is the basic data format used in the DB
    """
    def __init__(self, title, subtitle, text, author, category, timestamp):
        self.title = title
        self.subtitle = subtitle
        self.text = text

        # metadata
        self.author = author
        self.category = category
        self.timestamp = timestamp