.. _backlog:

backlog
=======

* add `spaces` and `spaces_expected` step to determine space between words
  using textflow. With this information, we can give advices in tuning
  text look and feel.

* Furthermore we can give advices to add work-?divisors?.

* SpecialWordChecker: Search for highlighted, upper case words and check
  if there use correctly in further Documents. This requires a Blacklist
  for words like SPIEGEL, WELT etc. Example: VeLoDyn

* Text Density checker. Check paragraph, chapter length

* detect text alignment and display correctly

* detect_decider mark abweichungen

* Block-Zitate benötigen keine Anführungszeichen

* docref: add math ref parser, siehe Formel

BEFORE RELEASE
--------------

* remove:

    loaded = utila.yaml_from_raw_or_path(raw, safe=False)
