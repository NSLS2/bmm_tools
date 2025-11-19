
import datetime
import inflection

def now(fmt="%Y-%m-%dT%H-%M-%S"):
    return datetime.datetime.now().strftime(fmt)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def inflect(word, number):
    if abs(number) == 1:
        return('%d %s' % (number, inflection.singularize(word)))
    else:
        return('%d %s' % (number, inflection.pluralize(word)))

