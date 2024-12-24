import os
import sys
import struct

# Static Key and Key Length
Key = "STarYZgr3DL11"
KeyLen = len(Key)

def crc32b(message):
    """Calculate CRC32 checksum."""
    crc = 0xFFFFFFFF
    for byte in message:
        crc ^= byte
        for _ in range(8):
            mask = -(crc & 1)
            crc = (crc >> 1) ^ (0xEDB88320 & mask)
    return ~crc & 0xFFFFFFFF

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} in.json")
        return

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        return

    # Get output file name
    base_name, _ = os.path.splitext(input_file)
    output_file = f"{base_name}.sav"

    try:
        # Read input file
        with open(input_file, "rb") as in_file:
            data = in_file.read()

        print(f"Writing {input_file} to {output_file}...")

        # Calculate checksum
        checksum = crc32b(data)

        # Encrypt data
        encrypted_data = bytearray(data)
        for i in range(len(encrypted_data)):
            encrypted_data[i] ^= ord(Key[i % KeyLen])

        # Append checksum
        encrypted_data += struct.pack('<I', checksum)

        # Write to output file
        with open(output_file, "wb") as out_file:
            out_file.write(encrypted_data)

        print("Done!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()