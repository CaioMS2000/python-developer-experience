from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E")
# U = TypeVar('U')
# E = TypeVar('E', bound=Exception)


class Left(Generic[E, T]):
    def __init__(self, value: E) -> None:
        self.value: E = value

    def is_right(self) -> bool:
        return False

    def is_left(self) -> bool:
        return True


class Right(Generic[E, T]):
    def __init__(self, value: T) -> None:
        self.value: T = value

    def is_right(self) -> bool:
        return True

    def is_left(self) -> bool:
        return False


Either = Left[E, T] | Right[E, T]


def left(value: E) -> Either[E, T]:
    return Left(value)


def right(value: T) -> Either[E, T]:
    return Right(value)
