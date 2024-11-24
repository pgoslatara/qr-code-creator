import argparse
from io import BytesIO

import qrcode
import requests
from PIL import Image


def cli(args=None):
    """Create a QR code for a presentation."""
    parser = argparse.ArgumentParser(
        description="Create QR codes for your presentations."
    )
    parser.add_argument(
        "--output-file",
        default="qr_code.png",
        help="The name of the output file, must end with '.png'.",
        type=str,
        required=False,
    )
    parser.add_argument(
        "--url",
        help="The URL to your Google Slides presentation.",
        type=str,
        required=True,
    )
    args = parser.parse_args()

    # Create QR code
    qr = qrcode.QRCode(
        version=10,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(args.url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    # Add logo to QR code
    logo = Image.open(
        BytesIO(
            requests.get(
                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-GMQe7hSHK_UDGPXaQo_ZU2YAPDuf7dn4Bg&s",
                timeout=5,
            ).content
        )
    )
    width, height = logo.size
    scale_factor = 1
    x = int((img.size[0] - (logo.size[0] * scale_factor)) / 2)
    y = int((img.size[1] - (logo.size[1] * scale_factor)) / 2)
    box = (x, y, x + int(width * scale_factor), y + int(height * scale_factor))
    logo = logo.resize((box[2] - box[0], box[3] - box[1]))
    img.paste(logo, box)

    # Save QR code
    img.save(args.output_file)
