import streamlit as st
import secrets
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

st.title("Quantum Key Distribution (QKD) Demo")

DEFAULTS = {
    "seed_a": None,
    "seed_b": None,
    "plaintext": "",
    "plaintext_input": "",
    "shared_key": None,
    "nonce": None,
    "ciphertext": None,
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset_demo():
    for k, v in DEFAULTS.items():
        st.session_state[k] = v

# Step 1: Input
st.header("Step 1 - Input")
st.markdown("""
**Seed A**: Generated using `secrets.token_bytes(16)` → unpredictable CSPRNG.  
**Seed B**: Same method, simulating quantum randomness.  
**Plaintext**: Default message "Quantum Secure Transaction".  
👉 Reason: `secrets.token_bytes()` uses a cryptographically secure PRNG, ensuring seeds are unpredictable and secure.
""")

if st.button("Generate Seeds"):
    st.session_state.seed_a = secrets.token_bytes(16)
    st.session_state.seed_b = secrets.token_bytes(16)

if st.session_state.seed_a and st.session_state.seed_b:
    st.write("Seed A:", st.session_state.seed_a)
    st.write("Seed B:", st.session_state.seed_b)

st.text_input("Enter plaintext message:", key="plaintext_input")
st.session_state.plaintext = st.session_state.plaintext_input.encode()

# Step 2A: HKDF (simulate QKD generate key function)
st.header("Step 2A - HKDF (simulate QKD generate key function)")
st.markdown("""
HKDF (HMAC-based Key Derivation Function) is used here to **simulate the key generation step of QKD**.  
Real QKD requires quantum hardware to produce truly random shared keys.  
Since we don’t have quantum hardware, HKDF is applied instead to combine Seed A + Seed B into a strong 256‑bit shared key.
""")

if st.button("Derive Shared Key"):
    if st.session_state.seed_a and st.session_state.seed_b:
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b"qkd-demo",
            backend=default_backend()
        )
        st.session_state.shared_key = hkdf.derive(
            st.session_state.seed_a + st.session_state.seed_b
        )

if st.session_state.shared_key:
    st.write("Shared Key:", st.session_state.shared_key)

# Step 2B: AES-GCM Encryption
st.header("Step 2B - AES-GCM Encryption")
st.markdown("""
AES-GCM provides confidentiality + integrity.  
**Nonce (12 bytes)** ensures uniqueness each time, preventing replay attacks.  
**Ciphertext** is the encrypted message, different even if plaintext repeats.
""")

if st.button("Encrypt Message"):
    if st.session_state.shared_key and st.session_state.plaintext:
        aesgcm = AESGCM(st.session_state.shared_key)
        st.session_state.nonce = secrets.token_bytes(12)
        st.session_state.ciphertext = aesgcm.encrypt(
            st.session_state.nonce,
            st.session_state.plaintext,
            None
        )

if st.session_state.nonce and st.session_state.ciphertext:
    st.write("Nonce:", st.session_state.nonce)
    st.write("Ciphertext:", st.session_state.ciphertext)

# Step 2C: Decryption (simulate QKD restore plaintext)
st.header("Step 2C - Decryption (simulate QKD restore plaintext)")
st.markdown("""
Decryption here **simulates the restoration of plaintext in a QKD workflow**.  
In real QKD, the shared quantum key would be used with classical cryptography to recover the message.  
In this demo, we use the derived HKDF key + Nonce + Ciphertext to restore the original plaintext.
""")

if st.button("Decrypt Message"):
    if st.session_state.shared_key and st.session_state.nonce and st.session_state.ciphertext:
        aesgcm = AESGCM(st.session_state.shared_key)
        decrypted = aesgcm.decrypt(
            st.session_state.nonce,
            st.session_state.ciphertext,
            None
        )
        st.write("Decrypted Message:", decrypted.decode())


# Terminology
with st.expander("Terminology"):
    st.write("QKD (Quantum Key Distribution) — secure key exchange using quantum principles.")
    st.write("HKDF (HMAC-based Key Derivation Function) — derives strong keys from input material.")
    st.write("AES-GCM (Advanced Encryption Standard – Galois/Counter Mode) — encryption mode providing confidentiality and integrity.")
    st.write("Nonce (Number used once) — ensures uniqueness of each encryption operation.")
    st.write("Seed (random binary input) — starting material for key derivation.")
    st.write("CSPRNG (Cryptographically Secure Pseudo Random Number Generator) — produces unpredictable random values suitable for cryptography.")


# Traceable Summary
st.subheader("Traceable Summary")
st.markdown("""
**Simulated QKD Workflow**  
- Input: Seed A + Seed B + Plaintext  
- Process: HKDF (simulate QKD key generation) → Shared Key  
- AES-GCM → Nonce + Ciphertext  
- Decryption (simulate QKD restore plaintext) → Restored Plaintext
""")

# Restart Demo
st.header("Restart Demo")
st.button("Restart", on_click=reset_demo)
