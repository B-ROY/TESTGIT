from django.core import urlresolvers


def get_named_patterns():
    "Returns list of (pattern-name, pattern) tuples"

    resolver = urlresolvers.get_resolver(None)

    for key, value in resolver.reverse_dict.items():
        print key,value
        if isinstance(key, basestring):
            pass
            #print key,value

    patterns = [
        (key, value[1])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ]
    #print patterns
    return patterns