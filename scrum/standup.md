## November 7, 2020


### Natalie

#### Since last meeting

- UML Diagram and planned architecture of the backend.
- Trained on Qt Designer.

#### Until next meeting

- Figure out how to select files in pyqt
- Maybe figure out how to display the image

#### Blockers

None.

### Julian

#### Since last meeting

- Emailed Scott about server access. Emailed IT about server access.
- Created `.txt` visualizer.

#### Until next meeting

- Polish the `.txt` viewer.
- Work on making a right panel to edit properties.

#### Blockers

None.



## November 11


### Natalie

#### Since last meeting

- File chooser and displaying and image.
- MVC refactoring.

#### Until next meeting

- Get controller working.
- Taking over as Scrum master.

#### Blockers

None.


### Julian

#### Since last meeting

- Creating editor panel GUI.

#### Until next meeting

- Refactoring GUI code.
- Polishing side panel GUI.

#### Blockers

None.


## November 19

### Natalie

#### Since last meeting

- Narrowed down our options for displaying images and bounding boxes

#### Until next meeting

- Implement image viewer and bounding boxes

#### Blockers

None.


### Julian

#### Since last meeting

- Wrote the QtWrapper library to make nested Qt code
- Made an icon for the project
- Researched singletons in python

#### Until next meeting

- Extending the wrapper to more things and refactor editor to use it
- Get everything running on Linux

#### Blockers

None.


## November 21

### Natalie

#### Since last meeting

- Created moveable/resizeable bounding boxes

#### Until next meeting

- Figure out the size grips for the bounding boxes / other possible approaches

#### Blockers

None.


### Julian

#### Since last meeting

- Figured out how to zoom and pan images (and watched Ratatouille)

#### Until next meeting

- Incorporate QGraphicScence into the codebase and also research other possible bounding box approaches

#### Blockers

None.


## November 25 - CANCELED


## November 28

### Natalie

#### Since last meeting

- Integrated new image view and bounding box code into existing editor widget

#### Until next meeting

- Figure out how to restrict bounding box to image view canvas
- Look into adding zoom in/out functionality (pinching, ctrl-scroll, and/or buttons)

#### Blockers

None.


### Julian

#### Since last meeting

- Implemented new image view and bounding box code and figured out way to zoom in and out of image
- Researched licenses

#### Until next meeting

- Refactor code
- Add comments and type suggestions
- Fixed import modules

#### Blockers

None.

## December 2

### Natalie

#### Since last meeting

- Worked on Fall Restrospective

#### Until next meeting

- Figure out how to restrict bounding box to image view canvas
- Look into adding zoom in/out functionality (pinching, ctrl-scroll, and/or buttons)

#### Blockers

None.


### Julian

#### Since last meeting

- Worked on Fall Restrospective
- Made demo video of our progress

#### Until next meeting

- Refactor code
- Add comments and type suggestions
- Fixed import modules

#### Blockers

None.


## January 7 

### Natalie

#### Since last meeting

- Added mouse support for `ImageView`.

#### Until next meeting

- Work on zoom UI.

#### Blockers

None.


### Julian

#### Since last meeting

- Added static type checking via `mypy`.

#### Until next meeting

- Add comments and types, and refactor more UI code

#### Blockers

None.


## January 11

### Natalie

#### Since last meeting

- Zoom in and out with shortcuts (ctrl+'+', ctrl+'-').
- Zoom increments are standardized.

#### Until next meeting

- Implement functionality to isolate the pixels inside the bounding box.

#### Blockers

None.


### Julian

#### Since last meeting

- Augmented QtWrapper.
- Started to create file for demo-ing UI components.

#### Until next meeting

- Continuing QTWrapper.
- Editing the image and live reload.

#### Blockers

None.

## January 16

### Natalie

#### Since last meeting

- Mapped bounding box coordinates to imageview coordinates

#### Until next meeting

- Restrict bounding box movement within graphics view
- Don't let bounding box fold in on itself
- Try to extract portion of image within bounding box (ignoring zoom/resizing events for now)

#### Blockers

None.


### Julian

#### Since last meeting

- Researched QGraphicsView stuff
- Refactored paint function for ROI
- Created a plan for executing live reloading of the image

#### Until next meeting

- Finish refactoring editor UI

#### Blockers

None.



## January 20

### Natalie

#### Since last meeting

- Progress with mapping bounding box coordinates to get the correct coordinates in image-space.

#### Until next meeting

- Restrict bounding box movement within graphics view.
- Don't let bounding box fold in on itself.
- Try to extract portion of image within bounding box (ignoring zoom/resizing events for now).

