# changelog

Every noteable change is logged here.

## v1.22.0

### Feature

* extend invalid chars (e24cfb3de751)
* use new lists resources (f67364f2db24)

## v1.21.0

### Feature

* look around to find referenced abbreviation (55ac53ab141e)

## v1.20.1

### Feature

* increase max distance to merge sentences (eccaccf35c2e)

## v1.20.0

### Feature

* use smarter sentence selector (15d6e3bac80c)
* add improve bounding merger (271174378bb2)
* add method to find bounding of a sentence on a page (d5434760bb94)
* add sentence bounding determiner (f1b11258ba18)

## v1.19.0

## v1.18.0

### Feature

* add colon list type (874c0740059b)

## v1.17.2

## v1.17.1

### Fix

* do not fail on non existing list (586196c2bf8d)
* do not fail on empty finding (5af2504ac704)

## v1.17.0

### Feature

* use headlines from headlines package (25dfcd48db30)

### Fix

* handle empty headline correctly (2bf792ee0aa2)

## v1.16.0

### Feature

* detect local links (64f8b78f55d4)

## v1.15.1

### Fix

* adjust word merge after upgrading rawmaker (2d2530c18d17)

## v1.15.0

### Feature

* add magic flag to preserve highnotes (b9ca1b6b5f6d)

### Fix

* clarify error message (df19d1fa831c)

## v1.14.2

## v1.14.1

### Fix

* fix missing import (d0138253976b)

## v1.14.0

### Feature

* add module to mark quotes (c8a32669c726)
* add package to analyze sentences (823605a82d7e)

## v1.13.0

### Feature

* use global text distance to improve vertical lists parser (c154c22dd21f)
* dump extraction strategy (7191d97c5710)
* use page independent list identifier (5a89ef1bdde8)
* use list identifier to improve page lookup (35ddf821314f)
* add list lookup over more than one page (ceb44c6368ce)
* increase tolerance to build bigger groups (6521b8cc8bbd)
* normalize list content (25047837d2fc)

### Fix

* adjust list content on overlapping pages (a32e3667855e)
* disable equal feed check, its not used at the moment (3d652561cb2d)
* do not lose headline information (b315ff37634e)

### Documentation

* add module documentation (126cb695af51)
* increase documentation (97ab5b6b1577)
* extend interface documentation (0d0fed1cdb73)

## v1.12.0

### Feature

* add headline surround improver (91d116602361)
* add level four to oneline headlines (5640cb817250)
* skip too many level four headlines (c509b434b61f)
* increase debugging information (9de0512c65ad)
* debug merge selection (5ad5009a3b97)
* improve patch detector (a7a70eba2108)

### Fix

* skip noheadlines to improve result (cd386ff31039)

### Documentation

* increase interface documentation (b86f5fc43476)

## v1.11.0

### Feature

* increase possible headline mean length (0654ac1a9ced)
* add extra headline validation step (ecab1d50fc3d)
* add support for roman number (c691121b327d)
* merge first level headlines if required (7afb8978b343)
* remove multiple detected first level headlines (b0812ab85053)
* enable number large pattern (a9dd0e181438)
* add first level with number pattern (05bfcfc19ddd)

### Fix

* do not fail on empty ptn (2d421808eafe)
* do not skip level one only (73d5a5a82715)

### Documentation

* adjust modules (68228319fd89)

## v1.10.0

### Feature

* use second try if no headline detection is possible (2dc991d6afe7)

### Fix

* adjust return value (76928568bdaa)

### Documentation

* Happy New Year! (a5b73df5a377)

## v1.9.1

### Fix

* fix index accessing (c6388948b750)
* do not fail on tuple index (9f4bcb6bddef)

## v1.9.0

### Feature

* use cache to reduce computation time (96c18841d2bd)
* extend invalid abbr pattern (43c52587f674)
* use sentence as parsing source (6a6ab69f0524)
* add method to determine that line is a internal line (4bc6c63781ef)
* add abbr path (b956799b8775)
* use improved no headline checker (6fd9e9647c77)

### Fix

