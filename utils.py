import hashlib

import cbor
import cid
import cid.cid
import multihash


def make_cbor(obj: object) -> bytes:
    return cbor.dumps(obj, sort_keys=True)


def make_cbor_sha256_multihash(obj: object) -> bytes:
    cbor_obj = make_cbor(obj)
    hash_digest = hashlib.sha256(cbor_obj).digest()
    return multihash.encode(hash_digest, "sha2-256")


def make_cbor_cid(obj: object) -> cid.cid.BaseCID:
    mh = make_cbor_sha256_multihash(obj)
    return cid.make_cid(1, "dag-cbor", mh)
