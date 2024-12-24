import os
import sys

# Static Key and Key Length
Key = "STarYZgr3DL11"
KeyLen = len(Key)

def xor_decrypt(data, key):
    """Decrypts the data using XOR with the given key."""
    return bytes(data[i] ^ ord(key[i % len(key)]) for i in range(len(data)))

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} in.sav")
        return
    
    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        return
    
    # Generate output filename
    base_name, _ = os.path.splitext(input_file)
    output_file = f"{base_name}.json"
    
    try:
        # Read the input file
        with open(input_file, "rb") as in_file:
            data = in_file.read()
        
        # Exclude the last 4 bytes (assume checksum)
        data = data[:-4]
        
        # Decrypt the data
        decrypted_data = xor_decrypt(data, Key)
        
        # Write the decrypted data to the output file
        with open(output_file, "wb") as out_file:
            out_file.write(decrypted_data)
        
        print(f"Writing {input_file} to {output_file}...")
        print("Done!")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()