#### Blockers

None.


### Julian

#### Since last meeting

- Refactoring editor UI.
- Live image editing.

#### Until next meeting

- Pull conversion functionality into own file.
- Learn about signals (write up).
- Keep going with live reloading.
- Finish refactoring editor UI.

#### Blockers

None.


## January 25

### Natalie

#### Since last meeting

- Extracts sub-image from within bounding box!!
- Bounding box doesn't turn inside out and won't go outside the image!!

#### Until next meeting

- Cleaning up branch to merge to master.
- Fixing automic resizing bug.

#### Blockers

None.


### Julian

#### Since last meeting

- Image edits! (contrast, brightness, rotation)

#### Until next meeting

- Polish and merge image edits.
- Learn about signals (write up).
- Finish refactoring editor UI.

#### Blockers

None.

## February 2

### Natalie

#### Since last meeting

- Trying to fix bugs when restricting bounding box movement

#### Until next meeting

- Create button to add new bounding boxes for each lead

#### Blockers

None.


### Julian

#### Since last meeting

- Finished editor UI refactor
- Polished controls

#### Until next meeting

- Image processing framework 

#### Blockers

None.

## February 10

### Natalie

#### Since last meeting

- Created menu bar buttons/shortcuts to add lead bounding boxes

#### Until next meeting

- Finish up the add lead buttons and merge to master

#### Blockers

None.


### Julian

#### Since last meeting

- Started implementing caching framework for image rotation/color

#### Until next meeting

- Start implementing functionality from literature reviews

#### Blockers

None.



## February 16

### Natalie

#### Since last meeting

- Cracked the problem of restricting bounding box movement **with** resizing!

#### Until next meeting

- Restrict the bounding box during resizing.

#### Blockers

None.


### Julian

#### Since last meeting

- Made some test images using the app to aid in developing extraction algorithms.

#### Until next meeting

- Start implementing signal extraction algorithms.

#### Blockers

None.


## February 19

### Natalie

#### Since last meeting

- Fixed bounding boxes so they stay inside image even with resizing!

#### Until next meeting

- Planning out detail and look into zoom stuff!

#### Blockers

None.


### Julian

#### Since last meeting

- Implemented Mallarachi, 2014 binarization and a basic extraction algorithm.

#### Until next meeting

- Implement grid extraction, maybe plan out the whole conversion process.

#### Blockers

None.


## February 24

### Natalie

#### Since last meeting

- Fixed zooming issues on window resizing
- Bounding box changes colors when selected/deselected
- Refactored ROIItem our of ImageView
- Added offset to image capturing to grab data from inside lines of the box

#### Until next meeting

- Designing the editor panel

#### Blockers

None.


### Julian

#### Since last meeting

- Implementing a new, more robust, way to extract the signal

#### Until next meeting

- Finish the robust stuff
- Write algorithm to detect size of grid

#### Blockers

None.


## February 28

### Natalie

#### Since last meeting

- Designed and started implementing global and lead-specific editor panels

#### Until next meeting

- A lot of code refactoring

#### Blockers

None.


### Julian

#### Since last meeting

- Finished algorithm but wasn't robust - not worth spending more time on
- Researched a class of algorithm called "snakes"
- Got grid detection algorithm working

#### Until next meeting

- More grid detection scaling

#### Blockers

None.


## March 5

### Natalie

#### Since last meeting

- Added detail panel
- Fixed grab handles
- Highlights active bounding box in red

#### Until next meeting

- Connecting UI to image processing

#### Blockers

None.


### Julian

#### Since last meeting

- Architected extraction process
- ECGToolkit refactor
- Implemented grid size extraction

#### Until next meeting

- Create function for integrating the grid size and the signal array to create scaled signal.
- Create baseline selection function.
- Output to file.

#### Blockers

None.


## April 5

### Natalie

#### Since last meeting

- Created ECG and lead model model classes
- Added Digitize button 

#### Until next meeting

- Create interface to save output file

#### Blockers

None.


### Julian

#### Since last meeting

- Started writing code to turn stuff into signal

#### Until next meeting

- Finish the function and incorporate ECG model

#### Blockers

None.


## April 12

### Natalie

#### Since last meeting

- Made ECG signal export interface to select file
- Refactored ECGModel

#### Until next meeting

- Rename `ECGModel` -> `ECG`

#### Blockers

Busy with other classes this week!


### Julian

#### Since last meeting

- Implemented functions to convert ecg cropped images to signals and output to file.

#### Until next meeting

- Make ticket to handle output file path corner cases.
- Connect the interface to the implementations (above).

#### Blockers

None.

