import base58
import hmac
import uuid

import axolotl_curve25519 as curve
import pywaves.crypto as crypto
from _sha1 import sha1


def generate_auth_data():
    new_uuid = uuid.uuid4()
    return hmac.new(new_uuid.bytes, digestmod=sha1).hexdigest()


def str_with_length(string_data):
    string_length_bytes = len(string_data).to_bytes(2, byteorder='big')
    string_bytes = string_data.encode('utf-8')
    return string_length_bytes + string_bytes


def signed_data(host, data):
    prefix = 'WavesWalletAuthentication'
    return str_with_length(prefix) + str_with_length(host) + str_with_length(data)


def verify_signature(public_key, signature, message):
    public_key_bytes = base58.b58decode(public_key)
    signature_bytes = base58.b58decode(signature)

    return curve.verifySignature(public_key_bytes, message, signature_bytes) == 0


def verify_address(public_key, address):
    public_key_bytes = base58.b58decode(public_key)
    unhashed_address = chr(1) + str('W') + crypto.hashChain(public_key_bytes)[0:20]
    address_hash = crypto.hashChain(crypto.str2bytes(unhashed_address))[0:4]
    address_from_public_key = base58.b58encode(crypto.str2bytes(unhashed_address + address_hash))

    return address_from_public_key == address
