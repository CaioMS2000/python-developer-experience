from __future__ import annotations
from typing import Any, TypeAlias, TypeVar, Generic, Callable, override
from dataclasses import dataclass
from abc import ABC, abstractmethod

L = TypeVar('L')
R = TypeVar('R')
T = TypeVar('T')

class Left(Generic[L]):
    value: L

    def __init__(self, value: L) -> None:
        self.value = value
    
    def is_left(self) -> bool:
        return True

    def is_right(self) -> bool:
        return False

    def map(self, func: Callable[[R], T]) -> Left[L]:
        return self

    def bind(self, func: Callable[[R], Left[L] | Right[T]]) -> Left[L]:
        return self

    def get_or_else(self, default: R) -> R:
        return default


class Right(Generic[R]):
    value: R

    def __init__(self, value: R) -> None:
        self.value = value
    
    def is_left(self) -> bool:
        return False
    
    def is_right(self) -> bool:
        return True
    
    def map(self, func: Callable[[R], T]) -> Right[T]:
        return Right(func(self.value))
    
    def bind(self, func: Callable[[R, *tuple[Any, ...]], Left[L] | Right[T]]) -> Left[L] | Right[T]:
        return func(self.value)

    def get_or_else(self, default: R) -> R:
        return self.value if self.value is not None else default

Either: TypeAlias = Left[L] | Right[R]

def left(value: L) -> Either[L, R]:
    return Left(value)

def right(value: R) -> Either[L, R]:
    return Right(value)

x = left(ValueError)
