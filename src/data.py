import uuid
from dataclasses import dataclass
from pathlib import Path

import pandas as pd


@dataclass(slots=True, kw_only=True)
class Order:
    time: int
    message_type: str
    price: float
    queue_position: int
    size: int
    order_id: uuid.UUID


class DataImporter:
    PROJECT_ROOT = Path().absolute()
    DATA_PATH = f'{PROJECT_ROOT}/data.csv'

    def __init__(self, data_path=DATA_PATH):
        self.df: pd.DataFrame = pd.read_csv(data_path)
        self.df.columns = ['time', 'message_type', 'price', 'queue_position', 'size', 'order_id']

    def read(self) -> list[Order]:
        return [Order(**kwargs) for kwargs in self.df.to_dict(orient='records')]

    def find_min_max_prices(self) -> (float, float):
        max_val = self.df.max(axis=0)['price']
        min_val = self.df[self.df['price'] != 0].min(axis=0)['price']
        return min_val, max_val
