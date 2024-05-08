from Crypto.PublicKey import ECC
from Crypto.Hash import SHA256
from Crypto.Signature import DSS
import json
from ECC.utils import generate_device_id


def generate_keys():
    key = ECC.generate(curve='P-521')  # 使用 P-521 曲线
    private_key = key.export_key(format='PEM')
    public_key = key.public_key().export_key(format='PEM')
    return private_key.encode(), public_key.encode()  # 转换为 bytes 类型


def generate_license(hardware_info, private_key):
    key = ECC.import_key(private_key)
    hash_obj = SHA256.new(json.dumps(hardware_info).encode('utf-8'))
    signer = DSS.new(key, 'fips-186-3')  # 使用 ECDSA 签名
    signature = signer.sign(hash_obj)
    license_data = {
        "hardware_info": hardware_info,
        "signature": signature.hex()
    }
    return license_data


def main():
    private_key, public_key = generate_keys()
    hardware_info = generate_device_id()
    license_data = generate_license(hardware_info, private_key)

    with open("license.json", "w") as f:
        json.dump(license_data, f)
    with open("public_key.pem", "wb") as f:
        f.write(public_key)

    with open("private_key.pem", "wb") as f:
        f.write(private_key)


if __name__ == "__main__":
    main()
