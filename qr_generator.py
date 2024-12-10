import qrcode
from typing import List


def generate_qr_code_as_list(url: str) -> List[List[bool]]:
    """
    Takes URL and returns a 2D boolean array representing the QR grid

    True=Black
    False=White
    :param url: The URL to convert to array
    :return: A 2D boolean array representing the URL's QR grid
    """
    # TODO(Check customizations)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(url)
    qr.make()

    return qr.modules
