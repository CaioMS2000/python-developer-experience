from __future__ import annotations
from typing import TypeVar, Generic, Callable, TypeAlias, cast, override
from abc import ABC, abstractmethod

# Definindo tipos genéricos
L = TypeVar("L")  # Tipo do valor de Left
R = TypeVar("R")  # Tipo do valor de Right
T = TypeVar("T")  # Tipo genérico para transformações

# # Alias para Either
Result: TypeAlias = "Left[L, R] | Right[L, R]"


# Classe base abstrata para Either
class Either(Generic[L, R], ABC):
    @property
    @abstractmethod
    def is_left(self) -> bool:
        pass

    @property
    @abstractmethod
    def is_right(self) -> bool:
        pass

    @abstractmethod
    def map(self, func: Callable[[R], T]) -> Result[L, T]:
        pass

    @abstractmethod
    def bind(self, func: Callable[[R], Either[L, T]]) -> Result[L, T]:
        pass

    @abstractmethod
    def get_or_else(self, default: R) -> R:
        pass


# Classe Left
class Left(Either[L, R]):
    value: L

    def __init__(self, value: L) -> None:
        self.value = value

    @property
    @override
    def is_left(self) -> bool:
        return True

    @property
    @override
    def is_right(self) -> bool:
        return False

    @override
    def map(self, func: Callable[[R], T]) -> Either[L, T]:
        # Left não é afetado por map
        return self

    @override
    def bind(self, func: Callable[[R], Either[L, T]]) -> Either[L, T]:
        # Left não é afetado por bind
        return self

    @override
    def get_or_else(self, default: R) -> R:
        return default  # Retorna o valor padrão


# Classe Right
class Right(Either[L, R]):
    value: R

    def __init__(self, value: R) -> None:
        self.value = value

    @property
    @override
    def is_left(self) -> bool:
        return False

    @property
    @override
    def is_right(self) -> bool:
        return True

    @override
    def map(self, func: Callable[[R], T]) -> Either[L, T]:
        new_value = func(self.value)
        new_right = cast(Right[L, T], Right(new_value))

        return new_right  # Aplica a função ao valor

    @override
    def bind(self, func: Callable[[R], Either[L, T]]) -> Either[L, T]:
        return func(self.value)  # Aplica a função e retorna o novo Either

    @override
    def get_or_else(self, default: R) -> R:
        return self.value  # Retorna o valor interno


# Funções auxiliares
def left(value: L) -> Either[L, object]:
    return Left(value)


def right(value: R) -> Either[object, R]:
    return Right(value)
