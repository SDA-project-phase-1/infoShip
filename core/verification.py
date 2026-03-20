#  basically core sends data packet to a queue from where they are passed to another function lets say aggregator
# which now sends direct data packet to browser
# and also holds them
# now with every packets , its send avg value to browser 
import hashlib

def generate_signature(raw_value_str: str, key: str, iterations: int) -> str:
    """
    Generates a PBKDF2 HMAC SHA-256 signature for the given value.
    Treats the secret key as the password and the raw value as the salt.
    """
    password_bytes = key.encode('utf-8')
    salt_bytes = raw_value_str.encode('utf-8')
    
    # Generate the hash
    hash_bytes = hashlib.pbkdf2_hmac(
        hash_name='sha256', 
        password=password_bytes, 
        salt=salt_bytes, 
        iterations=iterations
    )
    return hash_bytes.hex()

def verify_the_signature(hash_val_in_dataset:str, secret_key_in_config:str,iteration:int,data:str) -> bool:
    generated = generate_signature(data,secret_key_in_config,iteration)
    if generated == hash_val_in_dataset:
        return True
    return False