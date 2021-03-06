'''
PassportEye::Util: Interface between SKImage and the PyTesseract OCR
NB: You must have the "tesseract" tool present in your path for this to work.

Author: Konstantin Tretyakov
License: MIT
'''

from pytesseract import pytesseract
from scipy.misc import imsave

def ocr(img, mrz_mode=True):
    """Runs Tesseract on a given image. Writes an intermediate tempfile and then runs the tesseract command on the image.

    This is a simplified modification of image_to_string from PyTesseract, which is adapted to SKImage rather than PIL.

    In principle we could have reimplemented it just as well - there are some apparent bugs in PyTesseract (e.g. it
    may lose the NamedTemporaryFile due to its auto-delete behaviour).

    :param mrz_mode: when this is True (default) the tesseract is configured to recognize MRZs rather than arbitrary texts.
    """
    input_file_name = '%s.bmp' % pytesseract.tempnam()
    output_file_name_base = '%s' % pytesseract.tempnam()
    output_file_name = "%s.txt" % output_file_name_base
    try:
        imsave(input_file_name, img)

        if mrz_mode:
            config = "-psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789>< -c load_system_dawg=F -c load_freq_dawg=F"
        else:
            config = None

        status, error_string = pytesseract.run_tesseract(input_file_name,
                                             output_file_name_base,
                                             lang=None,
                                             boxes=False,
                                             config=config)
        if status:
            errors = pytesseract.get_errors(error_string)
            raise pytesseract.TesseractError(status, errors)
        f = open(output_file_name)
        try:
            return f.read().strip()
        finally:
            f.close()
    finally:
        pytesseract.cleanup(input_file_name)
        pytesseract.cleanup(output_file_name)
