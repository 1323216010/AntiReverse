from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import json
from utils import generate_device_id


def verify_license(public_key, license_file):
    with open(license_file, "r") as f:
        license_data = json.load(f)

    hardware_info = license_data["hardware_info"]
    signature = bytes.fromhex(license_data["signature"])

    key = ECC.import_key(public_key)
    hash_obj = SHA256.new(json.dumps(hardware_info).encode('utf-8'))
    verifier = DSS.new(key, 'fips-186-3')

    try:
        verifier.verify(hash_obj, signature)
        current_hardware_info = generate_device_id()
        if hardware_info == current_hardware_info:
            print("License is valid and hardware matches.")
        else:
            print("Hardware does not match.")
    except (ValueError, TypeError):
        print("License verification failed.")


def main():
    with open("public_key.pem", "rb") as f:
        public_key = f.read()
    verify_license(public_key, "license.json")


if __name__ == "__main__":
    main()
