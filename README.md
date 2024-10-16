# FotoFilter

## About the Project
**FotoFilter** is an AI-powered Flask application designed to help users filter and manage large collections of images. Utilizing advanced algorithms for face detection, blur detection, and similarity detection, FotoFilter allows users to easily identify and sort images based on content quality and uniqueness.

## Features
- **Face Detection**: Identify images containing faces.
- **Blur Detection**: Find and filter out blurry images.
- **Similarity Detection**: Detect and group similar images to reduce redundancy.
- **Interactive Web Interface**: Simple and responsive web interface for easy operation.

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
What you need to install the software:
- Python 3.9
- pip (Python package installer)

### Installation
1. **Clone the Repository**
   git clone https://github.com/rs2070/FotoFilter.git
   cd FotoFilter

2. **Set Up a Virtual Environment**
   - For macOS and Linux:
     python3 -m venv venv
     source venv/bin/activate

   - For Windows:
     python -m venv venv
     .\venv\Scripts\activate

3. **Install Required Packages**
   pip install -r requirements.txt

### Running the Application
After installation, you can run the application using Flask's built-in server.
-flask run

This will start the Flask server on `http://127.0.0.1:5000/`, and you can navigate to this address in your web browser to interact with the application.

Once the application is running, navigate to the homepage. You can upload images via the interface and use the provided tools to analyze and filter your image dataset. Results are displayed on the results page where you can download filtered sets or individual images.

## Contact
Rahul Sankaralingam - https://www.linkedin.com/in/rahul-sankaralingam/ - rsm4597@gmail.com

Project Link: [https://github.com/rs2070/FotoFilter](https://github.com/rs2070/FotoFilter)
