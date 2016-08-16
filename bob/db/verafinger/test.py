#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""A few checks at the VERA database.
"""

import os

from . import Database

import nose.tools
from nose.plugins.skip import SkipTest

# base directories where the VERA files sit
DATABASE_PATH = "/idiap/project/vera/databases/VERA-fingervein"
ANNOTATIONS_PATH = "/idiap/group/biometric/annotations/vera/Fingervein"


def sql3_available(test):
  """Decorator for detecting if the sql3 file is available"""

  from bob.io.base.test_utils import datafile
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    dbfile = datafile("db.sql3", __name__, None)
    if os.path.exists(dbfile):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The interface SQL file (%s) is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (dbfile, 'vera'))

  return wrapper


def db_available(test):
  """Decorator for detecting if the database files are available"""

  from bob.io.base.test_utils import datafile
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    if os.path.exists(DATABASE_PATH) and os.path.exists(ANNOTATIONS_PATH):
      return test(*args, **kwargs)
    else:
      raise SkipTest("Either the database path (%s), the annotations path (%s) or both are not available" % (DATABASE_PATH, ANNOTATIONS_PATH))

  return wrapper


@sql3_available
def test_clients():

  # test whether the correct number of clients is returned
  db = Database()

  nose.tools.eq_(len(db.groups()), 2)
  nose.tools.eq_(len(db.protocols()), 7)
  nose.tools.eq_(len(db.protocol_names()), 7)
  nose.tools.eq_(len(db.purposes()), 3)

  nose.tools.eq_(len(db.clients()), 220)
  nose.tools.eq_(len(db.clients(protocol='1vsAll')), 220)
  nose.tools.eq_(len(db.clients(protocol='B')), 108)
  nose.tools.eq_(len(db.clients(protocol='NOM50')), 100)
  nose.tools.eq_(len(db.clients(protocol='NOM')), 220)
  nose.tools.eq_(len(db.clients(protocol='SpoofingAttack50')), 100)
  nose.tools.eq_(len(db.clients(protocol='SpoofingAttack')), 220)
  nose.tools.eq_(len(db.clients(protocol='SpoofingEnrolAttack')), 220)


  nose.tools.eq_(len(db.client_ids()), 220)
  nose.tools.eq_(len(db.client_ids(protocol='1vsAll')), 220)
  nose.tools.eq_(len(db.client_ids(protocol='B')), 108)
  nose.tools.eq_(len(db.client_ids(protocol='NOM50')), 100)
  nose.tools.eq_(len(db.client_ids(protocol='NOM')), 220)
  nose.tools.eq_(len(db.client_ids(protocol='SpoofingAttack50')), 100)
  nose.tools.eq_(len(db.client_ids(protocol='SpoofingAttack')), 220)
  nose.tools.eq_(len(db.client_ids(protocol='SpoofingEnrolAttack')), 220)

  nose.tools.eq_(len(db.models()), 660)
  nose.tools.eq_(len(db.models(protocol='1vsAll')), 440)
  nose.tools.eq_(len(db.models(protocol='B')), 216)
  nose.tools.eq_(len(db.models(protocol='NOM50')), 100)
  nose.tools.eq_(len(db.models(protocol='NOM')), 220)
  nose.tools.eq_(len(db.models(protocol='SpoofingAttack50')), 100)
  nose.tools.eq_(len(db.models(protocol='SpoofingAttack')), 220)
  nose.tools.eq_(len(db.models(protocol='SpoofingEnrolAttack')), 220)

  nose.tools.eq_(len(db.model_ids()), 660)
  nose.tools.eq_(len(db.model_ids(protocol='1vsAll')), 440)
  nose.tools.eq_(len(db.model_ids(protocol='B')), 216)
  nose.tools.eq_(len(db.model_ids(protocol='NOM50')), 100)
  nose.tools.eq_(len(db.model_ids(protocol='NOM')), 220)
  nose.tools.eq_(len(db.model_ids(protocol='SpoofingAttack50')), 100)
  nose.tools.eq_(len(db.model_ids(protocol='SpoofingAttack')), 220)
  nose.tools.eq_(len(db.model_ids(protocol='SpoofingEnrolAttack')), 220)



@sql3_available
def test_objects():

  # tests if the right number of File objects is returned
  db = Database()

  #nose.tools.eq_(len(db.objects()), 452)
  #nose.tools.eq_(len(db.objects(groups='world')), 0)
  #nose.tools.eq_(len(db.objects(groups='dev')), 452)

  nose.tools.eq_(len(db.objects(protocol='1vsAll')), 440)
  nose.tools.eq_(len(db.objects(protocol='1vsAll', groups='world')), 0)
  nose.tools.eq_(len(db.objects(protocol='1vsAll', groups='dev')), 440)

  nose.tools.eq_(len(db.objects(protocol='B')), 216)
  nose.tools.eq_(len(db.objects(protocol='B', groups='world')), 0)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev')), 216)

  nose.tools.eq_(len(db.objects(protocol='NOM')), 440)
  nose.tools.eq_(len(db.objects(protocol='NOM', groups='world')), 0)
  nose.tools.eq_(len(db.objects(protocol='NOM', groups='dev')), 440)

  nose.tools.eq_(len(db.objects(protocol='NOM50')), 200)
  nose.tools.eq_(len(db.objects(protocol='NOM50', groups='world')), 0)
  nose.tools.eq_(len(db.objects(protocol='NOM50', groups='dev')), 200)

  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack50')), 200)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack50', groups='world')), 0)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack50', groups='dev')), 200)

  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack')), 440)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack', groups='world')), 0)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack', groups='dev')), 440)

  nose.tools.eq_(len(db.objects(protocol='SpoofingEnrolAttack')), 440)
  nose.tools.eq_(len(db.objects(protocol='SpoofingEnrolAttack', groups='world')), 0)
  nose.tools.eq_(len(db.objects(protocol='SpoofingEnrolAttack', groups='dev')), 440)

  nose.tools.eq_(len(db.objects(protocol='1vsAll', groups='dev', model_ids=('101_left_1_real',))), 440)
  nose.tools.eq_(len(db.objects(protocol='1vsAll', groups='dev', model_ids=('101_left_1_real',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='1vsAll', groups='dev', model_ids=('101_left_1_real',), purposes='probe')), 439)
  nose.tools.eq_(len(db.objects(protocol='1vsAll', groups='dev', model_ids=('101_left_1_real',), purposes='probe', classes='client')), 1)
  nose.tools.eq_(len(db.objects(protocol='1vsAll', groups='dev', model_ids=('101_left_1_real',), purposes='probe', classes='impostor')), 438)

  nose.tools.eq_(len(db.objects(protocol='B', groups='dev', model_ids=('10_left_1_real',))), 216)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev', model_ids=('10_left_1_real',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev', model_ids=('10_left_1_real',), purposes='probe')), 215)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='client')), 1)
  nose.tools.eq_(len(db.objects(protocol='B', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='impostor')), 214)

  nose.tools.eq_(len(db.objects(protocol='NOM50', groups='dev', model_ids=('10_left_1_real',))), 101)
  nose.tools.eq_(len(db.objects(protocol='NOM50', groups='dev', model_ids=('10_left_1_real',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='NOM50', groups='dev', model_ids=('10_left_1_real',), purposes='probe')), 100)
  nose.tools.eq_(len(db.objects(protocol='NOM50', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='client')), 1)
  nose.tools.eq_(len(db.objects(protocol='NOM50', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='impostor')), 99)

  nose.tools.eq_(len(db.objects(protocol='NOM', groups='dev', model_ids=('10_left_1_real',))), 221)
  nose.tools.eq_(len(db.objects(protocol='NOM', groups='dev', model_ids=('10_left_1_real',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='NOM', groups='dev', model_ids=('10_left_1_real',), purposes='probe')), 220)
  nose.tools.eq_(len(db.objects(protocol='NOM', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='client')), 1)
  nose.tools.eq_(len(db.objects(protocol='NOM', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='impostor')), 219)

  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack50', groups='dev', model_ids=('10_left_1_real',))), 101)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack50', groups='dev', model_ids=('10_left_1_real',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack50', groups='dev', model_ids=('10_left_1_real',), purposes='probe')), 100)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack50', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='client')), 1)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack50', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='impostor')), 99)

  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack', groups='dev', model_ids=('10_left_1_real',))), 221)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack', groups='dev', model_ids=('10_left_1_real',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack', groups='dev', model_ids=('10_left_1_real',), purposes='probe')), 220)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='client')), 1)
  nose.tools.eq_(len(db.objects(protocol='SpoofingAttack', groups='dev', model_ids=('10_left_1_real',), purposes='probe', classes='impostor')), 219)

  nose.tools.eq_(len(db.objects(protocol='SpoofingEnrolAttack', groups='dev', model_ids=('10_left_1_attack',))), 221)
  nose.tools.eq_(len(db.objects(protocol='SpoofingEnrolAttack', groups='dev', model_ids=('10_left_1_attack',), purposes='enroll')), 1)
  nose.tools.eq_(len(db.objects(protocol='SpoofingEnrolAttack', groups='dev', model_ids=('10_left_1_attack',), purposes='probe')), 220)
  nose.tools.eq_(len(db.objects(protocol='SpoofingEnrolAttack', groups='dev', model_ids=('10_left_1_attack',), purposes='probe', classes='client')), 1)
  nose.tools.eq_(len(db.objects(protocol='SpoofingEnrolAttack', groups='dev', model_ids=('10_left_1_attack',), purposes='probe', classes='impostor')), 219)


@sql3_available
def test_driver_api():

  from bob.db.base.script.dbmanage import main

  nose.tools.eq_(main('vera dumplist --self-test'.split()), 0)
  nose.tools.eq_(main('vera dumplist --protocol=1vsAll --class=client --group=dev --purpose=enroll --model=101_left_1_real --self-test'.split()), 0)
  nose.tools.eq_(main('vera checkfiles --self-test'.split()), 0)
  nose.tools.eq_(main('vera reverse Fingervein/001-M/001_L_1 --self-test'.split()), 0)
  nose.tools.eq_(main('vera path 37 --self-test'.split()), 0)


@sql3_available
@db_available
def test_load():

  db = Database()

  for f in db.objects():

    # loads an image from the database
    image = f.load(DATABASE_PATH)
    assert isinstance(image, numpy.ndarray)
    nose.tools.eq_(len(image.shape), 2) #it is a 2D array
    nose.tools.eq_(image.dtype, numpy.uint8)


@sql3_available
@db_available
def test_annotations():

  db = Database()

  for f in db.objects():

    # loads an image from the database
    image = f.load(DATABASE_PATH)

    annotations = f.annotations(ANNOTATIONS_PATH)
    assert isinstance(annotations, numpy.ndarray)
    nose.tools.eq_(len(annotations.shape), 2) #it is a 2D array
    nose.tools.eq_(annotations.shape[1], 2) #two columns
    nose.tools.eq_(annotations.dtype, numpy.uint8)
    assert len(annotations) > 10 #at least 10 points

    # ensures all annotation points are within image boundary
    Y,X = image.shape
    for y,x in annotations:
      assert y < Y
      assert x < X
