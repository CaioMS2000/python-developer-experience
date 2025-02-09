from __future__ import annotations
from typing import TypeVar, Generic, Callable, TypeAlias, cast, override
from abc import ABC, abstractmethod

# Definindo tipos genéricos
L = TypeVar("L")  # Tipo do valor de Left
R = TypeVar("R")  # Tipo do valor de Right
T = TypeVar("T")  # Tipo genérico para transformações

# Alias para Either
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
    def bind(self, func: Callable[[R], Result[L, T]]) -> Result[L, T]:
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
    def map(self, func: Callable[[R], T]) -> Result[L, T]:
        return self  # Left não é afetado por map

    @override
    def bind(self, func: Callable[[R], Result[L, T]]) -> Result[L, T]:
        return self  # Left não é afetado por bind

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
    def map(self, func: Callable[[R], T]) -> Result[L, T]:
        new_value = func(self.value)
        return Right(new_value)  # Aplica a função ao valor e retorna um Right

    @override
    def bind(self, func: Callable[[R], Result[L, T]]) -> Result[L, T]:
        return func(self.value)  # Aplica a função e retorna o novo Either

    @override
    def get_or_else(self, default: R) -> R:
        return self.value  # Retorna o valor interno

# Funções auxiliares
def left(value: L) -> Result[L, object]:
    return Left(value)

def right(value: R) -> Result[object, R]:
    return Right(value)