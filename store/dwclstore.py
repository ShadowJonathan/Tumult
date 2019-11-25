from typing import Optional

import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

dwclstore = None  # type: Optional[Collection]


def init(db: Database):
    global dwclstore
    dwclstore = db.dwclstore
    checkcollection()


def checkcollection():
    dwclstore.create_index([("mh", pymongo.DESCENDING)], sparse=True, background=True)
