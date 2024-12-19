import bcrypt

password_kitty = "1234"
password_doggy = "5678"

# Hashing the passwords
hash_kitty = bcrypt.hashpw(password_kitty.encode('utf-8'), bcrypt.gensalt())
hash_doggy = bcrypt.hashpw(password_doggy.encode('utf-8'), bcrypt.gensalt())

# Print the hashed passwords to put in credentials.json
print("Kitty's hashed password:", hash_kitty.decode('utf-8'))
print("Doggy's hashed password:", hash_doggy.decode('utf-8'))