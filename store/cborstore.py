from typing import Optional

import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

cborstore = None  # type: Optional[Collection]


def init(db: Database):
    global cborstore
    cborstore = db.cborstore
    checkcollection()


def checkcollection():
    cborstore.create_index([("type", pymongo.DESCENDING)], background=True)
