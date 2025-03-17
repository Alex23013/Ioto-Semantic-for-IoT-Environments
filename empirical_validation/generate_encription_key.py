from cryptography.fernet import Fernet

# Generate a new encryption key
key = Fernet.generate_key()

# Save it to a file for future use
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

print("Encryption Key Generated and Saved!")