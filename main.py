import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import threading
import numpy as np

# قاعدة بيانات التحاليل
analyses_data = {
    "Glucose": {
        "name_ar": "تحليل السكر",
        "name_en": "Glucose Test",
        "info_ar": "قياس نسبة الجلوكوز في الدم لتشخيص السكري أو مقدمات السكري.",
        "info_en": "Measures the glucose level in blood to diagnose diabetes or prediabetes.",
        "symptoms_ar": "زيادة العطش، التبول المتكرر، فقدان الوزن غير المبرر.",
        "symptoms_en": "Increased thirst, frequent urination, unexplained weight loss.",
        "normal_range_ar": "السكر الصائم: أقل من 100 مجم/ديسيلتر",
        "normal_range_en": "Fasting glucose: Less than 100 mg/dL"
    },
    "Cholesterol": {
        "name_ar": "تحليل الكوليسترول",
        "name_en": "Cholesterol Test",
        "info_ar": "قياس مستوى الكوليسترول في الدم لتقييم خطر الإصابة بأمراض القلب.",
        "info_en": "Measures cholesterol levels in the blood to assess the risk of heart disease.",
        "symptoms_ar": "آلام في الصدر، ضيق في التنفس، التعب المستمر.",
        "symptoms_en": "Chest pain, shortness of breath, constant fatigue.",
        "normal_range_ar": "الحد الطبيعي: أقل من 200 مجم/ديسيلتر",
        "normal_range_en": "Normal range: Less than 200 mg/dL"
    },
    "Triglycerides": {
        "name_ar": "تحليل الدهون الثلاثية",
        "name_en": "Triglycerides Test",
        "info_ar": "قياس مستوى الدهون الثلاثية في الدم لتقييم صحة القلب.",
        "info_en": "Measures triglyceride levels in the blood to assess heart health.",
        "symptoms_ar": "زيادة الوزن، الدوخة، ارتفاع ضغط الدم.",
        "symptoms_en": "Weight gain, dizziness, high blood pressure.",
        "normal_range_ar": "الحد الطبيعي: أقل من 150 مجم/ديسيلتر",
        "normal_range_en": "Normal range: Less than 150 mg/dL"
    },
    "Blood Pressure": {
        "name_ar": "تحليل ضغط الدم",
        "name_en": "Blood Pressure Test",
        "info_ar": "قياس ضغط الدم لتحديد إذا كان الشخص يعاني من ارتفاع أو انخفاض في ضغط الدم.",
        "info_en": "Measures blood pressure to determine if a person has high or low blood pressure.",
        "symptoms_ar": "الصداع، الدوار، نزيف الأنف.",
        "symptoms_en": "Headaches, dizziness, nosebleeds.",
        "normal_range_ar": "الحد الطبيعي: 120/80 مم زئبق",
        "normal_range_en": "Normal range: 120/80 mmHg"
    },
    "Liver Function": {
        "name_ar": "تحليل وظائف الكبد",
        "name_en": "Liver Function Test",
        "info_ar": "قياس مستويات الإنزيمات في الدم لتقييم صحة الكبد.",
        "info_en": "Measures enzyme levels in the blood to assess liver health.",
        "symptoms_ar": "اليرقان، التعب الشديد، آلام في البطن.",
        "symptoms_en": "Jaundice, extreme fatigue, abdominal pain.",
        "normal_range_ar": "الحد الطبيعي: مستويات إنزيمات الكبد يجب أن تكون في حدود معينة.",
        "normal_range_en": "Normal range: Liver enzymes should be within certain limits."
    },
    "Kidney Function": {
        "name_ar": "تحليل وظائف الكلى",
        "name_en": "Kidney Function Test",
        "info_ar": "قياس مستويات المواد في الدم لتقييم صحة الكلى.",
        "info_en": "Measures levels of substances in the blood to assess kidney health.",
        "symptoms_ar": "تورم القدمين، قلة التبول، التعب.",
        "symptoms_en": "Swelling of the feet, reduced urination, fatigue.",
        "normal_range_ar": "الحد الطبيعي: مستويات الكرياتينين في الدم يجب أن تكون أقل من 1.2 مجم/ديسيلتر.",
        "normal_range_en": "Normal range: Blood creatinine levels should be less than 1.2 mg/dL."
    },
    "Vitamin D": {
        "name_ar": "تحليل فيتامين د",
        "name_en": "Vitamin D Test",
        "info_ar": "قياس مستوى فيتامين د في الدم لتقييم الصحة العامة.",
        "info_en": "Measures the vitamin D level in the blood to assess general health.",
        "symptoms_ar": "آلام في العظام، ضعف العضلات، التعب.",
        "symptoms_en": "Bone pain, muscle weakness, fatigue.",
        "normal_range_ar": "الحد الطبيعي: 20-50 نانوغرام/مل.",
        "normal_range_en": "Normal range: 20-50 ng/mL."
    },
    "Hemoglobin": {
        "name_ar": "تحليل الهيموجلوبين",
        "name_en": "Hemoglobin Test",
        "info_ar": "قياس مستوى الهيموجلوبين في الدم لتحديد وجود الأنيميا.",
        "info_en": "Measures hemoglobin levels in the blood to diagnose anemia.",
        "symptoms_ar": "الدوخة، التعب، شحوب البشرة.",
        "symptoms_en": "Dizziness, fatigue, pale skin.",
        "normal_range_ar": "الحد الطبيعي: 13-17 جم/ديسيلتر.",
        "normal_range_en": "Normal range: 13-17 g/dL."
    },
    "Calcium": {
        "name_ar": "تحليل الكالسيوم",
        "name_en": "Calcium Test",
        "info_ar": "قياس مستوى الكالسيوم في الدم لتقييم صحة العظام والأسنان.",
        "info_en": "Measures calcium levels in the blood to assess bone and dental health.",
        "symptoms_ar": "تشنجات عضلية، ألم في العظام.",
        "symptoms_en": "Muscle cramps, bone pain.",
        "normal_range_ar": "الحد الطبيعي: 8.5-10.2 مجم/ديسيلتر.",
        "normal_range_en": "Normal range: 8.5-10.2 mg/dL."
    },
    "Magnesium": {
        "name_ar": "تحليل المغنيسيوم",
        "name_en": "Magnesium Test",
        "info_ar": "قياس مستوى المغنيسيوم في الدم لتقييم توازن المعادن.",
        "info_en": "Measures magnesium levels in the blood to assess mineral balance.",
        "symptoms_ar": "التعب، التشنجات العضلية.",
        "symptoms_en": "Fatigue, muscle cramps.",
        "normal_range_ar": "الحد الطبيعي: 1.7-2.2 مجم/ديسيلتر.",
        "normal_range_en": "Normal range: 1.7-2.2 mg/dL."
    },
    "Iron": {
        "name_ar": "تحليل الحديد",
        "name_en": "Iron Test",
        "info_ar": "قياس مستوى الحديد في الدم لتحديد وجود الأنيميا.",
        "info_en": "Measures iron levels in the blood to diagnose anemia.",
        "symptoms_ar": "التعب، شحوب الجلد، ضيق التنفس.",
        "symptoms_en": "Fatigue, pale skin, shortness of breath.",
        "normal_range_ar": "الحد الطبيعي: 60-170 ميكروغرام/ديسيلتر.",
        "normal_range_en": "Normal range: 60-170 mcg/dL."
    },
    "Thyroid": {
        "name_ar": "تحليل الغدة الدرقية",
        "name_en": "Thyroid Function Test",
        "info_ar": "قياس مستويات هرمونات الغدة الدرقية في الدم لتقييم عمل الغدة الدرقية.",
        "info_en": "Measures thyroid hormone levels in the blood to assess thyroid function.",
        "symptoms_ar": "زيادة الوزن، التعب، تغيرات في المزاج.",
        "symptoms_en": "Weight gain, fatigue, mood changes.",
        "normal_range_ar": "الحد الطبيعي: 0.4-4.0 ميكرومتر/لتر.",
        "normal_range_en": "Normal range: 0.4-4.0 µU/mL."
    },
    "C-Reactive Protein": {
        "name_ar": "تحليل البروتين التفاعلي C",
        "name_en": "C-Reactive Protein Test",
        "info_ar": "مؤشر لوجود التهاب في الجسم.",
        "info_en": "An indicator of inflammation in the body.",
        "symptoms_ar": "الحمى، الألم، التورم.",
        "symptoms_en": "Fever, pain, swelling.",
        "normal_range_ar": "الحد الطبيعي: أقل من 3 ملغ/لتر.",
        "normal_range_en": "Normal range: Less than 3 mg/L."
    },
    "Blood Sugar": {
        "name_ar": "تحليل البروتين التفاعلي C",
        "name_en": "C-Reactive Protein Test",
        "info_ar": "مؤشر لوجود التهاب في الجسم.",
        "info_en": "An indicator of inflammation in the body.",
        "symptoms_ar": "الحمى، الألم، التورم.",
        "symptoms_en": "Fever, pain, swelling.",
        "normal_range_ar": "الحد الطبيعي: أقل من 3 ملغ/لتر.",
        "normal_range_en": "Normal range: Less than 3 mg/L."}
}

