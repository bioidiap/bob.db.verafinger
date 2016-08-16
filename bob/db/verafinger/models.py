#!/usr/bin/env python
# vim: set fileencoding=utf-8 :


"""Table models and functionality for the VERA database.
"""

import os

import bob.io.base
import bob.io.image
import bob.db.base

import numpy

from sqlalchemy import Table, Column, Integer, String, ForeignKey, or_, and_, not_
from bob.db.base.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


protocolPurpose_file_association = Table('protocolPurpose_file_association', Base.metadata,
  Column('protocolPurpose_id', Integer, ForeignKey('protocolPurpose.id')),
  Column('file_id', Integer, ForeignKey('file.id')))

protocol_model_association = Table('protocol_model_association', Base.metadata,
  Column('protocol_id', Integer, ForeignKey('protocol.id')),
  Column('model_id', Integer, ForeignKey('model.id')))


class Client(Base):
  """Unique clients in the database, referred by a single integer"""

  __tablename__ = 'client'

  id = Column(Integer, primary_key=True)

  gender_choices = ('M', 'F')
  gender = Column(Enum(*gender_choices))

  age = Column(Integer)


  def gender_display(self):
    """Returns a representation of the client gender"""

    return 'male' if self.gender == 'M' else 'female'


  def __repr__(self):
    return "Client(%d) <%s>, %d years old" % \
        (self.id, self.gender_display, self.age)


class Finger(Base):
  """Unique fingers in the database, referred by a string

  Fingers have the format ``003_L`` (i.e. <client>_<finger>)
  """

  __tablename__ = 'finger'

  # Key identifier for the finger
  id = Column(String(5), primary_key=True)

  # Key identifier of the client associated with this finger
  client_id = Column(Integer, ForeignKey('client.id'))
  client = relationship("Client", backref=backref("fingers", order_by=id))

  def __init__(self, id, client):
    self.id = id
    self.client = client

  def __repr__(self):
    return "Client(%s)" % (self.id,)


class Model(Base):
  """This class defines possible enrollment models"""

  __tablename__ = 'model'

  # Key identifier for the client
  id = Column(Integer, primary_key=True)

  # Name of the protocol associated with this object
  name = Column(String(20))

  # Key identifier of the client associated with this model
  client_id = Column(String(20), ForeignKey('client.id')) # for SQL
  client = relationship("Client", backref=backref("models", order_by=id))

  # Key identifier of the enrollment associated with this model
  file_id = Column(Integer, ForeignKey('file.id')) # for SQL
  file = relationship("File", backref=backref("models", order_by=id))

  def __init__(self, name, client_id, file_id):
    self.name = name
    self.client_id = client_id
    self.file_id = file_id

  def __repr__(self):
    return "Model(%s)" % (self.name)


class File(bob.db.base.File):

  __tablename__ = 'file'

  # Key identifier for the file
  id = Column(Integer, primary_key=True)

  # Key identifier of the client associated with this file
  client_id = Column(String(20), ForeignKey('client.id')) # for SQL
  client = relationship("Client", backref=backref("files", order_by=id))

  # Unique path to this file inside the database
  path = Column(String(100), unique=True)

  # Identifier of the finger id associated with this file
  finger_choices = ('L', 'R')
  finger = Column(Enum(*finger_choices))

  # Identifier of the session
  session_choices = (1, 2)
  session = Column(Enum(*session_choices))


  def __init__(self, client, path, sgroup, finger_id,  session_id, stype):
    # call base class constructor
    self.sgroup = sgroup
    self.finger_id = finger_id
    self.session_id = session_id
    self.stype = stype


  def load(self, directory=None, extension='.png'):
    """Loads the image for this file entry


    Parameters:

      directory (str): The path to the root of the database installation.  This
        is the path leading to files named ``DDD-G`` where ``D``'s correspond
        to digits and ``G`` to the client gender. For example ``032-M``.


    Returns:

      numpy.ndarray: A 2D array of unsigned integers corresponding to the input
       image for this file in (y,x) notation (Bob-style).

    """

    return bob.io.base.load(self.make_path(directory, '.png'))


  def annotations(self, directory):
    """Loads annotations taking into consideration a base annotation folder

    The returned points (see return value below) correspond to a polygon in the
    2D space delimiting the finger. It is up to you to generate a mask out of
    these annotations.


    Parameters:

      directory (str): The path to the root of the annotation installation.
        This is the path leading to files named ``DDD-G`` where ``D``'s
        correspond to digits and ``G`` to the client gender. For example
        ``032-M``.


    Returns:

      numpy.ndarray: A 2D array of 8-bit unsigned integers corresponding to
        annotations for the given fingervein image. Points are loaded in (y,x)
        format so, the first column of the returned array correspond to the
        y-values while the second column to the x-values of each coordinate.

    """

    return numpy.loadtxt(self.make_path(directory, '.txt'), dtype='uint8')


class Protocol(Base):
  """VERA protocols"""

  __tablename__ = 'protocol'

  # Unique identifier for this protocol object
  id = Column(Integer, primary_key=True)
  # Name of the protocol associated with this object
  name = Column(String(20), unique=True)

  # For Python: A direct link to the Model objects associated with this Protcol
  models = relationship("Model", secondary=protocol_model_association, backref=backref("protocols", order_by=id))

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return "Protocol('%s')" % (self.name,)


class ProtocolPurpose(Base):
  """VERA protocol purposes"""

  __tablename__ = 'protocolPurpose'

  # Unique identifier for this protocol purpose object
  id = Column(Integer, primary_key=True)
  # Id of the protocol associated with this protocol purpose object
  protocol_id = Column(Integer, ForeignKey('protocol.id')) # for SQL
  # Group associated with this protocol purpose object
  group_choices = ('world', 'dev')
  sgroup = Column(Enum(*group_choices))
  # Purpose associated with this protocol purpose object
  purpose_choices = ('train', 'enroll', 'probe')
  purpose = Column(Enum(*purpose_choices))

  # For Python: A direct link to the Protocol object that this ProtocolPurpose belongs to
  protocol = relationship("Protocol", backref=backref("purposes", order_by=id))
  # For Python: A direct link to the File objects associated with this ProtcolPurpose
  files = relationship("File", secondary=protocolPurpose_file_association, backref=backref("protocolPurposes", order_by=id))

  def __init__(self, protocol_id, sgroup, purpose):
    self.protocol_id = protocol_id
    self.sgroup = sgroup
    self.purpose = purpose

  def __repr__(self):
    return "ProtocolPurpose('%s', '%s', '%s')" % (self.protocol.name, self.sgroup, self.purpose)

