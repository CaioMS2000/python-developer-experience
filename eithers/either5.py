from typing import Generic, TypeVar, Callable

T = TypeVar('T')
E = TypeVar('E')
U = TypeVar('U')

class Left(Generic[E, T]):
    def __init__(self, value: E) -> None:
        self.value: E = value
    
    def is_right(self) -> bool:
        return False
    
    def is_left(self) -> bool:
        return True

    def map(self, func: Callable[[T], U]) -> 'Left[E, T]': #pyright: ignore[reportUnusedParameter]
        return self  # Left não é afetado por map

    def bind(self, func: Callable[[T], 'Either[E, U]']) -> 'Left[E, T]': #pyright: ignore[reportUnusedParameter]
        return self  # Left não é afetado por bind

    def get_or_else(self, default: T) -> T:
        return default


class Right(Generic[E, T]):
    def __init__(self, value: T) -> None:
        self.value: T = value
    
    def is_right(self) -> bool:
        return True
    
    def is_left(self) -> bool:
        return False

    def map(self, func: Callable[[T], U]) -> 'Right[E, U]':
        return Right(func(self.value))

    def bind(self, func: Callable[[T], 'Either[E, U]']) -> 'Either[E, U]':
        return func(self.value)

    def get_or_else(self, default: T) -> T: #pyright: ignore[reportUnusedParameter]
        return self.value


Either = Left[E, T] | Right[E, T]

def left(value: E) -> Either[E, T]:
    return Left(value)

def right(value: T) -> Either[E, T]:
    return Right(value)

# Exemplo de uso
result: Either[str, int] = right(10).map(lambda x: x * 2)
print(result.value)  # 20

result = left("error").map(lambda x: x * 2)
print(result.value)  # "error"