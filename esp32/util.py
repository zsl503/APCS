
import json

users = {
    b'x\xea\x04\x88': {
        6: {
            "passwd": b'\xff\xff\xff\xff\xff\xff',
            "content": b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
            "operate":None
        }
    }
}


def cal_dcs(b: bytearray):
    sum = 0
    for i in b:
        sum += i
    return 256 - sum % 256


def bytes_to_numbers(b: bytes) -> List[int]:
    bs = []
    for i in b:
        bs.append(i)
    return bs


def numbers_to_bytes(numbers: List[int]) -> bytes:
    bs = bytearray()
    for i in numbers:
        bs.append(i)
    return bs


def bytes_to_number(b: bytes) -> List[int]:
    sum = 0
    for i in b:
        sum *= 256
        sum += i
    return sum


def find_by_uid_block(uid: bytes, block_id: int) -> Optional[(bytes, bytes)]:
    """
    根据uid和块号获取user的密钥和内容，如果找不到，返回None
    :param uid: uid
    :param block_id: 块号
    :return: 密钥和内容，找不到返回None
    """
    if uid in users.keys() and block_id in users[uid].keys():
        return users[uid][block_id]["passwd"], users[uid][block_id]["content"],users[uid][block_id]["operate"]
    else:
        return None


if __name__ == "__main__":
    b = b'x\xea\x04\x88'
    print(find_by_uid_block(b, 7))
