"""
this is a basic test file
"""

import locale
locale.setlocale(locale.LC_ALL, '')

num = 10000000

print('{:n}'.format(num))