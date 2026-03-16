import hashlib


def sha256_hex(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.sha256(data).hexdigest()


def find_collision(bits=32):
    """
    Find a SHA-256 collision in a truncated hash space using a birthday attack.

    For a hash with `bits` bits, by the birthday paradox we expect to find a
    collision after approximately 2^(bits/2) attempts.

    :param bits: Number of bits to use from the SHA-256 hash (must be a multiple of 4)
    :return: Tuple of (input1, input2, truncated_hash)
    """
    assert bits % 4 == 0, "bits must be a multiple of 4 (hex nibbles)"
    hex_chars = bits // 4

    seen = {}
    i = 0
    while True:
        msg = f"msg_{i}"
        h = sha256_hex(msg)[:hex_chars]
        if h in seen:
            return seen[h], msg, h
        seen[h] = msg
        i += 1


def part1():
    bits = 32
    input1, input2, collision_hash = find_collision(bits=bits)
    print(f"Collision in first {bits} bits of SHA-256:")
    print(f"  input1            : {input1}")
    print(f"  input2            : {input2}")
    print(f"  sha256(input1)    : {sha256_hex(input1)}")
    print(f"  sha256(input2)    : {sha256_hex(input2)}")
    print(f"  shared prefix     : {collision_hash}")


def part2():
    bits = 256
    birthday_bound = bits // 2
    print(f"For full {bits}-bit SHA-256:")
    print(f"  Finding a collision requires roughly 2^{birthday_bound} attempts")
    print(f"  (approximately 3.40e+38 hash evaluations)")
    print(f"  This is computationally infeasible with current technology.")


part1()
part2()
