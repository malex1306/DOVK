import tkinter as tk
from tkinter import messagebox

# Daten für das Quiz
questions = [
    "Um den Kern eines Koaxialkabels befindet sich ein Mantel aus einem nicht leitenden Material. Wie nennt man diese nichtleitende Schicht in der Elektronik?",
    "Eine wichtige physikalische Eigenschaft des Kabels ist sein Dämpfungsverhalten. In welcher Einheit wird dieses Verhalten gemessen?",
    "Welches Werkzeug benötigen Sie, um das Kabel für den Eigengebrauch selbst  zu vorbereiten?"
]

options = [
    ["dielektrische Schicht", "Schicht 1", "Schicht 4", "Schicht 5"],
    ["Flasche", "Dose", "Dezibel ", "Bass"],
    ["spezielle Kabelschneider", "crimp", "Mars", "Merkur"]
]

answers = ["dielektrische Schicht", "Dezibel", "crimp"]

class QuizApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Multiple Choice Quiz")
        self.current_question = 0
        self.correct_answers = 0

        self.question_label = tk.Label(master, text=questions[self.current_question])
        self.question_label.pack(pady=20)

        self.var = tk.StringVar()

        self.option_buttons = []
        for option in options[self.current_question]:
            rb = tk.Radiobutton(master, text=option, variable=self.var, value=option)
            rb.pack(anchor='w')
            self.option_buttons.append(rb)

        self.next_button = tk.Button(master, text="Weiter", command=self.next_question)
        self.next_button.pack(pady=20)

    def next_question(self):
        if self.var.get() == answers[self.current_question]:
            self.correct_answers += 1
        
        self.current_question += 1

        if self.current_question < len(questions):
            self.update_question()
        else:
            self.show_result()

    def update_question(self):
        self.question_label.config(text=questions[self.current_question])
        self.var.set(None)
        for i, option in enumerate(options[self.current_question]):
            self.option_buttons[i].config(text=option, value=option)

    def show_result(self):
        messagebox.showinfo("Ergebnis", f"Du hast {self.correct_answers} von {len(questions)} richtig beantwortet!")
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()