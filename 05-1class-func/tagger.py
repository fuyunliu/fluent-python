# -*- coding: utf-8 -*-


def tag(tag_name, *content, cls=None, **attrs):
    """Generate one or more HTML tags"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
                           for attr, value in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s<%s>' % (tag_name, attr_str, c, tag_name)
                         for c in content)
    else:
        return '<%s%s />' % (tag_name, attr_str)