def open_camera_screen(root):
    # Clear the screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create the camera screen
    camera_screen = tk.Frame(root)
    camera_screen.pack(fill="both", expand=True)

    tk.Label(camera_screen, text="Camera Feed", font=("Helvetica", 18)).pack(pady=10)

    # Canvas to show the camera feed
    camera_canvas = tk.Canvas(camera_screen, width=640, height=480)
    camera_canvas.pack()

    # Frame for buttons
    button_frame = tk.Frame(camera_screen)
    button_frame.pack(pady=10)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            # Convert OpenCV frame to PIL image for Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            img_tk = ImageTk.PhotoImage(img)
            camera_canvas.img_tk = img_tk  # Keep reference
            camera_canvas.create_image(0, 0, anchor="nw", image=img_tk)

        if not stop_camera:
            root.after(10, update_frame)

    def capture_image():
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                file_path = "captured_image.jpg"
                cv2.imwrite(file_path, frame)
                cap.release()
                cv2.destroyAllWindows()
                stop_camera_feed()
                show_image_screen(root, file_path)

    
    def stop_camera_feed():
        nonlocal stop_camera
        stop_camera = True
        cap.release()
        cv2.destroyAllWindows()
        show_analysis_screen(language)
        # show_analysis_screen(root)

    # Buttons
    tk.Button(button_frame, text="Capture Image", font=("Helvetica", 12), command=capture_image).pack(side="left", padx=10)
    tk.Button(button_frame, text="Close Camera", font=("Helvetica", 12), command=stop_camera_feed).pack(side="left", padx=10)

    # Open the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Unable to access the camera.")
        show_analysis_screen(root)
        return

    stop_camera = False
    update_frame()

