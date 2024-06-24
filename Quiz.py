import tkinter as tk
from tkinter import messagebox
import random
from string import ascii_lowercase

# Die richtigen Antworten müssen an erster Stelle in der eckigen Klammer stehen.
QUESTIONS = {
    "Um den Kern eines Koaxialkabels befindet sich ein Mantel aus einem nicht leitenden Material. Wie nennt man diese nichtleitende Schicht in der Elektronik?":
    ["dielektrische Schicht", "Schicht 1", "Schicht 4", "Schicht 5"],
    "Eine wichtige physikalische Eigenschaft des Kabels ist sein Dämpfungsverhalten. In welcher Einheit wird dieses Verhalten gemessen?":
    ["Dezibel", "Dose", "Fleisch", "Bass"],
    "Welches Werkzeug benötigen Sie, um das Kabel für den Eigengebrauch selbst vorzubereiten?":
    ["Crimp", "Spezieller Kabelschneider", "Mars", "Merkur"]
}

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz")
        self.num_questions = 0
        self.questions = []
        self.current_question = 0
        self.num_correct = 0

        self.setup_start_frame()

    def setup_start_frame(self):
        self.start_frame = tk.Frame(self.root)
        self.start_frame.pack(pady=20)

        self.label = tk.Label(self.start_frame, text="Wieviele Fragen möchten Sie beantworten?")
        self.label.pack(pady=5)

        self.entry = tk.Entry(self.start_frame)
        self.entry.pack(pady=5)

        self.start_button = tk.Button(self.start_frame, text="Start", command=self.start_quiz)
        self.start_button.pack(pady=5)

    def start_quiz(self):
        try:
            self.num_questions = int(self.entry.get())
            if not (1 <= self.num_questions <= len(QUESTIONS)):
                raise ValueError
        except ValueError:
            messagebox.showerror("Ungültige Eingabe", f"Bitte geben Sie eine Zahl zwischen 1 und {len(QUESTIONS)} ein.")
            return

        self.start_frame.pack_forget()
        self.prepare_questions()
        self.setup_question_frame()

    def prepare_questions(self):
        self.questions = random.sample(list(QUESTIONS.items()), k=self.num_questions)

    def setup_question_frame(self):
        self.question_frame = tk.Frame(self.root)
        self.question_frame.pack(pady=20)

        self.question_label = tk.Label(self.question_frame, text="", wraplength=400)
        self.question_label.pack(pady=10)

        self.answer_var = tk.StringVar()
        self.radio_buttons = []

        for i in range(4):
            rb = tk.Radiobutton(self.question_frame, text="", variable=self.answer_var, value="", anchor="w")
            rb.pack(fill="x", padx=20)
            self.radio_buttons.append(rb)

        self.submit_button = tk.Button(self.question_frame, text="Antworten", command=self.submit_answer)
        self.submit_button.pack(pady=10)

        self.show_question()

    def show_question(self):
        question, alternatives = self.questions[self.current_question]
        self.correct_answer = alternatives[0]
        ordered_alternatives = random.sample(alternatives, k=len(alternatives))

        self.question_label.config(text=f"Frage {self.current_question + 1}: {question}")

        for rb, alternative in zip(self.radio_buttons, ordered_alternatives):
            rb.config(text=alternative, value=alternative)
        self.answer_var.set(None)  # Reset the selected answer

    def submit_answer(self):
        answer = self.answer_var.get()
        if not answer:
            messagebox.showwarning("Keine Auswahl", "Bitte wählen Sie eine Antwort aus.")
            return

        if answer == self.correct_answer:
            self.num_correct += 1
            messagebox.showinfo("Richtig!", "⭐ Richtig! ⭐")
        else:
            messagebox.showinfo("Falsch", f"Die richtige Antwort ist {self.correct_answer!r}, nicht {answer!r}.")

        self.current_question += 1
        if self.current_question < self.num_questions:
            self.show_question()
        else:
            self.show_result()

    def show_result(self):
        self.question_frame.pack_forget()
        result_frame = tk.Frame(self.root)
        result_frame.pack(pady=20)

        result_label = tk.Label(result_frame, text=f"Sie haben {self.num_correct} von {self.num_questions} Fragen richtig beantwortet!")
        result_label.pack(pady=10)

        close_button = tk.Button(result_frame, text="Schließen", command=self.root.quit)
        close_button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
