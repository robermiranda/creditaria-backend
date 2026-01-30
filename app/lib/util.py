import random
import string


def genera_string_aleatorio(length):
    characters = string.ascii_letters + string.digits
    string_aleatorio = ''.join(random.choices(characters, k=length))
    return string_aleatorio
