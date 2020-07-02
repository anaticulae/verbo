# changelog

Every noteable change is logged here.

## v0.9.9

## v0.9.8

## v0.9.7

## v0.9.6

## v0.9.5

## v0.9.4

## v0.9.3

## v0.9.2

## v0.9.1

## v0.9.0

## v0.8.2

### Fix

* replace with texmex code (2c1c2f358332)

## v0.8.1

### Fix

* upgrade later to enable using in hey project (66453ec3af3e)

## v0.8.0

### Feature

* improve yaml representation (f248ba03fbab)
* enable block quote feature for cli (e27de6c8e319)
* add method to dump and load block quotes, determine path (712247458c67)
* add simple algorithm to extract quotation mark blocks (20a27f9dd007)
* add feature blockquote to extract block quotes (1d266867f090)

## v0.7.0

### Feature

* add list extraction strategy to select between geometry/vertical (4ce7f19aa098)
* add vertical distance list parser (31130205def5)
* merge more than one list over pages together (d57b187f9a56)
* list parser - add list pattern with rectangle at front (b97cdfe0e22a)

## v0.6.2

## v0.6.1

### Feature

* add option to select quotation loader pages (2dd0a5401b76)

## v0.6.0

### Feature

* dump extracted quotation instead of full sentence (baad1153a782)
* add lists to quotation extractor (739bee700132)
* use page wise list indexing (8c61e65ee924)
* use extracted `lists` to determine which line is a list line (0aaaddf4b5e8)
* load content navigator very early (4bfb1ecc0987)
* add list geometry parser (499e5ae62bd6)
* add method to parse potential list with regex (214baed1ed83)
* add method to determine words list output path (06937923ef11)

### Fix

* overwrite method to extend usage with other data types (ee7fb13a8235)

### Documentation

* clean up documentation (03de659da693)

## v0.5.12

### Fix

* remove outdated moved code (1b9287e3207e)

## v0.5.11

## v0.5.10

## v0.5.9

## v0.5.8

## v0.5.7

## v0.5.6

### Fix

* convert level when having None entry (ae667b556ab6)

## v0.5.5

### Fix

* adjust toc extractor range (c70ac159ca34)

## v0.5.4

## v0.5.3

### Fix

* do not overwrite detected level (9ff7f0be723a)

## v0.5.2

## v0.5.1

## v0.5.0

### Fix

* fix headline level detector (cefe9684948e)
* fix expected subjects (6d207b3306c0)
* ignore sentence which are parsed as headlines (12eafcaac6fb)
* add check to exclude miss parsed footnotes as headline (bd21836e6467)

## v0.4.8

## v0.4.7

## v0.4.6

## v0.4.5

## v0.4.4

## v0.4.3

### Fix

* do not fail on wrong boxed output (8e511baa4cf8)

## v0.4.2

### Fix

* ensure to handle empty sentences correctly (60aa0b10d82d)

## v0.4.1

### Feature

* add method to load and dump quotation (79f6bc186992)

## v0.4.0

### Feature

* extract and dump sentences which contains quotation marks (e597fb9f4754)
* add quotation step to extract quotation out of sentences (32c296ec5fb3)
* add interface information (8faae023cda1)
* add option to select wanted behavior (53f1c63baa39)
* merge pages between headlines (d68a4b06751e)
* ensure to handle missing successor correctly (4a77d6686eb0)
* extend interface documentation (cd800f2cc0f1)
* extend validation interface (20687ac3d13b)
* add language dependency to quotation rule (a54ad4a11a1e)
* ensure position of double quotation (3d1e2ae8e888)
* extend sentence parser with more complex sentence structure (d010013bc13f)
* remove text division out of parsed sentences (3a69b2acb7c0)
* add quotation mark validator (3507c39e6ec1)
* add decider_textrule basic cli structure (892549773fc1)
* add quotation mark to avoid splitting in citation (aa4ca8d78d21)
* add single quotation marks (5fdabea19f88)

### Fix

* fix unit test (9d9c25e8c250)
* support multiple line headlines and do not fail on index error (6747ac538773)
* do not store empty sentences (ee1933dbf580)
* make test compatible to new API (571c21935ed1)
* ensure to handle headlines without content correctly (c09f4d4fa900)
* fix sentence ending check, remove unused variable (3a6f60d7a5eb)
* extend DUDEN whitelist (4b5e62c7039f)
* fix colon pattern (13e0ee25e8ea)
* ensure that failing alignment does not crash application (c833ca1405ae)

### Documentation

* add backlog to store upcoming features (96f5c99b11a1)

## v0.3.2

### Fix

* make interface more explicit (728e636818eb)

## v0.3.1

### Fix

* do not fail on empty pages (6f13412a110f)

## v0.3.0

### Feature

* add adapter to convert oneline alignments to layout alignments (4d203a7573e3)
* add method to extract alignment from path (0af1b36af1bc)

## v0.2.3

### Fix

* return None if no textfeed can be computed (64a01b05070b)

## v0.2.2

## v0.2.1

## v0.2.0

### Feature

* determine current alignment (5e1fea40312b)
* add step to determine expected alignment (405691d40928)
* add path module to determine output of generated steps (2bb73131c59e)
* add step to determine line endings for every oneline (176a7290bbe3)
* add textflow description (08b52776cbcb)
* add basic structure of textflow package (e9c44b975683)
* add method to determine expected alignment for every line (3dae72a4ec39)
* make TextAlignment sortable (e235c9b4ed4c)
* extend text block detection (80ecc73e5fdd)
* add method to determine alignment for every line (87491eaf7c2e)
* add method to determine text orientation (df1105d212b7)

### Fix

* do not convert single items (a6ae89a04870)
* fix incomplete implementation (202cf8446821)

## v0.1.7

## v0.1.6

## v0.1.5

## v0.1.4

## v0.1.3

### Fix

* remove disabled yaml formatter (2dea308f98d6)

## v0.1.2

## v0.1.1

## v0.1.0

### Feature

* move code from hey project (764d94914356)

### Fix

* generate required test data (6fdba6c77c23)

## v0.0.0 Initial release

