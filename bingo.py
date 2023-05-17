from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Table,
    TableStyle,
)

# mostly written by chatgpt


def build_page(data):
    # Set up styles
    styles = getSampleStyleSheet()
    cell_style = styles["Normal"]
    cell_style.alignment = 1  # Center alignment

    # Define the dimensions of the bingo card table
    table_width = 5.5 * inch
    table_height = 5.5 * inch

    # Create a table to hold the bingo card data
    table_data = []
    for row in data:
        table_row = []
        for item in row:
            text = f'<font size="12">{item}</font>'
            table_row.append(Paragraph(text, cell_style))
        table_data.append(table_row)

    # Create the table and set its style
    table = Table(
        table_data, colWidths=[table_width / 5] * 5, rowHeights=[table_height / 5] * 5
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.black),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.black),
            ]
        )
    )

    # Create a paragraph style for the title
    title_style = styles["Title"]
    title_style.spaceAfter = 50  # Add 10 points of space after the title

    # Create the title paragraph
    title = Paragraph("BINGO Card", title_style)

    # Create a story with the title, table, and page break
    story = [title, table, PageBreak()]

    # Create a story with the table and page break
    story = [Paragraph("BINGO Card", styles["Title"]), table, PageBreak()]

    return story


def main():
    # Create a new PDF document
    doc = SimpleDocTemplate("result.pdf", pagesize=LETTER)

    # Define the data for the bingo cards
    card_data = [
        [
            ["Z", "I", "N", "G", "O"],
            ["1", "16", "31", "46", "61"],
            ["5", "20", "FREE", "50", "65"],
            ["10", "25", "40", "55", "70"],
            ["15", "30", "45", "60", "75"],
        ],
        [
            ["R", "I", "N", "G", "O"],
            ["2", "17", "32", "47", "62"],
            ["6", "21", "FREE", "51", "66"],
            ["11", "26", "41", "56", "71"],
            ["16", "31", "46", "61", "76"],
        ],
        # Add more card data as needed
    ]

    # Create a list to hold all the pages
    pages = []

    # Generate the pages for each card
    for data in card_data:
        page = build_page(data)
        pages.extend(page)

    # Build the document with the pages
    doc.build(pages)

    print("Bingo cards created successfully!")


# Call the function to create multiple bingo cards on separate pages in a single PDF
main()
