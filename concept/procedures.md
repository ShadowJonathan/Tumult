
### store terminology
dwclstore:      _id:        `cbor` multihash of `"payload"`,
                payload:    bare `object`,
                (mh):       *optional* `multihash` denoting Processed `tumult.dwcl`.

urlstore:       _id:    URL in `str`,
                cid:    IPFS object's Content ID.

poststore:      _id:        `post_id`,
                `...`:      `...`,
                (trail):    *optional* deadweight+cl **oldest-first** `[dwcl-mh,]` array,
                (mtrail):   *optional* `post_id` -> `dwcl-mh` mapping,
                (dw):       *optional* deadweight `[dwcl-mh,]` array,
                (cl):       *optional* `dwcl-mh`.

pointerstore:   _id:    `post_id`,
                mh:     `multihash` in `cborstore`,
                ghost:  `bool`.

cborstore:      _id:    `multihash` of `"cbor"`,
                cbor:   `cbor` bytes of object,
                type:   `str` denoting type in `tumult.*` fashion.

### Long-running DWCL processor

Meant to run in a background job, periodically sweeping across all DWCL objects, downloading media when referenced.

```python
for dwcl in dwclstore:

    # Ensure we don't process unnecessary stuff.
    if dwcl.mh is not None:

        # Make a copy for the local workset
        copy = dwcl.payload.copy()

        # Extra processing if content has media with it
        if "media" in copy.content[image:video:audio]:
            
            # Extra processing if media is coming from image, trim bloat.
            if content is 'image':
                trim_image_media_array(copy)

            # Download Media, add to urlstore, and store CID alongside URL
            media = dwcl.content.media
            CID = ipfs.store(media.url.download())
            urlstore.add(_id=media.url, cid=CID)
            media.cid = CID

        copy['type'] = "tumult.dwcl"

        cbor_bytes = cbor.dumps(copy)
        mh = multihash.make(cbor_bytes)

        # Store resolved DWCL into cborstore
        cborstore.insert(_id=mh, cbor=cbor_bytes, type="tumult.dwcl")

        # Store multihash with original DWCL
        dwclstore[dwcl._id].mh = mh
```

### Compile procedure

[//]: # (WIP)

1. select post from `poststore`

2. walk all referenced content/dw hashes (in dw, content or trail) in `contentstore`

    1. test if content/dw has CID saved with them, if so, skip section
    
        1. copy content/dw to temp cbor

        2. scan content/dw for media, if none, skip section

            1. test if URLs are in `mediastore`, **if not, skip compilation for current post**]
            
            2. add CIDs to URLs with content/dw in temp cbor
        
        3. 