import io
from numpy.typing import NDArray
from definitions import RegionDetail
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image
from utils import create_coordinate_scales


def generate_pdf_buffer(
    img_data: NDArray,
    region_details: list[RegionDetail],
    page_size: tuple[float, float] = A4,
    target_dpi=300,
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

    # Set font and color for labels
    initial_font_size = 14
    c.setFont("Courier-Bold", initial_font_size)
    c.setFillColorRGB(0.66, 0.66, 0.66)

    # Create scaling functions (img pixels --> canvas pt)
    (scale_x, scale_y) = create_coordinate_scales(
        img_width, img_height, page_width, page_height
    )

    # Draw labels in center of each region
    for region in region_details:
        label_str = str(region["label"])
        px = region["col"]
        py = region["row"]
        max_size_px = region["max_size_px"]

        # Map font size to max size that can fit in region 
        font_size = initial_font_size
        derived_font_size = (max_size_px / target_dpi) * 72
        if derived_font_size < font_size:
            font_size = derived_font_size

        font_y_offset = 0.35 * font_size
        c.setFontSize(0.75 * font_size)

        c.drawCentredString(scale_x(px), scale_y(py) - font_y_offset, label_str)

    c.showPage()
    c.save()

    # Move buffer pointer to start
    pdf_buffer.seek(0)

    return pdf_buffer