* ensure that index is in bounds (70df6b3f891b)
* reduce numbers of lines for a single page (ed2605be5a27)
* adjust imports after upgrading elements (95ad9e381104)

## v1.8.0

### Feature

* use single page strategy to extend cluster (14bb8950b37c)
* add method to run second strategy (8baf021e2f65)
* add single page headline extractor (9a949bced26b)
* merge line after to detected headline (0695f1f450fd)
* add method to detect multiline headlines (77bd35ff4c6f)

## v1.7.1

### Fix

* do not add formulas twice (c7aa606b6af7)
* add missing import (ec4f875a0379)

## v1.7.0

### Feature

* integrate parse raw formulas (507373fd98d3)
* add bounding to document type item (c0466e69ad93)
* load formulas data (cde9e13a39cd)

## v1.6.0

### Feature

* make find start and end less strict (fff5e2d85489)
* improved parsed area of geometry list (fa7af77d2cfd)

## v1.5.1

### Fix

* remove magic parameter (5b51cc636ead)

## v1.5.0

### Feature

* remove undefined (de06a47085dd)
* add option to dump different undefined types (33e65527c1b8)
* add method to split lists if necessary (fe2160e1001c)
* split sentences inside list items (006290dfcfdc)
* update pages attribute also (6cf036f3c69d)
* split list items into sentences (8481675447d0)

### Documentation

* adjust interface documentation (9a3110c3b019)
* extend interface documentation (4aa9328266ea)

## v1.4.0

### Feature

* add method to check if line is list chunk (716ba158ae79)
* add sentences step to generate sentences directly (501d43c69aeb)
* add option to parse more complex undefined data (117725bc2d4f)

### Fix

* do not fail when index and headlines does not fit together (bb1f98cadbcd)

## v1.3.0

### Feature

* add improved magics lookup mechanism (49fff69068b0)
* use oneline content to parse text (58788f434888)
* skip too many empty list items (9a79f8da251a)
* use improved list lookup to distinguish list item content (cc430f3e9000)
* split area by list item content (0a0e36d59eef)

### Fix

* do not analyze text content (a1714e787114)

### Documentation

* extend interface documentation (12c16ae3cf9c)

## v1.2.0

### Feature

* add option to return list separator (809ab0c2bc83)
* use regex to match list item start (d65cb695bc11)
* use improved list splitter (cb5bfc493d50)

### Fix

* adjust start correctly (2853e7e1fabf)
* disable last one fixer (93746c107319)
* adjust single content item (75cd98deba11)

## v1.1.1

### Fix

* adjust interface (8304d9855df0)

## v1.1.0

### Feature

* use holy values (4a127c343877)

## v1.0.4

### Fix

* adjust index after using ptcn (86f9735c5c85)

## v1.0.3

## v1.0.2

### Fix

* skip headline parsing for too few text data (60bf223f801d)

## v1.0.1

### Fix

* fix loader after sections changes (be33d64585ec)

## v1.0.0

### Feature

* add backup strategy to use two lines (df16c59dc878)
* move docref and textflow to texas (bbb0493af349)
* log selected judgement (ce7bf0f273c6)

## v0.28.7

## v0.28.6

### Feature

* use improved quotation parser (51765fb75ace)

### Fix

* skip empty pages (430b048bfcf0)

## v0.28.5

### Feature

* extend list parser (bff89b5d6a6f)
* add another possible dot (7103a3da7ddd)

### Fix

* adjust to new magic API (d1f79a43f9b4)

## v0.28.4

### Feature

* extend possible pattern (b82f4fa53d56)

## v0.28.3

### Feature

* remove duplicated findings (e111403c9800)
* add more pattern (37a4ebf8f305)

## v0.28.2

### Feature

* add more valid bib pattern (818dda1a0113)

## v0.28.1

### Feature

* merge links over more than two lines (4823ff388a2b)

### Fix

* decrease verbosity (4c225e8e77c8)

## v0.28.0

### Feature

