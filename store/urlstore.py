from typing import Optional

from pymongo.collection import Collection
from pymongo.database import Database

urlstore = None  # type: Optional[Collection]


def init(db: Database):
    global urlstore
    urlstore = db.urlstore
