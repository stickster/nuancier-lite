# -*- coding: utf-8 -*-
#
# Copyright © 2013  Red Hat, Inc.
#
# This copyrighted material is made available to anyone wishing to use,
# modify, copy, or redistribute it subject to the terms and conditions
# of the GNU General Public License v.2, or (at your option) any later
# version.  This program is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.  You
# should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# Any Red Hat trademarks that are incorporated in the source
# code or documentation are not subject to the GNU General Public
# License and may only be used or replicated with the express permission
# of Red Hat, Inc.
#

'''
nuancier-lite tests.
'''

__requires__ = ['SQLAlchemy >= 0.7']
import pkg_resources

import unittest
import shutil
import sys
import os

from datetime import datetime
from datetime import date
from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

sys.path.insert(0, os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..'))

from nuancier.lib import model

DB_PATH = 'sqlite:///:memory:'
PICTURE_FOLDER = os.path.join(os.path.dirname(__file__), 'pictures')
CACHE_FOLDER = os.path.join(os.path.dirname(__file__), 'cache')
TODAY = datetime.utcnow().date()


class Modeltests(unittest.TestCase):
    """ Model tests. """

    def __init__(self, method_name='runTest'):
        """ Constructor. """
        unittest.TestCase.__init__(self, method_name)
        self.session = None

    # pylint: disable=C0103
    def setUp(self):
        """ Set up the environnment, ran before every tests. """
        self.session = model.create_tables(DB_PATH, debug=False)

    # pylint: disable=C0103
    def tearDown(self):
        """ Remove the test.db database if there is one. """
        if os.path.exists(DB_PATH):
            os.unlink(DB_PATH)
        if os.path.exists(CACHE_FOLDER):
            if os.path.isdir(CACHE_FOLDER):
                shutil.rmtree(CACHE_FOLDER)
            elif os.path.isfile(CACHE_FOLDER):
                os.unlink(CACHE_FOLDER)
            else:
                print >> sys.stderr, \
                    'Check %s, it cannot be removed' % CACHE_FOLDER
        

        self.session.rollback()

        ## Empty the database if it's not a sqlite
        if self.session.bind.driver != 'pysqlite':
            self.session.execute('DROP TABLE "Votes" CASCADE;')
            self.session.execute('DROP TABLE "Candidates" CASCADE;')
            self.session.execute('DROP TABLE "Elections" CASCADE;')
            self.session.commit()


def create_elections(session):
    """ Create some basic elections for testing. """
    election = model.Elections(
        election_name='Wallpaper F19',
        election_folder='F19',
        election_year='2013',
        election_n_choice=16,
        election_date_start = TODAY - timedelta(days=10),
        election_date_end = TODAY - timedelta(days=8),
    )
    session.add(election)

    election = model.Elections(
        election_name='Wallpaper F20',
        election_folder='F20',
        election_year='2013',
        election_n_choice=16,
        election_date_start = TODAY - timedelta(days=2),
        election_date_end = TODAY + timedelta(days=3),
    )
    session.add(election)

    election = model.Elections(
        election_name='Wallpaper F21',
        election_folder='F21',
        election_year='2014',
        election_n_choice=16,
        election_date_start = TODAY + timedelta(days=1),
        election_date_end = TODAY + timedelta(days=6),
    )
    session.add(election)
    session.commit()


def create_candidates(session):
    """ Create some basic candidates for testing. """
    candidate = model.Candidates(
        candidate_file='DSC_0951.JPG',
        candidate_name='DSC_0951',
        candidate_author='pingou',
        election_id=1,
    )
    session.add(candidate)

    candidate = model.Candidates(
        candidate_file='DSC_0930.JPG',
        candidate_name='DSC_0930',
        candidate_author='pingou',
        election_id=1,
    )
    session.add(candidate)

    candidate = model.Candidates(
        candidate_file='DSC_0923.JPG',
        candidate_name='DSC_0923',
        candidate_author='pingou',
        election_id=2,
    )
    session.add(candidate)

    candidate = model.Candidates(
        candidate_file='DSC_0922.JPG',
        candidate_name='DSC_0922',
        candidate_author='pingou',
        election_id=2,
    )
    session.add(candidate)

    session.commit()


def create_votes(session):
    """ Add some votes to a some candidates. """

    vote = model.Votes(
        user_name='pingou',
        candidate_id=1,
    )
    session.add(vote)

    vote = model.Votes(
        user_name='ralph',
        candidate_id=1,
    )
    session.add(vote)

    vote = model.Votes(
        user_name='pingou',
        candidate_id=2,
    )
    session.add(vote)

    vote = model.Votes(
        user_name='toshio',
        candidate_id=1,
    )
    session.add(vote)

    vote = model.Votes(
        user_name='toshio',
        candidate_id=2,
    )
    session.add(vote)

    vote = model.Votes(
        user_name='ralph',
        candidate_id=3,
    )
    session.add(vote)

    session.commit()


if __name__ == '__main__':
    SUITE = unittest.TestLoader().loadTestsFromTestCase(Modeltests)
    unittest.TextTestRunner(verbosity=2).run(SUITE)
