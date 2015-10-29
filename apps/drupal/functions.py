#-*- coding: utf-8 -*-
import hashlib

itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

password_get_count_log2 = lambda setting: itoa64.find(setting[3])


def password_base64_encode(inp, count):
    '''
    This function password_base64_encode just copied from Drupal.
    '''
    output = ''
    i = 0

    while i < count-1:
        value = ord(inp[i])
        i += 1
        output += itoa64[value & 0x3f]
        if i < count:
            value |= ord(inp[i]) << 8

        output += itoa64[(value >> 6) & 0x3f]
        if i >= count:
            break
        i += 1

        if i < count:
            value |= ord(inp[i]) << 16

        output += itoa64[(value >> 12) & 0x3f]

        if i >= count:
            break
        i += 1

        output += itoa64[(value >> 18) & 0x3f]

    return output


def check_password(password, pass_hash):
    '''
    This function check_password just copied from Drupal.
    '''
    setting = pass_hash[0:12]
    count_log2 = password_get_count_log2(setting)
    count = xrange(1, (1 << count_log2) + 1)
    salt = setting[4:16]
    hash_tmp = hashlib.sha512((salt password).encode('utf-8')).digest()

    for i in count:
        hash_tmp = hashlib.sha512('{}{}'.format(hash_tmp, password)).digest()

    strlen = len(hash_tmp)
    check_hash = setting + password_base64_encode(hash_tmp, strlen)

    if check_hash[:55] == pass_hash:
        return True
    return False


def split_name(name):
    for i in [' ', '.', '_', '-', '+']:
        name_list = name.split(' ')
        if len(name_list):
            return name_list[:2]
    else:
        return [name, '']


def _str_reverse(string):
    reversed_list = list(string)
    reversed_list.reverse()
    return u''.join(reversed_list)


def text_summary(text, text_format=None, size=None):
    # Find where the delimiter is in the body
    for dtr in ('<!--break-->', '<!-- break -->', '<! -- break -->'):
        try:
            delimiter = text.index(dtr)
        except ValueError:
            continue
        else:
            # If a valid delimiter has been specified, use it to chop off the summary.
            return text[:delimiter]
    else:
        # If the size is zero, and there is no delimiter, the entire body is the summary.
        if size == 0:
            return text

    # We check for the presence of the PHP evaluator filter in the current
    # format. If the body contains PHP code, we do not split it up to prevent
    # parse errors.
    if text_format == 'php_code' and '<?' in text:
        return text

    # If we have a short body, the entire body is the summary.
    if len(text) <= size:
        return text

    # If the delimiter has not been specified, try to split at paragraph or
    # sentence boundaries.

    # The summary may not be longer than maximum length specified. Initial slice.
    summary = text[:size]

    # Store the actual length of the UTF8 string -- which might not be the same
    # as "size".
    max_rpos = len(summary)

    # How much to cut off the end of the summary so that it doesn't end in the
    # middle of a paragraph, sentence, or word.
    # Initialize it to maximum in order to find the minimum.
    min_rpos = max_rpos

    # Store the reverse of the summary. We use strpos on the reversed needle and
    # haystack for speed and convenience.
    reversed_summary = _str_reverse(summary)

    # Build an array of arrays of break points grouped by preference.
    # A paragraph near the end of sliced summary is most preferable.
    break_points = [{u'</p>': 0}]

    # If no complete paragraph then treat line breaks as paragraphs.
    line_breaks = {u'<br />': 6, u'<br>': 4}
    # Newline only indicates a line break if line break converter
    # filter is present.
    if text_format == 'filter_autop':
        line_breaks[u'\n'] = 1

    break_points.append(line_breaks)

    # If the first paragraph is too long, split at the end of a sentence.
    break_points.append({u'. ': 1, u'! ': 1, u'? ': 1, u'。': 0, u'؟ ': 1})

    # Iterate over the groups of break points until a break point is found.
    for points in break_points:
        # Look for each break point, starting at the end of the summary.
        for point, offset in points.items():
            # The summary is already reversed, but the break point isn't.
            try:
                rpos = reversed_summary.index(_str_reverse(point))
            except ValueError:
                pass
            else:
                min_rpos = min([rpos + offset, min_rpos])

        # If a break point was found in this group, slice and stop searching.
        if min_rpos != max_rpos:
            # Don't slice with length 0. Length must be <0 to slice from RHS.
            summary = min_rpos == 0 and summary or summary[0:0-min_rpos]
            break

    return summary
