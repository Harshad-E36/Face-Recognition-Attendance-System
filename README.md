# Face Recognition System

A Django-based Face Recognition System that allows user registration via webcam capture and recognizes previously registered users. This project utilizes OpenCV and the `face_recognition` library for face encoding and detection.

## Features

- **User Registration**: Register new users using their face and name.
- **Face Recognition**: Identify registered users in real time.
- **Database Storage**: Store face encodings and user details in a database.
- **Detection Logs**: Maintain a record of detected faces with timestamps.
- **Webcam Integration**: Capture user images directly from the browser.
- **AJAX-based Form Submission**: Enhance user experience with real-time feedback.

## Technologies Used

- **Django** – Python framework for backend development
- **OpenCV** – Image processing
- **face_recognition** – Face encoding and recognition
- **Bootstrap** – Frontend styling
- **jQuery & AJAX** – Dynamic UI interactions
- **SQLite** – Default Django database

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/FaceRecognitionDjango.git
cd FaceRecognitionDjango
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py migrate
```

### 5. Run the Development Server

```bash
python manage.py runserver
```

### 6. Access the Application

Open your browser and go to:

```
http://127.0.0.1:8000/
```

## Project Structure

```
FaceRecognitionDjango/
│── app/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   │   ├── index.html
│   │   ├── registration.html
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│── FaceRecognitionDjango/
│── manage.py
│── requirements.txt
│── README.md
```

## API Endpoints

| Endpoint           | Method | Description                           |
|-------------------|--------|---------------------------------------|
| `/`               | GET    | Home page                            |
| `/registration/`  | GET    | User registration page               |
| `/submit_form/`   | POST   | Handles new user registration        |
| `/process_frame/` | POST   | Processes frames for face recognition |
| `/get_detections/` | GET    | Fetches detected faces data          |

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss proposed modifications.

## Contact

For any issues or inquiries, feel free to reach out via GitHub Issues.

---

**Developed by Harshad Kshirsagar.**