def show_image_screen(root, image_path):
    # Clear the screen
    for widget in root.winfo_children():
        widget.destroy()

    # Create a screen for displaying the image
    image_screen = tk.Frame(root)
    image_screen.pack(fill="both", expand=True)

    # tk.Label(image_screen, text="Captured Image", font=("Helvetica", 18)).pack(pady=10)

    # Display the image
    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)
    img_label = tk.Label(image_screen, image=img_tk)
    img_label.image = img_tk  
    tk.Label(image_screen, text="This feature is under development and is not functional yet.", bg= "red", font= 20).pack(pady=10)
    img_label.pack(pady=10)

    # Button to return to the analysis screen
    tk.Button(image_screen, text="Return to Analysis", font=("Helvetica", 14), command=lambda: show_analysis_screen(language)).pack(pady=5)

# ------------------- Language Screen ---------------------------#
# Language Screen 
def show_language_screen():
    for widget in root.winfo_children():
        widget.destroy()

    language_screen = tk.Frame(root)
    language_screen.pack(fill="both", expand=True)

    language_label = tk.Label(language_screen, text="اختر اللغة" if language == "ar" else "Choose Language", font=("Helvetica", 18))
    language_label.pack(pady=20)

    ar_button = tk.Button(language_screen, text="العربية", font=("Helvetica", 16), command=lambda: show_analysis_screen("ar"))
    en_button = tk.Button(language_screen, text="English", font=("Helvetica", 16), command=lambda: show_analysis_screen("en"))

    ar_button.pack(pady=10)
    en_button.pack(pady=10)

