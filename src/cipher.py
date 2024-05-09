from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
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

    for i in msg:
        if i not in letters:
            msg = msg.replace(i, "")

    return msg


@cipher_router.get("/")
def cipher_index():

    html = """

    <!DOCTYPE html>
    <html>
    <body>

    <h2>Encrypt Messages</h2>

    <form action="#">
    <label for="message">Message:</label><br>
    <textarea type="text" id="message" name="message" rows="4" cols="50"></textarea><br>
    <label for="cipher">Cipher:</label><br>
    <input type="text" id="cipher" name="cipher"><br><br>
    <input type="button" value="Encrypt" onclick="encrypt();">
    <input type="button" value="Decrypt" onclick="decrypt();">
    <br><br><label for="output">Output:</label><br>
    <textarea type="text" id="output" rows="4" cols="50" disabled></textarea>
    </form> 

    <script type="text/javascript">

    const message_input = document.getElementById("message")
    const cipher_input = document.getElementById("cipher")
    const output_box = document.getElementById("output")
    
    async function encrypt(){
        let data = {
            message: message_input.value,
            cipher: cipher_input.value
        }
        const response = await fetch("/cipher/encrypt", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        });
        const resp = await response.json();
        output_box.value = resp.resp;
    }


    async function decrypt(){
        let data = {
            message: message_input.value,
            cipher: cipher_input.value
        }
        const response = await fetch("/cipher/decrypt", {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        });
        const resp = await response.json();
        output_box.value = resp.resp;
    }
    
    </script>
    </body>
    </html>

    """

    return HTMLResponse(html)

class CipherPayload(BaseModel):

    message: str
    cipher: str

@cipher_router.post("/encrypt")
def encrypt_cipher(request: CipherPayload):

    clean_msg = clean_string(request.message)
    clean_cipher = clean_string(request.cipher)

    encrypted = ""

    for i, letter in enumerate(clean_msg):
        cipher_letter = clean_cipher[i % len(clean_cipher)]

        encrypted += cipher_df.loc[letter, cipher_letter]

    return {"resp":encrypted}

@cipher_router.post("/decrypt")
def decrypt_cipher(request: CipherPayload):

    clean_msg = clean_string(request.message)
    clean_cipher = clean_string(request.cipher)

    decrypted = ""

    for i, letter in enumerate(clean_msg):
        cipher_letter = clean_cipher[i % len(clean_cipher)]

        decrypted += cipher_df.loc[cipher_df[cipher_letter] == letter, cipher_letter].index.to_list()[0]

    return {"resp": decrypted}