#!/usr/bin/env python3
# coding: utf8

import logging
from fpdf import FPDF
from checks import smart_input

pdf = FPDF()
pdf.add_page()


def list_fonts(fonts: list[str]):
    for i, font in enumerate(fonts):
        print(f"{i}: {font}")


def choose_font(fonts: list[str]):
    logging.debug("Choosing font")
    list_fonts(fonts)
    font_index = smart_input(f"Which font do you want for the pdf? (0-{len(fonts) - 1}) > ", len(fonts) - 1)
    pdf.add_font(fonts[font_index], '', "./fonts/" + fonts[font_index] + ".ttf", uni=True)
    pdf.set_font(fonts[font_index], size=15)
    logging.debug(f"Chose font {fonts[font_index]}")


def write_to_pdf(pdf_name: str, exported_file_name: str):
    logging.debug(f"Writing text to file {pdf_name}")
    with open(exported_file_name + ".txt", "r", encoding="utf-8") as f:
        pdf.multi_cell(190, 8, txt=f.read())

    pdf.output("simplified_" + pdf_name)
    logging.debug("Wrote text to file successfully")
