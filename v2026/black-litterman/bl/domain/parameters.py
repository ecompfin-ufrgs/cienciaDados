"""Parâmetros do modelo Black-Litterman."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelParameters:
    """Configuração do modelo, validada ao ser criada.

    Regras: tau > 0, delta > 0 e 0 < max_weight <= 1.
    """

    tau: float = 0.05         # incerteza do prior
    delta: float = 2.5        # aversão ao risco
    max_weight: float = 0.20  # peso máximo por ativo

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        """Levanta ValueError se as regras não forem atendidas."""
        pass
