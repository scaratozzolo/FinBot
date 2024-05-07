from fastapi import APIRouter
import pandas as pd
import string

cipher_router = APIRouter(prefix="/cipher", tags=["Cipher"])

letters = [i for i in string.ascii_uppercase]

matrix = {}
for i, letter in enumerate(letters):
    matrix[letter] = letters[i:] + letters[:i]

cipher_df = pd.DataFrame(matrix, index=letters)

def clean_string(msg):

    msg = msg.upper()
    msg = msg.replace(" ", "")
    msg = msg.strip()

    return msg


@cipher_router.get("/encrypt")
def encrypt_cipher(message: str, cipher: str):

    clean_msg = clean_string(message)
    clean_cipher = clean_string(cipher)

    encrypted = ""

    for i, letter in enumerate(clean_msg):
        cipher_letter = clean_cipher[i % len(clean_cipher)]

        encrypted += cipher_df.loc[letter, cipher_letter]

    return encrypted

@cipher_router.get("/decrypt")
def decrypt_cipher(encrypted: str, cipher: str):

    clean_msg = clean_string(encrypted)
    clean_cipher = clean_string(cipher)

    decrypted = ""

    for i, letter in enumerate(clean_msg):
        cipher_letter = clean_cipher[i % len(clean_cipher)]

        decrypted += cipher_df.loc[cipher_df[cipher_letter] == letter, cipher_letter].index.to_list()[0]

    return decrypted