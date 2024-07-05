# Video Synopsis Application

## Overview

This project is a video synopsis application that detects and tracks objects in a video, segments periods of activity, clusters similar events, and generates a summarized video. The goal is to condense lengthy surveillance footage into a short, informative video that highlights key events.

## Features

- **Motion Detection**: Detects objects in the video using motion detection algorithms.
- **Object Tracking**: Tracks detected objects across frames using robust tracking algorithms.
- **Temporal Segmentation**: Identifies and segments periods of significant activity in the video.
- **Event Clustering**: Groups similar events together to avoid redundancy.
- **Summary Generation**: Generates a concise video synopsis by stitching together key segments.

## Installation

### Prerequisites

- Python 3.6+
- OpenCV
- Numpy
- MoviePy
- Scikit-Learn

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Umayanga12/Video-synopsis-App.git
   cd video-synopsis-App
   ```

2. **Create a virtual environment and activate it:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Motion Detection and Object Tracking

1. **Run the motion detection and object tracking:**

   ```bash
   python motion_detection_tracking.py --input path_to_video --output path_to_output
   ```

2. **Customize the motion detection and tracking parameters as needed in `motion_detection_tracking.py`.**

### Temporal Segmentation and Event Clustering

1. **Run the temporal segmentation and event clustering:**

   ```bash
   python temporal_segmentation_clustering.py --input path_to_video --output path_to_output
   ```

2. **Customize the segmentation and clustering parameters as needed in `temporal_segmentation_clustering.py`.**

### Summary Generation

1. **Generate the video synopsis:**

   ```bash
   python generate_synopsis.py --input path_to_video --output path_to_output
   ```

2. **Customize the summary generation parameters as needed in `generate_synopsis.py`.**

2. **Interact with the application through the provided UI.**

## Project Structure

```
video-synopsis-application/
│
├── motion_detection_tracking.py    # Motion detection and object tracking script
├── temporal_segmentation_clustering.py  # Temporal segmentation and event clustering script
├── generate_synopsis.py            # Video synopsis generation script
├── requirements.txt                # List of dependencies
└── README.md                       # Project README
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenCV](https://opencv.org/)
- [MoviePy](https://zulko.github.io/moviepy/)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [Scikit-Learn](https://scikit-learn.org/)
