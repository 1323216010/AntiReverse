from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
import json
from utils import generate_device_id


def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def generate_license(hardware_info, private_key):
    key = RSA.import_key(private_key)
    hash_obj = SHA256.new(json.dumps(hardware_info).encode('utf-8'))
    signature = pkcs1_15.new(key).sign(hash_obj)
    license_data = {
        "hardware_info": hardware_info,
        "signature": signature.hex()
    }
    return license_data


def main():
    private_key, public_key = generate_keys()

    hardware_info = generate_device_id()
    license_data = generate_license(hardware_info, private_key)

    with open("../license.json", "w") as f:
        json.dump(license_data, f)

    with open("../public_key.pem", "wb") as f:
        f.write(public_key)


if __name__ == "__main__":
    main()
