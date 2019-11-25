from typing import Optional

import pymongo
from pymongo.collection import Collection
from pymongo.database import Database

urlstore = None  # type: Optional[Collection]


def init(db: Database):
    global urlstore
    urlstore = db.urlstore
    checkcollection()


def checkcollection():
    urlstore.create_index([("mh", pymongo.DESCENDING)], background=True)
    urlstore.create_index([("ghost", pymongo.DESCENDING)], background=True)
