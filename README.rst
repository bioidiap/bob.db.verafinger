.. vim: set fileencoding=utf-8 :
.. Tue 02 Aug 2016 15:43:29 CEST

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.verafinger/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.db.verafinger/master/index.html
.. image:: https://travis-ci.org/bioidiap/bob.db.verafinger.svg?branch=master
   :target: https://travis-ci.org/bioidiap/bob.db.verafinger
.. image:: https://coveralls.io/repos/bioidiap/bob.db.verafinger/badge.png
   :target: https://coveralls.io/r/bioidiap/bob.db.verafinger
.. image:: https://img.shields.io/badge/github-master-0000c0.png
   :target: https://github.com/bioidiap/bob.db.verafinger/tree/master
.. image:: http://img.shields.io/pypi/v/bob.db.verafinger.png
   :target: https://pypi.python.org/pypi/bob.db.verafinger
.. image:: http://img.shields.io/pypi/dm/bob.db.verafinger.png
   :target: https://pypi.python.org/pypi/bob.db.verafinger
.. image:: https://img.shields.io/badge/real-data--files-a000a0.png
   :target: https://www.idiap.ch/dataset/vera-fingervein
.. image:: https://img.shields.io/badge/spoofing-data--files-a000a0.png
   :target: https://www.idiap.ch/dataset/vera-spoofingfingervein

============================================
 VERA Fingervein Database Interface for Bob
============================================

This package contains an interface for the evaluation protocols of the `VERA
Fingervein Database`_. Notice this package does not contain the raw data files
from this dataset, which need to be obtained through the link above.


About
-----

This package is currently developed at the `Biometrics group`_ at the `Idiap
Research Institute`_.


Installation
------------

This package only contains database access functions so it is easy to
programatically reproduce evaluation results obtained in papers. You normally
don't install this package, unless you're modifying it. Instead, install one of
our top-level frameworks for vein image processing, such as ``bob.bio.vein``.


.. Write your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _vera fingervein database: https://www.idiap.ch/dataset/vera-fingervein
.. _biometrics group: http://www.idiap.ch/scientific-research/research-groups/biometric-person-recognition
.. _idiap research institute: http://www.idiap.ch
