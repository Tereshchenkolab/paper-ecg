

# Conversion Process


## Overview

```
                  ┌─────  Grid Mask   ───── Grid Size (px) ───────┐
                  │     (Binary Image)      (height, width)       │
 Cropped Lead  ───┤                                          Integration ───── Scaled Signal
 (Color Image)    │                                             │ │ │
                  └────   Lead Mask   ───── Signal Trace ───────┘ │ │
                        (Binary Image)        (array)             │ │
                                                                  │ │
                                                                  │ │
 Supplied by user:                       Grid Scale (mV and mm/s) ┘ └ Lead Offset (Seconds)
```


## Lead Mask

***

Color Image -> Binary Image


### I. Threshold Methods

*Strategy:* (1) Convert the image to greyscale, and (2) find a brightness level (threshold) that separates pixels in the signal (and potentially other text or markings) from the grid and noise.

#### (1) Greyscale methods

- Standard
- (Convert into special colorspace)?

#### (2) Threshold methods

- Otsu
- (Set by user)?

#### Other

- (Apply thresholing method to each color channel and choose color with best separation for colored grids)?


#### II. Kernel Methods

*Strategy:* Use a very bright threshold to convert to binary (including grid and lots of noise) and then apply kernels to isolate the signal.

- Reverse erosion



### Signal Trace

***

Binary Image -> Array

...



### Grid Mask

***

Color Image -> Binary Image

...



### Grid Size

***

Color Image -> Binary Image

...
