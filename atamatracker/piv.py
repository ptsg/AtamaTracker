"""piv - Particle Image Velocimetry
"""

import warnings

import numpy
import scipy
import scipy.signal
import scipy.ndimage


warnings.simplefilter('ignore', numpy.ComplexWarning)


def xcorr_norm(image, template):
    """Perform the normalized cross-correlation.

    Parameters:
    image -- [ndarray] Base image to match
    template -- [ndarray] Small image template to search

    Returns:
    cc -- [ndarray] Cross-correlation map
    """
    # cast images
    image = image.astype(numpy.double)
    template = template.astype(numpy.double)

    # normalized cross-correlation
    template = template - scipy.mean(template)
    template = template / scipy.sqrt(scipy.sum(template ** 2))
    template_sum = scipy.sum(template)
    filter_template = numpy.ones(template.shape) / template.size
    filter_sum = numpy.ones(template.shape)
    image_mean = scipy.signal.convolve2d(image, filter_template, 'same')
    image_sq = image ** 2
    image_sq_sum = scipy.signal.convolve2d(image_sq, filter_sum, 'same')
    cc = scipy.ndimage.correlate(image, template)
    cc_norm = ((cc - image_mean * template_sum) /
               scipy.sqrt(image_sq_sum - template.size * image_mean ** 2))

    return cc_norm


def find_point(image1, image2, i, j, pattern_size, di_range, dj_range):
    """Find the similar pattern of (j, i) in image1 from image2.

    Parameters:
    image1 -- [image] Image to refer to the pattern as numpy.ndarray
    image2 -- [image] Image to find the pattern as numpy.ndarray
    i -- [int] Vertical coordinate of pattern center
    j -- [int] Horizontal coordinate of pattern center
    pattern_size -- [int, int] Pattern size
    di_range -- [int, int] Vertical buffer length to find
    dj_range -- [int, int] Horizontal buffer length to find

    Returns:
    di -- Vertical delta of pattern from image1 to image2
    dj -- Horizontal delta of pattern from image1 to image2
    """
    li_half = (pattern_size[0] - 1) / 2
    lj_half = (pattern_size[1] - 1) / 2

    # crop images
    pattern = image1[i - li_half:i + li_half + 1,
                     j - lj_half:j + lj_half + 1]
    image = image2[i - li_half + di_range[0]:i + li_half + 1 + di_range[1],
                   j - lj_half + dj_range[0]:j + lj_half + 1 + dj_range[1]]

    cc = xcorr_norm(image, pattern)
    di, dj = numpy.unravel_index(numpy.argmax(cc), image.shape)

    if (di == 0 or di == cc.shape[0] - 1 or dj == 0 or
            dj == cc.shape[1] - 1 or numpy.max(cc) < 0.5):
        return 0, 0

    # subpixel analysis
    cc_C = cc[di, dj]
    cc_N = cc[di - 1, dj]
    cc_S = cc[di + 1, dj]
    cc_W = cc[di, dj - 1]
    cc_E = cc[di, dj + 1]
    di -= (0.5 * (numpy.log(cc_S) - numpy.log(cc_N)) /
           (numpy.log(cc_S) - 2 * numpy.log(cc_C) + numpy.log(cc_N)))
    dj -= (0.5 * (numpy.log(cc_E) - numpy.log(cc_W)) /
           (numpy.log(cc_E) - 2 * numpy.log(cc_C) + numpy.log(cc_W)))
    di += di_range[0] - li_half
    dj += dj_range[0] - lj_half

    return di, dj
