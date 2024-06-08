from typing import Protocol
from typing import Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class BaseTransactionInfo(Protocol):
    type_category: str
    first_name: str
    chat_id: Optional[str] = None
    category: Optional[str] = None
    date: Optional[datetime] = None
    amount: Optional[float] = None
