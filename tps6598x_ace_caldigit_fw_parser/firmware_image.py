import dataclasses
import sys
from typing import Final, Any

from path import Path
from attrs import define, field
from construct import ByteSwapped, GreedyBytes, Const, Byte, Bytes, Int32ul, Hex, Pointer
from construct_typed import DataclassMixin, DataclassStruct, csfield


_le_native: Final[bool] = sys.byteorder == "little"


def LittleEndianByteSwapped(subcon):
    if _le_native:
        return subcon
    return ByteSwapped(subcon)


@dataclasses.dataclass
class _Version(DataclassMixin):
    data: bytes = csfield(Hex(Bytes(3)))
    major: int = csfield(Hex(Pointer(2, Byte)))
    minor: int = csfield(Hex(Pointer(1, Byte)))
    patch: int = csfield(Hex(Pointer(0, Byte)))


Version = DataclassStruct(_Version)

_version_offset: Final[int] = 0x34


@dataclasses.dataclass
class _Payload(DataclassMixin):
    data: bytes = csfield(GreedyBytes)
    version: Any = csfield(Pointer(_version_offset, Version))


Payload = DataclassStruct(_Payload)


_magic: Final[int] = 0xACEF0001
_pubkey_size: Final[int] = 0x180


@dataclasses.dataclass
class _Firmware(DataclassMixin):
    magic: int = csfield(Const(_magic, Hex(Int32ul)))
    pubkey: bytes = csfield(Bytes(_pubkey_size))
    rsa_sig: bytes = csfield(Bytes(_pubkey_size))
    payload: Any = csfield(Payload)


Firmware = DataclassStruct(_Firmware)


@define
class FirmwareImage:
    img_path: Path
    data: bytes = field(repr=lambda _: "")
    fw: Any

    @classmethod
    def from_path(cls, img_path: Path):
        if not isinstance(img_path, Path):
            img_path = Path(img_path)
        img_path = img_path.expanduser()
        data = open(img_path, "rb").read()
        fw = Firmware.parse(data)
        return cls(img_path, data, fw)

    def write_payload(self, out_payload_path: Path) -> None:
        with open(out_payload_path.expanduser(), "wb") as f:
            f.write(self.fw.payload.data)

    def __str__(self) -> str:
        return f"\nimg_path: {self.img_path}\nfw:\n{self.fw}"
