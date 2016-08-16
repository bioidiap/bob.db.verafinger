#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

"""This script creates the VERA database in a single pass.
"""

import os

from .models import *

def nodot(item):
  """Can be used to ignore hidden files, starting with the . character."""
  return item[0] != '.'


def add_files(session, imagedir, verbose):
  """Add files (and clients) to the VERA database."""


  def add_file(subdir, filename, model_dict, file_dict):
    """Parses a single filename and add it to the list.

    Also adds a client entry if not already in the database.
    """

    subclient_id, side, session_id = \
        os.path.splitext(os.path.basename(filename))[0].split('_')

    subclient_id = int(subclient_id)
    side = 'left' if side == 'L' else 'right'
    session_id = int(session_id)

    # each finger is considered as a separate client
    client_id = "%d_%s" % (subclient_id, side)

    if not (client_id in client_dict):
      c = Client(client_id, subclient_id)
      session.add(c)
      session.flush()
      session.refresh(c)
      client_dict[client_id] = True

    session_id = int(v[2])
    base_path = os.path.join(typedir, subdir,
        os.path.basename(filename).split('.')[0])
    sgroup = 'dev'

    if verbose > 1:
      print("  Adding file '%s'..." %(base_path, ))

    cfile = File(client_id, base_path, sgroup, finger_id, session_id)
    session.add(cfile)
    session.flush()
    session.refresh(cfile)
    file_dict[sgroup][cfile.id] = cfile

    if sgroup == 'dev':
      model_id = "%d_%s_%d" % (subclient_id, finger_id, session_id)

      if verbose > 1:
        print("  Adding Model '%s'..." %(model_id, ))

      model = Model(model_id, client_id, cfile.id)
      session.add(model)
      session.flush()
      session.refresh(model)
      model_dict[model_id] = model

    return [client_dict, model_dict, file_dict]


  if verbose:
    print("Adding files...")

  client_dict = {}
  model_dict = {}
  file_dict = {}
  file_dict['world'] = {}
  file_dict['dev'] = {}

  if not os.path.isdir(os.path.join(imagedir,typedir)):
    raise RuntimeError("Cannot find directory '%s'" % \
        os.path.join(imagedir,typedir))

  subdir_list = [l for l in list(filter(nodot, os.listdir(os.path.join(imagedir,typedir)))) if os.path.isdir(os.path.join(imagedir,typedir,l))]

  for subdir in subdir_list:
    file_list = list(filter(nodot, os.listdir(os.path.join(imagedir, typedir, subdir))))

    for filename in file_list:
      filename_, extension = os.path.splitext(filename)
      if extension == '.png':
        client_dict, model_dict, file_dict = add_file(session, typedir,
            subdir, os.path.join(imagedir, filename), client_dict,
            model_dict, file_dict, verbose)

  return [client_dict, model_dict, file_dict]


def add_protocols(session, client_dict, model_dict, file_dict, verbose):
  """Adds protocols"""

  # 2. ADDITIONS TO THE SQL DATABASE
  client_full_ids = client_dict.keys()
  client_ids = sorted(set([int(c.split('_')[0]) for c in client_full_ids]))[:50]
  client_100_ids = [c for c in client_full_ids if int(c.split('_')[0]) in client_ids]

  client_B_ids =[]
  i = 1
  ni = 0

  while ni < 60:
    fingers = None

    if ni < 48: fingers = ['left', 'right']
    elif ni < 54: fingers = ['left']
    else: fingers = ['right']

    found = False
    for f in fingers:
      client_id = "%d_%s" % (i, f)
      if client_id in client_full_ids:
        client_B_ids.append(client_id)
        found = True
    if found: ni += 1
    i += 1

  protocol_list = ['1vsAll', 'B', 'NOM50','NOM'] + protocol_list_spoof
  protocolPurpose_list = [('world', 'train'), ('dev', 'enroll'), ('dev', 'probe')]

  for proto in protocol_list:

    p = Protocol(proto)
    # Add protocol
    if verbose:
      print("Adding protocol %s..." % (proto))

    session.add(p)
    session.flush()
    session.refresh(p)

    for purpose in protocolPurpose_list:
      pu = ProtocolPurpose(p.id, purpose[0], purpose[1])

      if verbose > 1:
        print(" Adding protocol purpose ('%s', '%s','%s')..." % (p.name,
          purpose[0], purpose[1]))

      session.add(pu)
      session.flush()
      session.refresh(pu)

      cfile_dict = file_dict[purpose[0]]

      #if proto in protocol_list_spoof: continue
      for f_id, f_file in cfile_dict.iteritems():

        if verbose > 1:
          print("   Adding file ('%s') to protocol purpose ('%s', '%s','%s')..." % (f_file.path, p.name, purpose[0], purpose[1]))

        if proto == '1vsAll' and f_file.stype == 'real':
          pu.files.append(f_file)

        elif proto == 'B' and f_file.stype == 'real':
          if f_file.client_id in client_B_ids and f_file.stype == 'real':
            pu.files.append(f_file)

        elif proto == 'NOM' and f_file.stype == 'real':
          if ((f_file.session_id == 1 and purpose[1] == 'enroll') or (f_file.session_id == 2 and purpose[1] == 'probe')) \
        and f_file.stype == 'real':
            pu.files.append(f_file)

        elif proto == 'NOM50' and f_file.stype == 'real':
          if ((f_file.session_id == 1 and purpose[1] == 'enroll') or (f_file.session_id == 2 and purpose[1] == 'probe')) \
        and f_file.client_id in client_100_ids and f_file.stype == 'real':
            pu.files.append(f_file)

    #if proto in protocol_list_spoof: continue
    for m_id, model in model_dict.iteritems():

        if proto == '1vsAll' and model.file.stype == 'real':
          p.models.append(model)
        elif proto == 'B':
          if model.client_id in client_B_ids and model.file.stype == 'real':
            p.models.append(model)
        elif proto == 'NOM':
          if model.file.session_id == 1 and model.file.stype == 'real':
            p.models.append(model)
        elif proto == 'NOM50':
          if model.file.session_id == 1 and model.client_id in client_100_ids and model.file.stype == 'real':
            p.models.append(model)


def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0],
      echo=(args.verbose > 2))
  Base.metadata.create_all(engine)


def create(args):
  """Creates or re-creates this database"""

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  client_dict, model_dict, file_dict = add_files(s, args.imagedir, args.verbose)
  add_protocols(s, client_dict, model_dict, file_dict, args.verbose)
  s.commit()
  s.close()


def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help="If set, I'll first erase the current database")
  parser.add_argument('-v', '--verbose', action='count', help='Do SQL operations in a verbose way')
  parser.add_argument('-D', '--imagedir', metavar='DIR', default='/idiap/project/vera/', help="Change the relative path to the directory containing the images of the VERA database (defaults to %(default)s)")

  parser.set_defaults(func=create) #action
