import uuid
import hashlib
import subprocess


def get_mac_address():
    mac = hex(uuid.getnode())[2:]
    return ':'.join(mac[i:i + 2] for i in range(0, len(mac), 2))


def get_motherboard_serial():
    if subprocess.os.name == 'nt':
        # Windows
        output = subprocess.check_output("wmic baseboard get serialnumber", shell=True)
    else:
        # Unix-like
        output = subprocess.check_output("sudo dmidecode -s baseboard-serial-number", shell=True)
    return output.decode().strip()


def generate_device_id():
    mac_address = get_mac_address()
    motherboard_serial = get_motherboard_serial()
    unique_id = mac_address + motherboard_serial
    return hashlib.sha256(unique_id.encode()).hexdigest()


def generate_decimal_hash(data):
    # 使用 hashlib 生成 SHA-256 哈希值
    hash_object = hashlib.sha256(data.encode())
    hex_dig = hash_object.hexdigest()

    # 将十六进制的哈希值转换为十进制
    decimal_hash = int(hex_dig, 16)

    return decimal_hash
