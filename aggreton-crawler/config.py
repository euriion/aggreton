__author__ = 'euriion'
import sys
import os

if not os.environ.has_key('AGGRETON_CRAWLER'):
    raise Exception('AGGRETON_CRAWLER should be assinged in environment varialbes')
    sys.exit(1)

AGGRETON_CRAWLER = os.environ.has_key('AGGRETON_CRAWLER').strip()

if not os.path.exists(AGGRETON_CRAWLER):
    raise Exception('AGGRETON_CRAWLER directory does not exist')
    sys.exit(1)