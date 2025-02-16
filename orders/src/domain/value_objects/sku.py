from dataclasses import dataclass


@dataclass(frozen=True)
class SKU:
    value: str

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SKU):
            return False

        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)
