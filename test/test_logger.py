from __future__ import with_statement
import tempfile
import StringIO
import pyyaks.logger

def test_suppress_newline():
    stdout = StringIO.StringIO()
    logger = pyyaks.logger.get_logger(level=pyyaks.logger.INFO, stream=stdout)
    for handler in logger.handlers:
        handler.suppress_newline = True
    logger.info('Info')
    logger.warning('Warning')
    for handler in logger.handlers:
        handler.suppress_newline = False
    logger.info('Info')
    logger.warning('Warning')
    assert stdout.getvalue() == "InfoWarningInfo\nWarning\n"

def test_suppress_newline_cm():
    stdout = StringIO.StringIO()
    logger = pyyaks.logger.get_logger(level=pyyaks.logger.INFO, stream=stdout)
    with pyyaks.logger.newlines_suppressed(logger):
        logger.info('Info')
        logger.warning('Warning')
    logger.info('Info')
    logger.warning('Warning')
    assert stdout.getvalue() == "InfoWarningInfo\nWarning\n"

def test_stream():
    stdout = StringIO.StringIO()
    logger = pyyaks.logger.get_logger(level=pyyaks.logger.INFO, stream=stdout)
    logger.debug('Debug')
    logger.info('Info')
    logger.warning('Warning')
    assert stdout.getvalue() == "Info\nWarning\n"
    
def test_file():
    tmp = tempfile.NamedTemporaryFile()
    logger = pyyaks.logger.get_logger(filename=tmp.name, stream=None)
    logger.debug('Debug')
    logger.info('Info')
    logger.warning('Warning')
    assert open(tmp.name).read() == "Info\nWarning\n"
    
def test_redefine():
    stdout1 = StringIO.StringIO()
    stdout2 = StringIO.StringIO()
    tmp1 = tempfile.NamedTemporaryFile()
    tmp2 = tempfile.NamedTemporaryFile()
    logger = pyyaks.logger.get_logger(filename=tmp1.name, stream=stdout1, filelevel=pyyaks.logger.WARNING)
    logger.debug('Debug1')
    logger.info('Info1')
    logger.warning('Warning1')
    logger = pyyaks.logger.get_logger(filename=tmp2.name, stream=stdout2, level=pyyaks.logger.DEBUG)
    logger.debug('Debug2')
    logger.info('Info2')
    logger.warning('Warning2')
    assert open(tmp1.name).read() == "Warning1\n"
    assert stdout1.getvalue() == "Info1\nWarning1\n"
    assert open(tmp2.name).read() == "Debug2\nInfo2\nWarning2\n"
    assert stdout2.getvalue() == "Debug2\nInfo2\nWarning2\n"
