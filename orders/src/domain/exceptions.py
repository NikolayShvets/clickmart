class DomainError(Exception):
    pass


class MoneyIsNotPositiveError(DomainError):
    pass


class EmptyOrderItemError(DomainError):
    pass


class EmptyOrderError(DomainError):
    pass


class StockIsBelowZeroError(DomainError):
    pass


class OutOfStockError(DomainError):
    pass


class AllocationMismatchError(DomainError):
    pass
