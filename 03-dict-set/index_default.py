"""Build an index mapping word -> list of occurrences"""

import sys
import re
import collections

WORD_RE = re.compile('\w+')

index = collections.defaultdict(list)
with open(sys.argv[1], 'rt', encoding='utf-8') as f:
    for line_no, line in enumerate(f, 1):
        for match in WORD_RE.finditer(line):
            word = match.group()
            column_no = match.start() + 1
            location = (line_no, column_no)
            index[word].append(location)


for word in sorted(index, key=str.upper):
    print(word, index[word])
