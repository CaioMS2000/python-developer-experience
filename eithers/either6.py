from __future__ import annotations
from typing import TypeVar, Generic, Callable, override
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Define tipos genéricos para Left, Right e transformações
L = TypeVar("L")  # Tipo do erro
R = TypeVar("R")  # Tipo do sucesso
T = TypeVar("T")  # Tipo para transformações
U = TypeVar("U")  # Tipo adicional para transformações do Left


class Either(Generic[L, R], ABC):
    """
    Classe abstrata base que representa um resultado que pode ser
    sucesso (Right) ou erro (Left).
    """

    @abstractmethod
    def is_right(self) -> bool:
        """Retorna True se é um Right, False se é um Left."""
        pass

    def is_left(self) -> bool:
        """Retorna True se é um Left, False se é um Right."""
        return not self.is_right()

    @abstractmethod
    def map(self, f: Callable[[R], T]) -> Either[L, T]:
        """
        Aplica uma função ao valor se for Right, mantém o erro se for Left.
        """
        pass

    @abstractmethod
    def map_left(self, f: Callable[[L], U]) -> Either[U, R]:
        """
        Aplica uma função ao erro se for Left, mantém o valor se for Right.
        """
        pass

    @abstractmethod
    def flat_map(self, f: Callable[[R], Either[L, T]]) -> Either[L, T]:
        """
        Aplica uma função que retorna Either ao valor se for Right.
        """
        pass

    @abstractmethod
    def get_or_else(self, default: R) -> R:
        """
        Retorna o valor se for Right, ou o valor default se for Left.
        """
        pass

    @abstractmethod
    def fold(self, left_f: Callable[[L], T], right_f: Callable[[R], T]) -> T:
        """
        Aplica left_f se for Left, right_f se for Right.
        """
        pass


@dataclass(frozen=True)
class Left(Either[L, R]):
    """Representa um erro/falha na computação."""

    value: L

    @override
    def is_right(self) -> bool:
        return False

    @override
    def map(self, f: Callable[[R], T]) -> Either[L, T]:
        return Left[L, T](self.value)

    @override
    def map_left(self, f: Callable[[L], U]) -> Either[U, R]:
        return Left[U, R](f(self.value))

    @override
    def flat_map(self, f: Callable[[R], Either[L, T]]) -> Either[L, T]:
        return Left[L, T](self.value)

    @override
    def get_or_else(self, default: R) -> R:
        return default

    @override
    def fold(self, left_f: Callable[[L], T], right_f: Callable[[R], T]) -> T:
        return left_f(self.value)


@dataclass(frozen=True)
class Right(Either[L, R]):
    """Representa um sucesso na computação."""

    value: R

    @override
    def is_right(self) -> bool:
        return True

    @override
    def map(self, f: Callable[[R], T]) -> Either[L, T]:
        return Right[L, T](f(self.value))

    @override
    def map_left(self, f: Callable[[L], U]) -> Either[U, R]:
        return Right[U, R](self.value)

    @override
    def flat_map(self, f: Callable[[R], Either[L, T]]) -> Either[L, T]:
        return f(self.value)

    @override
    def get_or_else(self, default: R) -> R:
        return self.value

    @override
    def fold(self, left_f: Callable[[L], T], right_f: Callable[[R], T]) -> T:
        return right_f(self.value)


def of_right(value: R) -> Either[L, R]:
    """Cria uma instância de Right com o valor fornecido."""
    return Right[L, R](value)


def of_left(error: L) -> Either[L, R]:
    """Cria uma instância de Left com o erro fornecido."""
    return Left[L, R](error)


def try_catch(f: Callable[[], R]) -> Either[Exception, R]:
    """
    Executa uma função que pode lançar exceção e retorna:
    - Right com o resultado se sucesso
    - Left com a exceção se falha
    """
    try:
        return Right[Exception, R](f())
    except Exception as e:
        return Left[Exception, R](e)
