import string
import random

def generate_random_string(length=8):
  characters = string.ascii_letters + string.digits
  random_string = "".join(random.choices(characters, k=length))
  return random_string