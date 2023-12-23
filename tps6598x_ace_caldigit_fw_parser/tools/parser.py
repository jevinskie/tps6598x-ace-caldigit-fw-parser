#!/usr/bin/env python3

import sys

from path import Path
from tap import Tap

from tps6598x_ace_caldigit_fw_parser.firmware_image import FirmwareImage


class Args(Tap):
    in_fw: Path  # Input path to firmware
    out_payload: Path  # Output path to write payload binary

    def __init__(self, *args, **kwargs):
        super().__init__(*args, underscores_to_dashes=True, **kwargs)

    def configure(self):
        self.add_argument("-i", "--in_fw")
        self.add_argument("-o", "--out_payload", required=False)


def real_main(args) -> int:
    print(f"Parsing {args.in_fw}")
    fw_img = FirmwareImage.from_path(args.in_fw)
    print(f"fw_img: {str(fw_img)}")
    if args.out_payload is not None:
        fw_img.write_payload(args.out_payload)
    return 0


def main() -> None:
    args = Args().parse_args()
    sys.exit(real_main(args))


if __name__ == "__main__":
    main()
