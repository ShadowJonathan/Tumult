### Core

All objects are `dal-cbor` serialized, all keys or components sorted/conformed in a way that any object always serialises back into the same `cbor` bytes.

### Definitions in this document

#### Mutable vs Immutable

All IPLD objects are immutable by design, but these objects sometimes represent WIP versions of those objects.

"Mutability" hereby refers to the fact that any object in these categories can be *replaced* by a more "complete", "latest" or "correct" version.

Thus a "Mutable" object can either be replaced by an Immutable or another Mutable version, or eventually become obsolete by completeness of data in other objects.

#### Processed vs Derivative

"Processed" refers that the object has an "original", but has only been edited (CIDs replacing URLs, CIDs added for additional data, structure cleaned up, ultra-mutable keys (like note count on a Tumblr post) removed) to make it acceptable for IPLD format.

"Derivative" refers that the object is "virtual" or "pseudo" in the sense that it's there for indexing and pointing to other objects (like a `tumult.tree` object).

All objects have a key `"type"`, this key denotes the type of the object, **this key must always be present on all objects**.

### `tumult.media.ledger`

> Immutable
>
> Derivative

10000-length media CID pointer block.

```json5
{
  "type": "tumult.media.ledger",

  "media": [
    {"/": "QmUG9GckfqFhfpuAQg4zsMUegQES5CKh2eCq9Gph293Rxh"},
    // etc...
  ],
  "next": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"} // null on genesis block
}
```

### `tumult.media.binder`

> Mutable (into `tumult.media.ledger`)
>
> Derivative

<10000-length media CID pointer block, used as entrypoint to ledger chain, and contains latest or last-added media objects as "leftovers", will eventually be filled and turned into ledger block.

```json5
{
  "type": "tumult.media.binder",

  "media": [
    {"/": "QmUG9GckfqFhfpuAQg4zsMUegQES5CKh2eCq9Gph293Rxh"},
    // etc...
  ],
  "next": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"}
}
```

### `tumult.post`

> Immutable
>
> Processed
>
> (Note, can be updated with a new original version)

A post object that has been directly scraped. This object denotes the state of the post as it was when it was ingested.

**It is possible that these objects still get updated, altough only to denote a *new complete state* (edit, addition of tags, other), thus this object is still immutable, and all "old" objects are still valid, albeit outdated.**

```json5
{
  "type": "tumult.post",

  "id": 188921992027,
  "blog": "t:BySBnKuwMY6d5MlD67eJzg",
 
  // Fields that come with a complete post
  "timestamp": "2008-06-04T18:39:44Z",
  "tags": ["these", "are", "some", "tags"],
 
  // ContentLayout, resolves to tumult.dwcl
  "cl": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"},

  // DeadWeight, Optional, resolves to tumult.dwcl
  "dw": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"},
  
  // Reblog Trail, Optional, resolves to tumult.trail
  "trail": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"}
}
```

### `tumult.post.ghost`

> Mutable (into `tumult.post`)
>
> Derivative

A post object that has not yet been directly scraped, and is instead *resolved* through reblog references of other posts.

Due to the nature of Tumblr, with it's ability to edit original content while reblogging, a virtual post like this can have two states: Conflict and Consensus.

Conflict is when reblogs of this post give different content of this post, when there has been an edit somewhere along the chain.

Consensus is when reblogs of this post all return the same content of this post.

Due to brevity, deadweight is not added to this post, but can be found by traversing `tumult.conflict.witnesses` objects linked to this object, in their `tumult.trail` objects.

#### Conflict situation
```json5
{
  "type": "tumult.post.ghost",

  "id": 188921992027,
  "blog": "t:BySBnKuwMY6d5MlD67eJzg",
 
  // ContentLayout, resolves to tumult.conflict
  "cl.conflict": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"},
}
```

#### Consensus situation
```json5
{
  "type": "tumult.post.ghost",

  "id": 188921992027,
  "blog": "t:BySBnKuwMY6d5MlD67eJzg",
 
  // Consensus ContentLayout, resolves to tumult.dwcl
  "cl": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"},
  
  // Additional list of posts that give consensus that this post has this specific content and layout.
  // Resolves to tumult.conflict.witnesses
  "cl.witnesses": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"},
}
```

### `tumult.trail`

> Immutable
>
> Derivative

A trail object, noting down the post's reblog history, **oldest-first**.

