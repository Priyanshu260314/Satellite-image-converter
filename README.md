# 🛰️ Satellite Image Converter

**A Flask-Based Web Application for Satellite Image Processing and Enhancement**

## 📌 About the Project

Satellite Image Converter & Enhancer is a web-based application developed using Python and Flask. It allows users to upload satellite images, process them using OpenCV, and view the enhanced results through a simple web interface.
The project demonstrates the practical application of image processing, database management, and web development.

## ✨ Features

- 📤 **Image Upload:** Upload satellite images from your local device.
- 🖼️ **Image Enhancement:** Process images using OpenCV.
- 🔄 **Before & After Comparison:** Compare original and enhanced images.
- 🏠 **Home Page:** Navigate through the main application features.
- 📊 **Dashboard:** Access available image-processing functionality.
- 🔐 **Login and Signup Pages:** User interface for account access.
- 🗄️ **Database Integration:** Store image records and upload timestamps using SQLite.
- 📁 **Multiple Image Formats:** Supports PNG, JPG, JPEG, BMP, and WEBP.
- 📱 **User-Friendly Interface:** Built using HTML, CSS, and JavaScript.

*Note: Features such as authentication, image downloads, and dashboard functionality depend on their implementation in the current version.*

## 🛠️ Technologies Used

| Python | Backend programming |
| Flask | Web application framework |
| Flask-SQLAlchemy | Database integration |
| OpenCV | Image processing |
| SQLite | Database storage |
| HTML| Web page structure |
| CSS | Styling and layout |
| JavaScript | Frontend interactions |

## 📂 Project Structure

Satellite-Image-Converter/
│
├── app.py
├── image.db
│
├── templates/
│   ├── index.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── about.html
│   └── help.html
│
└── static/
    ├── input/
    ├── output/



*Note: This is the expected structure. Keep the folder and file names consistent with your actual project.*

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- A web browser
- Git (optional)

### Step 1: Clone the Repository

Replace the example URL with your actual GitHub repository URL.

git clone https://github.com/Priyanshu260314/Satellite-image-converter.git

Move into the project folder:

cd Satellite-Image-Converter

Alternatively, download the repository ZIP file and extract it.

### Step 2: Install Dependencies
 install the main dependencies:

pip install Flask Flask-SQLAlchemy opencv-python


### Step 3: Run the Application

```bash
python app.py
```

Open your browser and visit:

**http://127.0.0.1:5000/**

If your application uses a different port, open the local URL shown in your terminal.

## 🚀 How to Use

1. Start the Flask application.
2. Open the application in your browser.
3. Navigate to the home page or dashboard.
4. Upload a satellite image in a supported format.
5. Process the uploaded image.
6. View the original and enhanced results.

## 🖼️ Screenshots

Add screenshots of your actual application to showcase its interface.

### Original Image

<img width="299" height="168" alt="images" src="https://github.com/user-attachments/assets/4b32d61e-3865-475b-ab5a-475290ac44cc" />


### Enhanced Image

<img width="1920" height="1020" alt="Screenshot 2026-10-13 221218" src="https://github.com/user-attachments/assets/7447b4d3-a4d6-439e-98f7-cb7f5c0a17fe" />


To display these screenshots on GitHub, create a `screenshots` folder in your repository and upload the corresponding image files.

## 🗄️ Database

The application uses SQLite with Flask-SQLAlchemy to manage image records.

The image record model can contain:

- Image ID
- Original filename
- Enhanced filename
- Upload timestamp

Image files are stored in the configured input and output folders, while the database stores their associated metadata.

## 🔬 Image Processing

OpenCV is used to process uploaded satellite images and improve their visual appearance, depending on the enhancement techniques implemented in the application.

**Note:** Visual enhancement is not the same as increasing the actual spatial resolution of an image. AI-based super-resolution would require a dedicated algorithm or model.

## 🎯 Project Objectives

- Develop a Python-based image-processing web application.
- Understand image processing with OpenCV.
- Integrate Flask with an SQLite database.
- Build a user-friendly interface.
- Explore image enhancement techniques for satellite imagery.

## 🔮 Future Enhancements

- AI-based satellite image super-resolution.
- Interactive before-and-after comparison.
- Improved user authentication.
- Image quality evaluation using PSNR and SSIM.

## ⚠️ Limitations

- Enhancement quality depends on the input image and the processing algorithm.
- The application runs locally unless deployed to a server.

⭐ If you find this project useful, consider giving the repository a star on GitHub.
