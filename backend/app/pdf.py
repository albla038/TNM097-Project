import io
from numpy.typing import NDArray
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3
from reportlab.lib.utils import ImageReader
from PIL import Image
import matplotlib.pyplot as plt


def generate_pdf_buffer(
    img_data: NDArray,
    page_size: tuple[float, float] = A3,
) -> io.BytesIO:
    """
    Generates a PDF buffer containing the given image data.
    """

    # Get page size in pt
    (page_width, page_height) = page_size

    # Read img data with PIL
    pil_img = Image.fromarray(img_data)
    # Get image dimensions in px to determine print orientation
    (img_width, img_height) = pil_img.size

    # Rotate image by 90 degrees if it is wider than it is taller
    # This makes sure the image is always printed correctly vertical/"standing"
    if img_width > img_height:
        pil_img = pil_img.rotate(90, expand=True)
        (img_width, img_height) = pil_img.size

    # Create image buffer
    img_buffer = io.BytesIO()
    # Save PIL image to buffer
    pil_img.save(img_buffer, format="PNG")
    # Move buffer pointer to start
    img_buffer.seek(0)

    # Create pdf output buffer
    pdf_buffer = io.BytesIO()

    # Create PDF canvas with correct dimensions
    c = canvas.Canvas(pdf_buffer, pagesize=page_size)

    # Draw image on PDF canvas
    c.drawImage(
        image=ImageReader(img_buffer),
        anchor="c",
        preserveAspectRatio=True,
        x=0,
        y=0,
        width=page_width,
        height=page_height,
        mask="auto",
    )
    c.showPage()
    c.save()

    # Move buffer pointer to start
    pdf_buffer.seek(0)

    return pdf_buffer
