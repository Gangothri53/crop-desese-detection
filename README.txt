 🌱 Sustainable Crop Disease Detection

A Flask-based web application that detects crop diseases from leaf images and provides actionable solutions, supporting English and Telugu languages with PDF reports and audio guidance.  


Features Implemented
1. Leaf Image Upload 
   - Users can upload an image of a leaf through an attractive, green-themed interface.  
   - Optional voice input is supported for users who cannot type.  
2. Disease Prediction (Placeholder) 
   - Detects diseases like Leaf Blight, Powdery Mildew, or Healthy leaves.  
   - Shows disease name and confidence percentage.  

3. PDF Report Generation 
   - Generates a PDF report dynamically containing:  
     - Leaf image  
     - Predicted disease and confidence  
     - Recommended solutions in English + Telugu  
   - Proper Telugu font rendering included.  

4. Audio Reports 
   - Generates voice narration of the disease report in English and Telugu using `gTTS`.  
   - Audio can be played directly from the results page.  

5. Download and Navigation 
   - Downloadable PDF report  
   - Audio playback controls  
   - Option to upload another image from the results page.  

6. Frontend Design  
   - Green-themed, clean, and responsive UI using HTML/CSS.  
   - Animated upload card with modern styling for better user experience.  
Technology Stack

- Backend: Python, Flask  
- PDF Generation:ReportLab  
- Voice Generation:gTTS (Google Text-to-Speech)  
- Frontend: HTML, CSS, Google Fonts  
-Languages Supported: English and Telugu  

Folder Structure

crop_disease_detection/
│
├── app/
│ ├── app.py
│ ├── NotoSansTelugu-Regular.ttf
│ └── templates/
│ ├── index.html
│ └── result.html
│
├── uploads/ # Temporary uploaded leaf images
├── reports/ # Generated PDF reports
├── static/
│ └── audio/ # Generated audio files
└── README.md
