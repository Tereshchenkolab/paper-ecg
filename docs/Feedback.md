# Project Presentation Feedback

This feedback was solicited after a presentation given on May 7, 2021 to a cohort of peer groups focused on machine learning. The feedback is presentation and an explanation is given as to whether or not it will be acted upon.

## Bounding Box Improvements

> The lead detection through bounding boxes seems like it could be well improved. 
> Since the traces are the only black parts of the image (minus the labels) being able
> to click and select all the pixels seems like it would be easily do-able (similar to
> paint->fill).

One peer some very creative suggestion for lead detection. It is not entirely clear precisely what they had in mind, but there are two possibilities that seems reasonable: identifying so-called "contiguous" regions of pixels, a group of pixels that are all neighbors, or neighbors of neighbors, etc., and useing these regions to trace lead curves; or selecting all pixels with similar color values or greyscale brightness to detect pixels that belong to the leads. 

The first approach was attempted during the exploratory phase of the project and was found to be too sensitive to noise for practical use. The second approach is, in all practical terms, already implented via the Otsu threshold selection method, which identifies the best threshold to separate the "black-like" pixels from any other grey noise in a greyscale image. This method works quite well! In summary, no action is needed.

## Auto-rotation bug fix

There is a bug with the automatic rotation feature that was mentioned during the presentation and peer groups recommended that this be fixed. The bug is due to the grid detection method used to estimate rotation angle depending on the image already having grid lines at 0 and 90 degrees (*d'oh!*). This will be fixed.

## User error feedback

> Could try to reduce noise if the user accidentally picks a section that does not have ECG data.

This feedback is not completely self-explanatory. If they meant that the application should correct noise in the user placing the lead bounding boxes by making minor correction, that is not feasible because the formatting of ECGs is too varied. If they meant that feedback to the user should be improved when the algorithms failed, this is being addressed.

## Automation and noise reduction

There were two comments related to expanding the use of automation and reducing the noise.

> Expand automation and reduce noise

> If they have time to use machine learning to convert cropped leads into signal that would be good.

Both of these goals are excellent. However, due to resource constraints, machine learning approaches are not currently feasible. Noise reduction is certainly achievable via more robust algorithms; these algorithms have already been developed and will be incorporated into the application.
