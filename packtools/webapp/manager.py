#!/usr/bin/env python
# coding: utf-8
import os
import sys
import json
import unittest


WEBAPP_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WEBAPP_PATH)

FLASK_COVERAGE = os.environ.get('FLASK_COVERAGE', None)

if FLASK_COVERAGE:
    try:
        import coverage
    except ImportError:
        msg = 'Não é possível importar o modulo coverage'
        raise RuntimeError(msg)
    COV = None
    if FLASK_COVERAGE:
        COV = coverage.coverage(branch=True, include='packtools/webapp/*')
        COV.start()
else:
    COV = None

from app import create_app
from flask_script import Manager, Shell  # noqa

app = create_app()
manager = Manager(app)

def make_shell_context():
    return dict(
        app=app
    )
manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
@manager.option('-p', '--pattern', dest='pattern')
@manager.option('-f', '--failfast', dest='failfast')
def test(pattern='test_*.py', failfast=False):
    """ Executa tests unitarios.
    Lembre de definir a variável: OPAC_CONFIG="path do arquivo de conf para testing"
    antes de executar este comando:
    > export OPAC_CONFIG="/foo/bar/config.testing" && python manager.py test

    Utilize -p para rodar testes específicos, ex.: test_admin_*.'
    """
    failfast = True if failfast else False

    if COV and not FLASK_COVERAGE:
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)

    tests = unittest.TestLoader().discover('tests', pattern=pattern)

    result = unittest.TextTestRunner(verbosity=2, failfast=failfast).run(tests)

    if COV:
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # covdir = 'tmp/coverage'
        # COV.html_report(directory=covdir)
        # print('HTML version: file://%s/index.html' % covdir)
        COV.erase()

    if result.wasSuccessful():
        return sys.exit()
    else:
        return sys.exit(1)


def manager_run():
    manager.run()

if __name__ == '__main__':
    manager_run()
