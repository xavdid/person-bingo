import json
from itertools import chain, islice
from random import sample
from typing import Iterable

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

FREE_FACT = "Knows David or Vicky!"
NUM_CARDS = 5


# https://docs.python.org/3/library/itertools.html#itertools-recipes
# until py 3.12
def batched(iterable: list[str], n) -> Iterable[list[str]]:
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := list(islice(it, n)):
        yield batch


def pick_facts(facts: list[str]) -> list[list[str]]:
    chosen = sample(facts, 24)
    chosen.insert(12, FREE_FACT)
    return list(batched(chosen, 5))


# mostly written by chatgpt


def build_page(data):
    # Set up styles
    styles = getSampleStyleSheet()
    cell_style = styles["Normal"]
    cell_style.alignment = 1  # Center alignment

    # Define the dimensions of the bingo card table
    table_width = 6 * inch
    table_height = 7 * inch

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
                ("TOPPADDING", (0, 0), (-1, -1), 10),  # top padding
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

    return story


def main():
    # Create a new PDF document
    doc = SimpleDocTemplate("result.pdf", pagesize=LETTER)

    # Define the data for the bingo cards
    with open("facts.json") as f:
        facts = json.loads(f.read())
    assert len(facts) >= 24, "must have at least 24 facts for a 5x5 grid + free square"

    # Generate the pages for each card
    doc.build(
        list(
            # from_iterable gives me the flat list I need
            chain.from_iterable(build_page(pick_facts(facts)) for _ in range(NUM_CARDS))
        )
    )

    print("Bingo cards created successfully!")


# Call the function to create multiple bingo cards on separate pages in a single PDF
main()
