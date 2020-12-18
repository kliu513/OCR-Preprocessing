# OCR-Preprocessing
### QR-code-reader.py
The program reads QR code from an image and writes code data to a `.xml` file.
Required libraries: Python Imaging Library, pyzbar

### black-edge-detector.py
The program detects and removes black (dark) edges of a scanned/pictured image.
Required library: Python Imaging Library

### image-corrector.py
The program corrects a skewed image and removes its black edges using `edge_detection` from `black-edge-detector.py`.
Required libraries: OpenCV, NumPy, scikit-image, Python Imaging Library

### stamp-extractor.py
The program extracts and removes stamps from an image.
Required libraries: OpenCV, NumPy

### table-extractor.py
The program extracts and removes tables from an image.
