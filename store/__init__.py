from pymongo.database import Database

import store.cborstore as cborstore
import store.dwclstore as dwclstore
import store.pointerstore as pointerstore
import store.poststore as poststore
import store.urlstore as urlstore


def init(db: Database):
    cborstore.init(db)
    dwclstore.init(db)
    pointerstore.init(db)
    poststore.init(db)
    urlstore.init(db)
