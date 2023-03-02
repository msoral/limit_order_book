from dataclasses import dataclass

import config


@dataclass(frozen=True, slots=True)
class TopOfTheBookResult:
    price: float
    size: int

    @property
    def total_value(self) -> float:
        return float(config.FLOAT_SIGNIFICANT_DIGIT_FORMAT.format(self.price * self.size))

    def __repr__(self):
        return f"TopOfTheBookResult(price={self.price}, size={self.size}, total_value={self.total_value}"
