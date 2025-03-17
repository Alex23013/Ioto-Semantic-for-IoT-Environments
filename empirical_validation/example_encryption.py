from cryptography.fernet import Fernet

# Load the key from the file
with open("encryption_key.key", "rb") as key_file:
    encryption_key = key_file.read()

# Create the cipher object
cipher = Fernet(encryption_key)

# Example encryption
plaintext = "Visitor Name"
encrypted_text = cipher.encrypt(plaintext.encode())
print("Encrypted:", encrypted_text)

# Example decryption
decrypted_text = cipher.decrypt(encrypted_text).decode()
print("Decrypted:", decrypted_text)