import hashlib

def hashPassword(_password):
  encodedPassword = str(_password).encode()
  hashedPassword = hashlib.sha256(encodedPassword).hexdigest()
  return hashedPassword

def verifyPassword(_password, _hashedPassword):
  encodedPassword = str(_password).encode()
  hashedPassword = hashlib.sha256(encodedPassword).hexdigest()
  if hashedPassword == _hashedPassword:
    return True
  return False

if __name__ == '__main__':
  hashedPassword = hashPassword("hola123")
  verification = verifyPassword("hola123", "b460b1982188f11d175f60ed670027e1afdd16558919fe47023ecd38329e0b7f")
  print(verification)