import hashlib

'''
The functions password_base64_encode,password_get_count_log2
and check_password just copied from Drupal.
'''

itoa64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def password_base64_encode(inp, count):
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

def password_get_count_log2(setting):
  return itoa64.find(setting[3]);

def check_password(password, pass_hash):
  setting = pass_hash[0:12]
  count_log2 = password_get_count_log2(setting)
  count = range(1, (1 << count_log2) + 1)
  count.reverse()
  salt = setting[4:16]
  hash_tmp = hashlib.sha512(salt + password).digest()

  for i in count:
    hash_tmp = hashlib.sha512(hash_tmp + password).digest()

  strlen = len(hash_tmp)
  check_hash = setting + password_base64_encode(hash_tmp, strlen)

  if check_hash[0:55] == pass_hash:
    return True
  else:
    return False

def split_name(name):
    for i in [' ', '.', '_', '-', '+']:
        name_list = name.split(' ')
        if len(name_list):
            return name_list[:2]
            break
    else:
        return [name, '']

