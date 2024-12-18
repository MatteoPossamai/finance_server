import dataclasses
import datetime
import enum

@dataclasses.dataclass
class Record:
    id: int
    date: datetime.datetime
    category: str
    amount: float
    currency: str

    def to_list(self):
        return [getattr(self, field.name) for field in dataclasses.fields(self)]

    @property
    def header(self):
        return [field for field in dataclasses.fields(self)]


@dataclasses.dataclass
class Income(Record):
    issuer: str


@dataclasses.dataclass
class Expense(Record):
    to: str


class RecordType(enum.Enum):
    Expense=Expense
    Income=Income