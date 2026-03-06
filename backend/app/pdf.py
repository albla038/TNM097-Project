import io
from numpy.typing import NDArray
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, A3
from reportlab.lib.utils import ImageReader
from PIL import Image
import matplotlib.pyplot as plt


def generate_pdf_buffer(
    img_data: NDArray,
    page_size: tuple[float, float] = A4,
) -> io.BytesIO:
    """
    Generates a PDF buffer containing the given image data.
    """

    # Read img data with PIL
    pil_img = Image.fromarray(img_data)
    # Get image dimensions in px to determine print orientation
    (img_width, img_height) = pil_img.size

    # Get page size in pt
    (page_width, page_height) = page_size

    # Change page orientation to landscape if image is wider than it is taller
    # This makes sure the image is always printed as large as possible
    if img_width > img_height:
        # Swap page width and height
        page_size = (page_height, page_width)
        (page_width, page_height) = page_size

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
