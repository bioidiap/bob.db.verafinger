.. vim: set fileencoding=utf-8 :
.. Tue 16 Aug 17:34:26 CEST 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.svg
   :target: http://pythonhosted.org/bob.db.verafinger/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.svg
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.db.verafinger/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.verafinger/badges/master/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.verafinger/commits/master
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.verafinger
.. image:: http://img.shields.io/pypi/v/bob.db.verafinger.svg
   :target: https://pypi.python.org/pypi/bob.db.verafinger
.. image:: http://img.shields.io/pypi/dm/bob.db.verafinger.svg
   :target: https://pypi.python.org/pypi/bob.db.verafinger


============================================
 VERA Fingervein Database Interface for Bob
============================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It contains an interface for the evaluation protocols of the `VERA
Fingervein Database`_. Notice this package does not contain the raw data files
from this dataset, which need to be obtained through the link above.


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
.. _vera fingervein database: https://www.idiap.ch/dataset/vera-fingervein