* extend debugging information (e0d89930bbf8)
* extend patch pattern (fdce369c8a55)
* add character level pattern (998218d1b0ff)
* add magic strategy to result selection (f29b03332194)
* extend headline level error table (4fef4140bfe5)
* add method to detect too many invalid headline endings (7850d8a2893c)
* add more debugging information (692f04faf4ab)
* add enable magic strategy (042890a2e2e6)
* add magic strategy which use doctextstyle clustering (7306372a25ca)
* add document machine strategy (2527e1740fc6)
* add fonts and magics to headline extractor (7005569f1ba2)
* load headlines from generated content (485419173f5f)
* extend content type detector (8c7a7cef29fe)
* handle undefined sentences (06fdd85ba4ed)
* skip table content (23e204f11917)

### Fix

* handle empty strings correctly (53875c1ff8fc)
* headline is already in content coordinates (1b62215a1e18)
* skip invalid list access (2e853bccb69f)

### Documentation

* extend interface documentation (febbf5a98b8a)

## v0.27.6

### Fix

* skip invalid list as a result of area changing (62734af0131b)

## v0.27.5

### Fix

* fix list lookup (0defc55e02ee)
* improve sentence merger (124abe0532c3)
* merge divis at end of a line (111a5df024a3)
* adjust to new double colon rule (a2078783069c)
* limit max blockquote length (7bb78f112998)

## v0.27.4

## v0.27.2

### Feature

* enable raw bib ref attribute (1b81b1cb8b62)

### Fix

* adjust cluster strategy (0ac1e0dac203)
* fix holy value access (fb81f1d5fd2c)
* increase required logging level (43cd4acabedf)

### Documentation

* move bibliography documentation (f9f2b3824596)

## v0.27.1

### Fix

* handle empty page (e346f622b75a)

## v0.27.0

### Feature

* add method to dump and load wordspace results (3383d2f47e1b)
* skip formula, figure, list and table wordspace check (ebf6a89f0035)
* add basic wordspace step infrastructure (5be0f2eff5a6)

### Fix

* reduce logging verbosity (44dcbc1c65e2)

## v0.26.1

### Feature

* skip cluster which seam no headline (28e28ff2afc6)

### Fix

* allow longer headline (e3fc83bcc1a5)

## v0.26.0

### Feature

* add judge debugging information (a33efcbbcf65)
* disable headline strategy on too many headline hole (f8813ed5a083)
* add another first level chapter pattern (6f16cdf2157b)
* add method to check that token is a headline (b77775ad7d15)
* add method to score invalid headlines (9bab61b1122a)
* add method to travel toc by numbered level (5229db25420c)

## v0.25.2

## v0.25.1

### Documentation

* Happy New Year! (3766210d0b4c)

## v0.25.0

### Feature

* extend level four check (175b0fee0ba0)
* split headline level and title (97b1c9baceb3)
* enable fourth cluster strategy (0ef4389c08cb)
* exclude dotted list as potential headline (7be33e778c40)
* extend best strategy selector (ba442a285dc5)
* add cluster strategy (77a5ce66ad42)
* improve strategy error feedback (1e45f36bb92c)
* ease accessing path module (85e45c62f2e8)

### Fix

* handle empty data correctly (441d5bec5f08)

## v0.24.1

### Feature

* add reference to raw converter (2b365d3f9c8a)

## v0.24.0

### Feature

* extend bib pattern parser (56735079f8ef)
* skip invalid bib references (b8f04fde5068)
* extend plain converter (7030633c7bc6)
* add raw content later (bafa9d8642bd)
* add tech parser facade (f32b065ff828)
* extend bibliography pattern parser (80898b548ea1)
* add sentence lookup (a3754bc8f709)

## v0.23.0

### Feature

* add first approach of bibref parser (24af8961f3e6)

## v0.22.1

## v0.22.0

### Feature

* add table reference extractor (2c4546780479)
* extend figure pattern (abacdffe1d4a)
* extend parser pattern (b2b7d2157206)
* add section label parser (9c60190f776d)
* extend figure extraction step (20a0166daaf2)
* add flag to enumerate sentence number (a97a81fcc103)
* add figure reference extractor (31792860fa0e)
* add basic docref cli structure (2bda35db86ec)

### Fix

* improve code style (aa1ef163a3ad)