# ----------------- Analysis info pop ---------------------- # 
def show_analysis_info(analysis_type, language):
    data = analyses_data.get(analysis_type, {})
    if not data:
        messagebox.showerror("Error", "Invalid analysis data")
        return

    if f"name_{language}" not in data:
        messagebox.showerror("Error", f"Invalid language: {language}")
        return

    name = data[f"name_{language}"]
    data = analyses_data[analysis_type]
    name = data[f"name_{language}"]
    info = data[f"info_{language}"]
    symptoms = data[f"symptoms_{language}"]
    normal_range = data[f"normal_range_{language}"]

    # Create a popup window for details
    popup = tk.Toplevel()
    popup.title(name)
    popup.geometry("500x400")
    popup.resizable(False, False)

    # Display analysis info
    tk.Label(popup, text=name, font=("Helvetica", 16, "bold")).pack(pady=10)
    tk.Label(popup, text=info, wraplength=450, justify="left", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(popup, text=f"Symptoms: {symptoms}", wraplength=450, justify="left", font=("Helvetica", 12)).pack(pady=5)
    tk.Label(popup, text=f"Normal Range: {normal_range}", font=("Helvetica", 12)).pack(pady=5)

    # Display image if available
    image_path = data.get("image_path")
    if image_path:
        try:
            image = Image.open(image_path)
            image = image.resize((200, 150), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(image)
            img_label = tk.Label(popup, image=img)
            img_label.image = img  
            img_label.pack(pady=10)
        except Exception as e:
            print(f"Error loading image: {e}")

    # Input field for user's test result
    tk.Label(popup, text="Enter your test result:", font=("Helvetica", 12)).pack(pady=5)
    result_entry = tk.Entry(popup, font=("Helvetica", 12))
    result_entry.pack(pady=5)
    def check_result():
        try:
            result = float(result_entry.get())
            if language == "ar" and "أقل من" in normal_range:
                threshold = float(normal_range.split()[-2])
                if result < threshold:
                    message = "النتيجة ضمن المعدل الطبيعي."
                else:
                    message = "النتيجة أعلى من المعدل الطبيعي. يرجى استشارة الطبيب."
            elif language == "en" and "less than" in normal_range.lower():
                threshold = float(normal_range.split()[-2])
                if result < threshold:
                    message = "Your result is within the normal range."
                else:
                    message = "Your result is above the normal range. Please consult a doctor."
            else:
                message = (
                    "يرجى مقارنة النتيجة يدويًا بالنطاق المحدد."
                    if language == "ar"
                    else "Please manually compare your result with the provided range."
                )
            messagebox.showinfo("نتيجة الفحص" if language == "ar" else "Result Check", message)
        except ValueError:
            messagebox.showerror(
                "خطأ في الإدخال" if language == "ar" else "Input Error",
                "يرجى إدخال رقم صحيح." if language == "ar" else "Please enter a valid number."
            )


    check_button = tk.Button(popup, text="Check Result", command=check_result, font=("Helvetica", 12))
    check_button.pack(pady=10)

    # Close button
    close_button = tk.Button(popup, text="Close", command=popup.destroy, font=("Helvetica", 12))
    close_button.pack(pady=10)

# ----------------- Analysis Screen ----------------------- # 
def show_analysis_screen(language):
    for widget in root.winfo_children():
        widget.destroy()

    analysis_screen = tk.Frame(root)
    analysis_screen.pack(fill="both", expand=True)

    tk.Label(
        analysis_screen, 
        text="التحاليل" if language == "ar" else "Analyses",
        font=("Helvetica", 18, "bold")
    ).pack(pady=10)

    analyses = list(analyses_data.keys())

    # Create a grid for buttons
    button_frame = tk.Frame(analysis_screen)
    button_frame.pack(pady=20)

    # Adjust layout for three columns
    for index, analysis in enumerate(analyses):
        analysis_name = analyses_data[analysis]["name_ar"] if language == "ar" else analyses_data[analysis]["name_en"]
        analysis_button = tk.Button(
            button_frame,
            text=analysis_name,
            font=("Helvetica", 14),
            command=lambda a=analysis: show_analysis_info(a, language),
            width=20,
            height=2
        )
        analysis_button.grid(row=index // 3, column=index % 3, padx=20, pady=10)

    # Button to capture an image
    capture_button = tk.Button(
        analysis_screen,
        text="إلتقط صورة" if language == "ar" else "Capture Image",
        font=("Helvetica", 14),
        command=lambda: open_camera_screen(root),
        bg="lightblue",
        fg="black",
        width=25,
        height=2
    )

    capture_button.pack(pady=20)

# First screen 
def show_welcome_screen():
    global language
    welcome_screen = tk.Frame(root, bg="lightblue")
    welcome_screen.pack(fill="both", expand=True)

    welcome_msg = "مرحباً بك في تطبيق طمني" if language == "ar" else "Welcome to To'meni App"
    welcome_label = tk.Label(welcome_screen, text=welcome_msg, font=("Helvetica", 24, "bold"), bg="lightblue")
    welcome_label.pack(pady=50)

    root.after(3000, lambda: show_language_screen())

# --------------------------------------------------------#
if __name__ == "__main__":
    root = tk.Tk()
    root.title("To'meni App")
    root.geometry("800x600")
    language = "ar"  # Default language
    show_welcome_screen()
    root.mainloop()
