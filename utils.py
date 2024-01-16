from threading import Timer


def has(txt1, txt2, verbose=False):
    if isinstance(txt2, list):
        _has = False
        for t in txt2:
            _has = txt1.find(t) != -1
            if verbose:
                print(t, _has)
            if _has:
                return _has
        return False
    else:
        return txt1.find(txt2) != -1


def setTimeout(fn, ms, *args, **kwargs):
    t = Timer(ms / 1000., fn, args=args, kwargs=kwargs)
    t.start()
    return t