## v0.21.0

### Feature

* extend links parser (81854829c2fa)
* add more accepted chars to link parser (5ebada6e4581)
* add option to collect starting position of parsed pattern (70ee204edd2a)
* add step to parse hyperlinks (942fba939f0e)

## v0.20.3

## v0.20.1

### Fix

* fix empty valid area check (28c93cf5a026)

## v0.20.0

### Feature

* remove headline content to improve vertical list parser (fe34237e1369)
* adjust holy value of vertical parser (8cf144ecd1d5)
* improve vertical parser (bd8632540b07)
* improve list regex parser (c4a8fcefec0f)
* exclude more invalid list data (81abaf4589eb)

### Fix

* single area is always valid (8261d66749fb)
* add missing area splitter (930dc88214b2)

## v0.19.1

### Feature

* use magic data to improve list extractor (021aff27e0f4)
* use improve list strategy selector (50e208749560)
* add zip_optimizer form utila code (5e5d63996565)

### Fix

* ensure to handle chunk sized mode correctly (a6453f63136e)

## v0.19.0

### Feature

* change to local area index for multiple lists (cb61991359b0)
* extend score lists to support extended lists (ec2861922cdd)
* patch list serializer to supported extended lists over pages (2e5fe627c4dd)
* use oneline data to improve extraction results (9fcaf96c2d4f)
* add magic data as optional data source (f38159cab5f6)
* add path checking routine (25e8c6aa9fcf)
* add decoration for multi line extraction (1150f90a8c4a)
* specify multiline headline parser (26e754ffc842)
* add look back for chapter-X-pattern to multiline (3ad005a7088e)
* extend black list pattern (be1959a9d883)
* extend headline exclude strategy (c815ccd8c125)
* add Kapitel-X-Pattern to standard headline extractor (114bfefadba1)

## v0.18.0

### Feature

* skip extraction result with too many level one headlines (a698117bafb4)
* use improve headline extractor strategies (81748199788b)
* add separate headline filter (37e3ce586f92)
* introduce separate page extraction possibility (f7428bca9be9)
* add new headline extraction mechanism (25825af180ed)
* add decoration parser to detect `Kapitel 1` pattern (c9946aef3550)
* disable levelfour parser if regularly levelfour was parsed (b829228c0597)
* deactivate distance check for level 3 and more headlines (dd5686129c2c)
* use distance before to improve distance check (dbeaf01ff925)
* use logical indexing (711fb7d950ef)
* add decoration field to handle `Kapitel 1 Headlines` (bdcdb74d64f1)

### Fix

* use improved headline level parser (67e81fa245c4)
* fix extract area of parsed list (ff081d8fd449)

### Documentation

* extend interface documentation (1ca1f9aff9ad)

## v0.17.2

## v0.17.0

### Feature

* skip small text for level4 computation (15a107d55596)

### Fix

* patch most common font family determination (18fdd7295714)

## v0.16.4

### Fix

* remove level from title in standard headline extractor (7ba27b02bfcb)
* level four validator (552b1160b8f9)
* do not change default level type (a325f6e1ff0c)

## v0.16.3

### Feature

*  use new title/raw field (66a0cad9a581)

### Fix

* patching headlines dumper to store raw data (1bae3fb5ecac)

## v0.16.2

### Fix

* add missing page attribute (0151fc591d5b)

## v0.16.1

### Documentation

* adjust outdated documentation (64850d30d141)

## v0.16.0

### Feature

* merge group horizontal to fix layout extraction bugs (7a9c97607cb8)
* add patch to alter MultilineGroup behavior (c462e5a37b65)
* ignore false positive headlines with short content (191340ef70a4)
* ignore no headlines which start on right side (ff3ba6c62c6f)

## v0.15.3

## v0.15.2

### Fix

* fix bug of merging on empty page start (83b2ec7a6e1a)

## v0.15.1

### Feature

* disable headlines which hugely differ from level 1-3 (0d7c5911c3da)
* extend path location (60458574f475)

## v0.15.0

### Feature

