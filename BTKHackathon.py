import pandas as pd
from datetime import datetime
import schedule
import time

# Ödev verilerini saklamak için tablo yapısı
tasks = pd.DataFrame(columns=["Öğrenci Adı", "Görev Adı", "Açıklama", "Teslim Tarihi", "Tamamlandı Mı"])
students = {}  # Sınıf ve şube bazında öğrenciler

# Öğretmen doğrulama bilgileri
teachers = {"Miray": "123", "Leyla": "789"}

# Öğrenci verisi (örnek olarak)
students["10A"] = ["Ali", "Ayşe", "Mehmet"]
students["10B"] = ["Fatma", "Hasan", "Zeynep"]

# Öğretmen girişi
def teacher_login(username, password):
    if username in teachers and teachers[username] == password:
        print("Öğretmen girişi başarılı.")
        return True
    else:
        print("Giriş bilgileri hatalı.")
        return False

# Sınıf ve şube seçimi
def select_class_and_section():
    print("Lütfen sınıf ve şube girin (örneğin: 10A):")
    selected_class = input()
    if selected_class in students:
        print(f"{selected_class} sınıfındaki öğrenciler: {', '.join(students[selected_class])}")
        return selected_class
    else:
        print("Geçersiz sınıf. Lütfen tekrar deneyin.")
        return select_class_and_section()

# Ödev ekleme fonksiyonu
def add_task_for_student(task_name, description, due_date, student_name):
    global tasks
    new_task = {
        "Öğrenci Adı": student_name,
        "Görev Adı": task_name,
        "Açıklama": description,
        "Teslim Tarihi": due_date,
        "Tamamlandı Mı": False
    }
    tasks = pd.concat([tasks, pd.DataFrame([new_task])], ignore_index=True)
    print(f"'{task_name}' ödevi {student_name} için eklendi. Teslim tarihi: {due_date}")

# Ödev verme işlemi
def assign_homework(selected_class):
    print("Ödev adı girin:")
    task_name = input()
    print("Ödevin açıklamasını girin:")
    task_description = input()  # Ödev açıklaması için ek bilgi
    print("Teslim tarihini girin (YYYY-MM-DD formatında):")
    due_date = input()

    for student in students[selected_class]:
        print(f"{student} için ödev verilecek. Onaylıyor musunuz? (Evet/Hayır)")
        confirmation = input().lower()
        if confirmation == 'evet':
            add_task_for_student(task_name, task_description, due_date, student)

# Hatırlatma fonksiyonu
def reminder_for_students():
    global tasks
    today = datetime.now().strftime("%Y-%m-%d")
    for student in tasks["Öğrenci Adı"].unique():
        upcoming_tasks = tasks[(tasks["Öğrenci Adı"] == student) &
                               (tasks["Teslim Tarihi"] > today) &
                               (tasks["Tamamlandı Mı"] == False)]

        if not upcoming_tasks.empty:
            print(f"{student} için hatırlatmalar kontrol ediliyor...")
            for index, task in upcoming_tasks.iterrows():
                teslim_tarihi = datetime.strptime(task["Teslim Tarihi"], "%Y-%m-%d")
                kalan_sure = teslim_tarihi - datetime.now()
                kalan_gun = kalan_sure.days
                kalan_saat, kalan_dakika = divmod(kalan_sure.seconds, 3600)
                kalan_dakika //= 60  # kalan dakika hesaplama

                # Hatırlatma mesajı
                if kalan_gun <= 3:  # sadece 3 güne kadar olanları göster
                    print(f"Hatırlatma: {task['Görev Adı']} teslim tarihi yaklaşıyor! Kalan süre: {kalan_gun} gün, {kalan_saat} saat, {kalan_dakika} dakika ({student})")

# Programı başlatma
print("Ödev Takip Sistemi Başlatıldı...")

# Öğretmen girişi
username = input("Kullanıcı adınızı girin: ")
password = input("Parolanızı girin: ")

if teacher_login(username, password):
    selected_class = select_class_and_section()
    assign_homework(selected_class)

# Schedule hatırlatıcıyı her dakika çalıştır
schedule.every().minute.at(":00").do(reminder_for_students)

# Sonsuz döngü ile schedule'u başlat
while True:
    schedule.run_pending()
    time.sleep(14)

