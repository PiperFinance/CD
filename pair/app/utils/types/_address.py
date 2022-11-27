import re
from web3 import Web3


class Address(str):
    """
    # * This can change base on the chain you are in but in general this means
    # * addresses not starting with 0x and are invalid
    # * address are converted via web3.tochecksum :)
    """
    address_Eth_like = re.compile(r'^0x[0-9a-fA-F]{40}$')

    NO_ADDRESS = "0x0000000000000000000000000000000000000000"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    def __new__(cls, v):
        return super().__new__(str, Web3.toChecksumAddress(v))

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            pattern='^0x[0-9a-fA-F]{40}$',
            examples=[
                '0xEF45d134b73241eDa7703fa787148D9C9F4950b0',
                '0x152eE697f2E276fA89E96742e9bB9aB1F2E61bE3'
            ],
        )

    @classmethod
    def is_valid(cls, v) -> bool:
        return cls.address_Eth_like.fullmatch(v) is not None

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        m = cls.address_Eth_like.fullmatch(v)
        if m is None:
            raise ValueError('invalid address format')
        return Web3.toChecksumAddress(v)

    def to_bytes32(self):
        return "000000000000000000000000"+self[2:].lower()

    def __repr__(self):
        return f'Address({super().__repr__()})'

    def __str__(self):
        return self

    def __hash__(self) -> int:
        return super().__hash__()

    @property
    def checked(self):
        '''Makes Sure Address is Checksumed'''
        return Web3.toChecksumAddress(self)