* extract headlines based on oneline layout data (4212c6976ce6)
* make multiline headline parser more robust (c54a998cb12b)
* disable headline level for useless input (7fa3dc87d616)
* add guard to disable feature (5ff31f61b5ef)
* merge level four headlines to normal extraction (f037e70af74e)
* add first draft of level 4 headline parser (d663dfd3ac00)

### Fix

* adjust headlines section range (921e23051caa)
* adjust headline validation test (756be01b41fd)
* determine `level + text` correctly (746fd30ce9f4)

## v0.14.0

### Feature

* improve headline parser quality (b1c2cceb4898)
* extend dotted list parser pattern (29131b0bf20b)
* add alignment to describe block end (a1314bb6656d)

### Fix

* do not parse newline as list content (ebc116102e8c)
* fix alignment loader (7efd5be62d25)

## v0.13.6

## v0.13.3

### Feature

* ensure that only proper lists are accepted to dump (ec3466e9ba2d)

### Fix

* fix merging list (126107ad0088)

## v0.13.2

### Fix

* add support for non decimal page numbers (999c6ed95f13)
* handle range determination for multiple page section (d465bf0a159b)

### Documentation

* remove duplicated backlog (2bb22cc38c0b)

## v0.13.1

### Fix

* fix headline parser after upgrading requirements (b4d161f71b2f)

## v0.13.0

### Feature

* determine headline level out of geometry (9ab4e33e7a9a)
* add multi dimension near checker (f5f831808278)

### Documentation

* extend interface documentation (230110119d30)

## v0.12.1

### Fix

* decide to handle expanded list items in sentence analysis (2e341bc4a29b)
* ensure that fix is executed (fabfcc86faa4)

## v0.12.0

### Feature

* extend NoLevel headline white list (a346e48b69bd)
* enable best global selecting strategy (8c88f5c852a1)
* add step to adjust extracted PageList page number (0eb3d853d344)
* add first approach of multiple pages strategy (6c9637bf0deb)
* use count covered space to detect best list extraction (e48f1745881f)
* add method to merge content to one long content page (0af1c3229b63)
* add new multiple pages strategy (c52e252d9c75)

### Fix

* fix content border selection (87399a7db239)
* handle headlines of appendix separately (1f8dcc2e8d6e)

### Documentation

* extend module documentation (442e3da42c32)

## v0.11.0

### Feature

* add support for Chapter starts on MultiplePages (feed0cd2b208)
* introduce new judgement strategy to pass master98 example (6574d1ea5108)

### Fix

* adjust unit test to pass current quotation parser (daaa78c0e847)
* adjust page sentence merger (a478339af1f5)
* fix alignment parser test (41e7ead6ec7c)
* fix broken regex list parser (f5c35181f2c0)
* introduce min block center width (e723c971eac2)
* fix expected result due new specification (ed2e4929140f)
* use more stable line based alignment approach (20b6c73e7235)
* adjust relative text feed computation (54cbef1e1892)
* solve duplicated font distance error test (0c987f9580f8)

## v0.10.0

### Feature

* add right aligned blockquote parser (65ba8959c15f)
* add blockquote detector (64c9f7662cd2)

### Fix

* increase required debug level (6de4d37d73e9)
* adjust unit test with sentence/chapter with list example (18ad2b362c11)
* fix list extractor (917981e3daa9)

## v0.9.9

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

## v0.5.6

### Fix

* convert level when having None entry (ae667b556ab6)

## v0.5.5

### Fix

* adjust toc extractor range (c70ac159ca34)

## v0.5.3

### Fix

* do not overwrite detected level (9ff7f0be723a)

## v0.5.0

### Fix

* fix headline level detector (cefe9684948e)
* fix expected subjects (6d207b3306c0)
* ignore sentence which are parsed as headlines (12eafcaac6fb)
* add check to exclude miss parsed footnotes as headline (bd21836e6467)

## v0.4.8

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

## v0.1.3

### Fix

* remove disabled yaml formatter (2dea308f98d6)

## v0.1.0

### Feature

* move code from hey project (764d94914356)

### Fix

* generate required test data (6fdba6c77c23)

## v0.0.0 Initial release
