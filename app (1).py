import streamlit as st
import pandas as pd

def caesar_encrypt(text, shift):
    result = ""
    steps = []
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            steps.append((char, new_char))
            result += new_char
        else:
            result += char
    return result, steps

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text, key):
    text = text.upper().replace(" ", "")
    key = key.upper()
    key_stream = (key * (len(text) // len(key) + 1))[:len(text)]
    
    steps = []
    encrypted_text = "".join(
        chr(((ord(p) - ord('A') + ord(k) - ord('A')) % 26) + ord('A'))
        for p, k in zip(text, key_stream)
    )
    for p, k, e in zip(text, key_stream, encrypted_text):
        steps.append((p, k, e))
    return encrypted_text, steps

def vigenere_decrypt(text, key):
    text = text.upper().replace(" ", "")
    key = key.upper()
    key_stream = (key * (len(text) // len(key) + 1))[:len(text)]
    
    steps = []
    decrypted_text = "".join(
        chr(((ord(c) - ord('A') - (ord(k) - ord('A'))) % 26) + ord('A'))
        for c, k in zip(text, key_stream)
    )
    for c, k, d in zip(text, key_stream, decrypted_text):
        steps.append((c, k, d))
    return decrypted_text, steps

def hybrid_encrypt(plaintext, vigenere_key, caesar_shift):
    vigenere_encrypted, vigenere_steps = vigenere_encrypt(plaintext, vigenere_key)
    caesar_encrypted, caesar_steps = caesar_encrypt(vigenere_encrypted, caesar_shift)
    return vigenere_encrypted, caesar_encrypted, vigenere_steps, caesar_steps

def hybrid_decrypt(ciphertext, vigenere_key, caesar_shift):
    caesar_decrypted, caesar_steps = caesar_decrypt(ciphertext, caesar_shift)
    vigenere_decrypted, vigenere_steps = vigenere_decrypt(caesar_decrypted, vigenere_key)
    return caesar_decrypted, vigenere_decrypted, caesar_steps, vigenere_steps

st.title("Vigenere + Caesar Cipher Encryption & Decryption")

mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"])

vigenere_key = st.text_input("Enter Vigenere Cipher Key:")
caesar_shift = st.number_input("Enter Caesar Cipher Shift Value:", min_value=1, max_value=25, value=3)

if mode == "Encrypt":
    plaintext = st.text_input("Enter Plaintext:")
    if st.button("Encrypt"):
        vigenere_result, final_encrypted, vigenere_steps, caesar_steps = hybrid_encrypt(plaintext, vigenere_key, caesar_shift)
        st.write(f"Vigenere Encrypted Text: {vigenere_result}")
        st.write(f"Final Encrypted Text (Caesar Applied): {final_encrypted}")
        
        st.subheader("Vigenere Encryption Steps")
        vigenere_df = pd.DataFrame(vigenere_steps, columns=["Plaintext Letter", "Key Letter", "Encrypted Letter"])
        st.table(vigenere_df)
        
        st.subheader("Caesar Encryption Steps")
        caesar_df = pd.DataFrame(caesar_steps, columns=["Before Shift", "After Shift"])
        st.table(caesar_df)

elif mode == "Decrypt":
    ciphertext = st.text_input("Enter Ciphertext:")
    if st.button("Decrypt"):
        caesar_decrypted, final_decrypted, caesar_steps, vigenere_steps = hybrid_decrypt(ciphertext, vigenere_key, caesar_shift)
        st.write(f"After Caesar Decryption: {caesar_decrypted}")
        st.write(f"Final Decrypted Text (Vigenere Applied): {final_decrypted}")
        
        st.subheader("Caesar Decryption Steps")
        caesar_df = pd.DataFrame(caesar_steps, columns=["Before Shift", "After Shift"])
        st.table(caesar_df)
        
        st.subheader("Vigenere Decryption Steps")
        vigenere_df = pd.DataFrame(vigenere_steps, columns=["Ciphertext Letter", "Key Letter", "Decrypted Letter"])
        st.table(vigenere_df)