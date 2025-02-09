from typing import Generic, TypeVar

# Definindo tipos genéricos para o valor de sucesso e o erro
T = TypeVar('T')  # Tipo do valor de sucesso
U = TypeVar('U')  # Tipo do valor transformado (usado em map e bind)
E = TypeVar('E', bound=Exception)  # Tipo do erro (deve ser uma exceção)

class Either(Generic[E, T]):
    """
    Classe base para representar um resultado que pode ser um erro (Left) ou um sucesso (Right).
    Aqui, o erro está à esquerda (E) e o sucesso à direita (T).
    """

    def __init__(self, value: E | T, is_right: bool):
        self._value = value
        self._is_right = is_right

    def is_right(self) -> bool:
        """Retorna True se o resultado for um sucesso (Right)."""
        return self._is_right

    def is_left(self) -> bool:
        """Retorna True se o resultado for um erro (Left)."""
        return not self._is_right

    def get_or_else(self, default: T) -> T:
        """
        Retorna o valor contido se for um sucesso (Right).
        Caso contrário, retorna o valor padrão `default`.
        """
        value: T = self._value
        return value if self.is_right() else default

    def __repr__(self) -> str:
        status = "Right" if self.is_right() else "Left"
        return f"{status}({self._value})"

class Right(Either[E, T]):
    """Classe que representa um sucesso (Right)."""

    def __init__(self, value: T):
        super().__init__(value, is_right=True)

class Left(Either[E, T]):
    """Classe que representa um erro (Left)."""

    def __init__(self, error: E):
        super().__init__(error, is_right=False)

# Exemplo de uso
def divide(a: float, b: float) -> Either[ZeroDivisionError, float]:
    """Divide dois números, retornando um Either[ZeroDivisionError, float]."""
    if b == 0:
        return Left(ZeroDivisionError("Division by zero"))
    return Right(a / b)

# Testando a função divide
result = divide(10, 2)
print(result)  # Right(5.0)

result = divide(10, 0)
print(result)  # Left(ZeroDivisionError("Division by zero"))
