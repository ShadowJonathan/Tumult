There are three main database categories:

# store terminology
contentstore:   original content/dw saved by `cbor-mhash`,
                note if object is content or deadweight,
                post_id this content is associated with,
                optional CID pointing to `cborstore` with fully resolved cbor object (with media CIDs also resolved)

poststore:      original post object,
                optionally (when downloaded) has content + hash pointing to `contentstore`,
                optionally has dw + hash pointing to `contentstore`,
                optionally has trail + hashes pointing to `contentstore`

mediastore:     url to CID mapping

# Object classification

Media: Immutable

Content/DW: Immutable/Dependent Immutable

Trail: Dependent Immutable

Post: Dependent Immutable

Tree: Updating Immutable

## Terminology
Immutable: Immutable upon creation

Dependent Immutable: Needs other object's Immutable CID to be created

Updating Immutable: Only dependant on indexing other's CIDs and update them

# Content sweep

1. select content from `contentstore`

# Compile procedure

1. select post from `poststore`

2. walk all referenced content/dw hashes (in dw, content or trail) in `contentstore`

    1. test if content/dw has CID saved with them, if so, skip section
    
        1. copy content/dw to temp cbor

        2. scan content/dw for media, if none, skip section

            1. test if URLs are in `mediastore`, **if not, skip compilation for current post**]
            
            2. add CIDs to URLs with content/dw in temp cbor
        
        3. 