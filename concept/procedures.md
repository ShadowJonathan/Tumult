There are three main database categories:

# store terminology
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
                
postpointer:    _id:    `post_id`,
                mh:     `multihash` in `cborstore`,
                ghost:  `bool`.

cborstore:      _id:    `multihash` of `"cbor"`,
                cbor:   `cbor` bytes of object,
                type:   `str` denoting type in `tumult.*` fashion.

# Content sweep

[//]: # (WIP)

1. select content from `contentstore`

# Compile procedure

[//]: # (WIP)

1. select post from `poststore`

2. walk all referenced content/dw hashes (in dw, content or trail) in `contentstore`

    1. test if content/dw has CID saved with them, if so, skip section
    
        1. copy content/dw to temp cbor

        2. scan content/dw for media, if none, skip section

            1. test if URLs are in `mediastore`, **if not, skip compilation for current post**]
            
            2. add CIDs to URLs with content/dw in temp cbor
        
        3. 