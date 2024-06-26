import sys
import random
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
                             QPushButton, QRadioButton, QButtonGroup, QMessageBox, QMenuBar, QMenu, QAction)
from PyQt5.QtGui import QIcon

# Load QUESTIONS from data.json
try:
    with open('data.json', 'r', encoding='utf-8') as f:
        QUESTIONS = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading data.json: {e}")
    QUESTIONS = {}

# Load DISTRACTORS from false.json
try:
    with open('false.json', 'r', encoding='utf-8') as f:
        DISTRACTORS = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error loading false.json: {e}")
    DISTRACTORS = {}

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.num_questions = 0
        self.questions = []
        self.current_question = 0
        self.num_correct = 0
        self.user_name = ""
        

        self.initUI()

    def initUI(self):
        self.setMinimumSize(800, 600)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        self.menu_bar = QMenuBar(self)
        self.file_menu = QMenu("File", self)
        self.menu_bar.addMenu(self.file_menu)

        self.score_menu = QMenu("Score", self)
        self.menu_bar.addMenu(self.score_menu)

        icon = QIcon('/mnt/data/image.png')

        self.start_action = QAction(icon, "Start", self)
        self.start_action.triggered.connect(self.show_start_menu)
        self.file_menu.addAction(self.start_action)

        self.about_action = QAction(icon, "About App", self)
        self.about_action.triggered.connect(self.show_about)
        self.file_menu.addAction(self.about_action)

        self.quit_action = QAction(icon, "Quit", self)
        self.quit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.quit_action)

        self.layout.setMenuBar(self.menu_bar)
        
        self.setWindowTitle('Learningapp')
        self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: #FFFFFF;
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }
            QLabel {
                font-size: 16px;
                padding: 10px;
            }
            QLineEdit, QRadioButton, QPushButton {
                background-color: #3E3E3E;
                color: #FFFFFF;
                border: 1px solid #5E5E5E;
                border-radius: 5px;
                padding: 10px;
                font-size: 15px;
            }
            QLineEdit {
                padding: 5px;
            }
            QPushButton {
                background-color: #b2b9a5;
                color: #000000;
                font-size: 20px;
                border: none;
                border-radius: 5px;
                padding: 6px 12px; /* Kleinere Padding-Werte für kleinere Buttons */
            }
            QPushButton:hover {
                background-color: #7c7f95;
            }
            QPushButton:pressed {
                background-color: #004B9A;
            }
            QRadioButton {
                padding: 5px;
            }
            QMenuBar {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QMenuBar::item {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QMenuBar::item:selected {
                background-color: #5E5E5E;
            }
            QMenu {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QMenu::item:selected {
                background-color: #5E5E5E;
            }
        """)
        self.show_start_menu()

    def show_start_menu(self):
        self.clear_layout()

        # Start Button
        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.show_name_and_questions_input)
        self.layout.addWidget(self.start_button)

        # About Button
        self.about_button = QPushButton("About App", self)
        self.about_button.clicked.connect(self.show_about)
        self.layout.addWidget(self.about_button)

         # Quit Button
        self.quit_button = QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.close)
        self.layout.addWidget(self.quit_button)

    def show_name_and_questions_input(self):
        self.clear_layout()

        self.label_name = QLabel("Geben Sie Ihren Namen ein:")
        self.layout.addWidget(self.label_name)

        self.entry_name = QLineEdit(self)
        self.layout.addWidget(self.entry_name)

        self.label_questions = QLabel(f"Wieviele Fragen möchten Sie beantworten? Es gibt aktuell {len(QUESTIONS)} zu beantworten")
        self.layout.addWidget(self.label_questions)

        self.entry_questions = QLineEdit(self)
        self.layout.addWidget(self.entry_questions)

        self.start_quiz_button = QPushButton("Start Test", self)
        self.start_quiz_button.clicked.connect(self.start_quiz)
        self.layout.addWidget(self.start_quiz_button)

    def show_about(self):
        QMessageBox.information(self, "About App", "Diese Anwendung wurde entwickelt und ist Eigentum von Vasco B. (Datenverwaltung), Marcel N. (Hauptprogrammierung) und Marcel A. (Grafische Benutzeroberfläche).")

    def start_quiz(self):
        self.user_name = self.entry_name.text().strip()
        if not self.user_name:
            QMessageBox.critical(self, "Ungültige Eingabe", "Bitte geben Sie Ihren Namen ein.")
            return

        try:
            self.num_questions = int(self.entry_questions.text())
            if not (1 <= self.num_questions <= len(QUESTIONS)):
                raise ValueError
        except ValueError:
            QMessageBox.critical(self, "Ungültige Eingabe", f"Bitte geben Sie eine Zahl zwischen 1 und {len(QUESTIONS)} ein.")
            return

        self.prepare_questions()
        self.show_question_frame()

    def prepare_questions(self):
        # Select random questions from QUESTIONS
        self.questions = random.sample(list(QUESTIONS.items()), k=self.num_questions)

    def show_question_frame(self):
        self.clear_layout()

        self.question_label = QLabel("", self)
        self.layout.addWidget(self.question_label)

        self.answer_group = QButtonGroup(self)
        self.radio_buttons = []

        for i in range(4):
            rb = QRadioButton("", self)
            self.answer_group.addButton(rb)
            self.layout.addWidget(rb)
            self.radio_buttons.append(rb)

        self.submit_button = QPushButton("Antworten", self)
        self.submit_button.clicked.connect(self.submit_answer)
        self.layout.addWidget(self.submit_button)

        self.show_question()

    def show_question(self):
        question, correct_answer = self.questions[self.current_question]
        distractors = DISTRACTORS.get(question, [])


        # Debug print statement
        #print(f"Question: {question}")
        #print(f"Correct Answer: {correct_answer}")
        #print(f"Distractors: {distractors}")

        # Shuffle distractors and add correct answer to the list
        options = [correct_answer] + distractors
        random.shuffle(options)

        self.question_label.setText(f"Frage {self.current_question + 1}: {question}")

        for rb, option in zip(self.radio_buttons, options):
            rb.setText(option)
            rb.setChecked(False)

    def submit_answer(self):
        selected_button = self.answer_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Keine Auswahl", "Bitte wählen Sie eine Antwort aus.")
            return

        answer = selected_button.text()
        question, correct_answer = self.questions[self.current_question]

        if answer == correct_answer:
            self.num_correct += 1
            self.update_score_menu()  # Update score menu on correct answer
            QMessageBox.information(self, "Richtig!", "⭐ Richtig! ⭐")
        else:
            QMessageBox.information(self, "Falsch", f"Die richtige Antwort ist {correct_answer!r}, nicht {answer!r}.")

        self.current_question += 1
        if self.current_question < self.num_questions:
            self.show_question()
        else:
            self.show_result()

    def update_score_menu(self):
        score_text = f"Fragen richtig beantwortet: {self.num_correct}/{self.num_questions}"
        self.score_menu.clear()
        score_action = QAction(score_text, self)
        self.score_menu.addAction(score_action)

    def show_result(self):
        self.clear_layout()

        result_label = QLabel(f"{self.user_name}, Sie haben {self.num_correct} von {self.num_questions} Fragen richtig beantwortet!", self)
        self.layout.addWidget(result_label)

        close_button = QPushButton("Schließen", self)
        close_button.clicked.connect(self.close)
        self.layout.addWidget(close_button)

    def clear_layout(self):
        while self.layout.count() > 0:
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    quiz = QuizApp()
    quiz.show()
    sys.exit(app.exec_())