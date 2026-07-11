class ParserError(Exception):
    pass


class UnknownProduct(ParserError):
    pass


class UnknownReason(ParserError):
    pass


class InvalidQuantity(ParserError):
    pass


class EmptyMessage(ParserError):
    pass

class InvalidQuantity(Exception):
    """Не удалось определить количество."""
    pass