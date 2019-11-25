from typing import Optional

import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

poststore = None  # type: Optional[Collection]


def init(db: Database):
    global poststore
    poststore = db.poststore
    checkcollection()


def checkcollection():
    poststore.create_index([("trail", pymongo.DESCENDING)], sparse=True, background=True)
    poststore.create_index([("mtrail.$**", pymongo.DESCENDING)], sparse=True, background=True)
    poststore.create_index([("mh", pymongo.DESCENDING)], sparse=True, background=True)
    poststore.create_index([("cl", pymongo.DESCENDING)], sparse=True, background=True)
