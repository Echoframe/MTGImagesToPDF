# MTG Proxy Card Print Pipeline

I couldn't find a working tool for slapping images into a grid that has the right size so i made this, one i found was broken somehow.

This project allows you to create **print-ready PDFs of Magic: The Gathering cards** at professional quality, with proper bleed, DPI alignment, and color compensation for **Canon Photo Paper Plus Glossy II** using an **Epson ET-2851** printer.

## Features

* Layout MTG cards on **A4 pages** (3x3 grid, 9 cards per page)
* **Bleed margins** for precise cutting
* **DPI validation and optional upscaling** for low-resolution images
* **Glossy-paper compensation** to avoid pale prints
* **RGB workflow** optimized for Epson inkjet drivers

## Requirements

* Python 3.8+
* Packages:

  ```bash
  pip install pillow reportlab
  ```

  Optional for AI upscaling:

  ```bash
  pip install realesrgan torch torchvision numpy
  ```
* Input images of cards in **PNG, JPEG, or TIFF format**
* Canon Photo Paper Plus Glossy II

## Directory Structure

```
mtg_print_project/
├── cards/             # Folder containing card images
├── mtg_a4_print_final.py   # Main Python script
├── README.md          # This file
```

## Usage / Startup Guide

1. **Prepare input images**

   * Place your card scans/images in the `cards/` directory
   * Supported formats: `.png`, `.jpg`, `.jpeg`, `.tif`, `.tiff`

2. **Check images resolution**

   * Ideally 1200 DPI scans for best quality
   * The script will automatically upscale images below 600 DPI

3. **Run the script**

   ```bash
   python mtg_a4_print_final.py
   ```

   * The script will process each card, apply optional upscaling, glossy compensation, and generate the print-ready PDF
   * Progress is displayed in the console

4. **Verify PDF**

   * Open the generated `mtg_a4_print_ready.pdf`
   * Use a PDF viewer to check that card sizes are correct (63mm x 88mm)

5. **Printer settings (Epson ET-2851)**

   * Paper type: Canon Photo Paper Plus Glossy II
   * Color management: Application manages color (RGB)
   * Enhancements: OFF
   * Scaling: 100% / Actual size
   * Borderless: OFF
   * Orientation: Portrait

6. **Print the PDF**

   * Ensure settings above
   * Print a test page to verify sizing before full batch

## Optional Enhancements

* **AI-based upscaling** for very low-resolution images using Real-ESRGAN
* **Test grid overlay** for verifying cut sizes

## Notes

* Do **not convert images to CMYK** manually; keep them RGB for correct color rendering on glossy photo paper.
* Avoid printer automatic scaling; it will change the card size.
* The script creates **temporary TIFF files** for processing, which are deleted automatically.
* Bleed is included to allow precise cutting.

---