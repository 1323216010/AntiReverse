import json
from ECC.generate_keys import generate_device_id, generate_license


def main():
    with open("private_key.pem", "rb") as f:
        private_key = f.read()

    hardware_info = generate_device_id()
    license_data = generate_license(hardware_info, private_key)

    with open("license.json", "w") as f:
        json.dump(license_data, f)


if __name__ == "__main__":
    main()