```json5
{
  "type": "tumult.trail",

  // Trail objects can be one of two things;
  // - Post ID with DWCL
  // - DeadWeight denotation with DWCL
  // These can be differentiated between the "post" key having an int, or null.
  "trail": [

    // Post ID with DWCL
    {
      "post": 123,
      "cl": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"}
    },

    // DeadWeight denotation with DWCL
    {
      "post": null,
      "dw": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"}
    }
  ] 
}
```

### `tumult.dwcl`

> Immutable
>
> Processed

DWCL, standing for DeadWeight Content Layout, an amalgamation of those three types of data into one object.

DeadWeight is a result of Tumblr trying to fix their site when they switched over to NPF (Neue Post Format, replacing HTML with Blocks), when reblogs have already been made, and their original blogs have been deleted/switched to a different URL.

Tumblr inserts "broken trail objects" in the reblog trail whenever such a situation has occured. These objects are referenced as "dead weight" because that is their function, they do not refer to any specific post, but instead give an echo of one. These objects are irrecoverable to their original status, but also cannot be omitted from the reblog chain.

In any post (or deadweight), two values are key to the actual post content: `"content"` and `"layout"`.

A DWCL object either holds the content+layout of a post, or the content+layout+metadata of a deadweight object.

Note: Any media block does not (and should not) use IPLD syntax with the CID that they use to refer to the IPFS object.
This is to prevent a pin of the top `tumult.tree` object (that indexes all `tumult.post`+`tumult.post.ghost` objects) to resolve the enormous amount of media that is recursively referenced in every post, and start storing it's giga/terabytes of data.

Instead, any media object is correctly referenced in `tumult.media.*` objects, which are in turn chained together, and finally referenced in the `tumult.megapin` object.

```json5
{
  "type": "tumult.dwcl",

  "payload": {

     // List of NPF blocks
    "content": [

      // All media objects (image, video, audio) will have CIDv1 base64 values in "cid" alongside "url", 
      // pointing to a IPFS version of the file

      // In image blocks, media object arrays are trimmed to just one value (replacing the original array) with the highest dimensional scale.
      // This is to reduce bloat.

    ],
    
    // NPF post layout.
    // See https://www.tumblr.com/docs/npf#layout-blocks
    // TODO: update above link with IPFS-saved version.
    "layout": [],

    // DeadWeight has an additional field like below, denoting a Tumblr-provided "original" blog
    "broken_blog": "a-deleted-blog"
 
    // Note: Payload can potentially have more values than mentioned above.
  }
}
```

### `tumult.conflict`

> Mutable
>
> Derivative

An object holding information about a `tumult.post.ghost`'s potential content, but where no consensus exists between all reblogs.

```json5
{
  "type": "tumult.conflict",
  
  // An array of tumult.conflict.witnesses objects paired with tumult.dwcl objects
  "testimony": [
    {
      // A tumult.dwcl object that these posts perceive
      "cl": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"},
 
      // A tumult.conflict.witnesses object denoting posts that perceive this tumult.dwcl object
      "witnesses": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"},

      // A number for the sake of usability.
      // Is generated by grabbing the length of the array of "posts" in this above tumult.conflict.witnesses object.
      "tally": 18,
    },
    // etc...
  ] 
}
```

### `tumult.conflict.witnesses`

> Mutable
>
> Derivative

An array of posts that give witness to a consensus of post content, be it conflicting or communal.

```json5
{
  "type": "tumult.conflict.witnesses",

  "posts": [
    123, 
    234, 
    345, 
    567, 
    // etc...
  ] 
}
```

### `tumult.tree`

> Mutable
>
> Derivative

[//]: # (TODO)

### `tumult.megapin`

> Mutable
>
> Derivative

The MegaPin, referring to the latest top `tumult.tree` node, and the latest `tumulr.media.binder` node.

It is called a "mega pin" because of it's recursive reference to the entirety of a tumult archive, with all post metadata, and all media files. A IPFS cluster can use this pin to grab and store the entirety of an tumult archive.

This pin is to be updated with the latest media binder *first*, then with the latest top tree node. Media files are much more difficult to get (from Tumblr) and store than the entirety of metadata of all posts.

Note: Possibly in the future the spec of this object will be updated to include latest Note counts, or Blog metadata.

```json5
{
  "type": "tumult.megapin",
 
  // Exact timestamp of finalization of this object, denotes point in time of tumult archive version.
  "timestamp": "2019-06-04T18:39:44Z",
  
  // Top tumult.tree object, resolving down all metadata of posts
  "posts": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"},

  // Latest tumult.media.* object in the chain
  "media": {"/": "bafyreidz4nwpyn3kjy6vccylo4d5cheo4f2pflmfsigmdizzdn6kayijn4"}
}
```