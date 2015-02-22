# coding=utf-8

import os
import uuid
import unicodedata

from random import choice
from string import ascii_lowercase, digits

from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


def validateDataInDict(dictionary, *keys):
    for key in keys:
        if key not in dictionary:
            return False, _(u"Faltan datos")
        if not dictionary[key]:
            return False, _(u"Información inválida")

    return True, ''


def all_keys_valid_inside_dict(dictionary, *keys):
    for key in keys:
        if key not in dictionary or not dictionary[key]:
            return False
    return True


def get_first_error(errors):
    if isinstance(errors, dict):
        for field, list_errors in errors.items():
            for error in list_errors:
                return _(unicode(error))
                # if field == '__all__':
                #     return _(unicode(error))
                # return _(unicode(field).upper() + ' : ' + unicode(error))
    else:
        return None


def generate_random_username(
    length=16, chars=ascii_lowercase+digits,
    split=4, delimiter='-'
):

    username = ''.join([choice(chars) for i in xrange(length)])

    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(
            length=length,
            chars=chars,
            split=split,
            delimiter=delimiter
        )
    except User.DoesNotExist:
        return username


def isfloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def zip_filename_to_info_solution(filename):
    try:
        parts = filename.split('/')[::-1]
        filename = parts[0].split('.')
        return {
            'name': filename[0],
            'ext': filename[1],
            'filename': parts[0],
            'tasktopic': parts[1],
            'tasktype': parts[2],
            'week': parts[3],
            'season': parts[4],
            'precollege': parts[5],
        }
    except Exception:
        return None


def create_filename(filename, folder):
    ext = filename.split('.')[-1]
    filename = '%s.%s' % (uuid.uuid4().hex, ext)
    return os.path.join(folder, filename)


def remove_accents(cad):
    if type(cad) is not unicode:
        cad = unicode(cad)

    return ''.join([c for c in unicodedata.normalize('NFD', unicode(cad)) if unicodedata.category(c) != 'Mn'])
