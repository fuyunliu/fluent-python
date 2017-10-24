"""

Radical folding and text sanitizing.

Handling a string with `cp1252` symbols:
    >>> order = '“Herr Voß: • ½ cup of Œtker™ caffè latte • bowl of açaí.”'
    >>> shave_marks(order)
    '“Herr Voß: • ½ cup of Œtker™ caffe latte • bowl of acai.”'
    >>> shave_marks_latin(order)
    '“Herr Voß: • ½ cup of Œtker™ caffe latte • bowl of acai.”'
    >>> dewinize(order)
    '"Herr Voß: - ½ cup of OEtker(TM) caffè latte - bowl of açaí."'
    >>> asciize(order)
    '"Herr Voss: - 1⁄2 cup of OEtker(TM) caffe latte - bowl of acai."'

Handling a string with Greek and Latin accented characters:
    >>> greek = 'Ζέφυρος, Zéfiro'
    >>> shave_marks(greek)
    'Ζεφυρος, Zefiro'
    >>> shave_marks_latin(greek)
    'Ζέφυρος, Zefiro'
    >>> dewinize(greek)
    'Ζέφυρος, Zéfiro'
    >>> asciize(greek)
    'Ζέφυρος, Zefiro'

"""

import unicodedata
import string


def shave_marks(txt):
    """Remove all diacritic marks"""
    norm_txt = unicodedata.normalize('NFD', txt)
    shaved = ''.join(c for c in norm_txt if not unicodedata.combining(c))
    return unicodedata.normalize('NFC', shaved)


def shave_marks_latin(txt):
    """Remove all diacritic marks from Latin base characters"""
    norm_txt = unicodedata.normalize('NFD', txt)
    latin_base = False
    keepers = []
    for c in norm_txt:
        if unicodedata.combining(c) and latin_base:
            continue  # ignore diacritic on Latin base char
        keepers.append(c)
        # if it isn't combining char, it's a new base char
        if not unicodedata.combining(c):
            latin_base = c in string.ascii_letters
    shaved = ''.join(keepers)
    return unicodedata.normalize('NFC', shaved)


single_map = str.maketrans("""‚ƒ„†ˆ‹‘’“”•–—˜›""",
                           """'f"*^<''""---~>""")

multi_map = str.maketrans({  # <2>
    '€': '<euro>',
    '…': '...',
    'Œ': 'OE',
    '™': '(TM)',
    'œ': 'oe',
    '‰': '<per mille>',
    '‡': '**',
})

multi_map.update(single_map)


def dewinize(txt):
    """Replace Win1252 symbols with ASCII chars or sequences"""
    return txt.translate(multi_map)


def asciize(txt):
    no_marks = shave_marks_latin(dewinize(txt))
    no_marks = no_marks.replace('ß', 'ss')
    return unicodedata.normalize('NFKC', no_marks)
