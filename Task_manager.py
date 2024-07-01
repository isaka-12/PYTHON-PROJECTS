from datetime import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class TaskManager:
    def __init__(self):
        self.tasks = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}
        self.evaluations = {day: [] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]}

    def add_task(self, day, task):
        if day in self.tasks:
            self.tasks[day].append(task)
        else:
            print(f"Invalid day: {day}")

    def evaluate_task(self, day, task, evaluation):
        if day in self.evaluations:
            self.evaluations[day].append((task, evaluation))
        else:
            print(f"Invalid day: {day}")

    def save_to_text_file(self, filename):
        with open(filename, 'w') as file:
            for day in self.tasks:
                file.write(f"{day}:\n")
                for task in self.tasks[day]:
                    file.write(f"  Task: {task}\n")
                for task, evaluation in self.evaluations[day]:
                    file.write(f"  Task: {task} - Evaluation: {evaluation}\n")
                file.write("\n")

    def save_to_pdf(self, filename):
        text_filename = "weekly_tasks.txt"
        if not os.path.exists(text_filename):
            self.save_to_text_file(text_filename)

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        with open(text_filename, 'r') as file:
            text = file.readlines()

        y = height - 40
        for line in text:
            if y < 40:
                c.showPage()
                y = height - 40
            c.drawString(40, y, line.strip())
            y -= 15

        c.save()

def get_user_input():
    manager = TaskManager()
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for day in days:
        print(f"Enter tasks for {day} (type 'done' when finished):")
        while True:
            task = input(f"  Task: ")
            if task.lower() == 'done':
                break
            manager.add_task(day, task)
    
    for day in days:
        print(f"Evaluate tasks for {day}:")
        for task in manager.tasks[day]:
            evaluation = input(f"  Task '{task}' - Evaluation: ")
            manager.evaluate_task(day, task, evaluation)
    
    return manager

if __name__ == "__main__":
    manager = get_user_input()
    manager.save_to_text_file("weekly_tasks.txt")
    manager.save_to_pdf("weekly_tasks.pdf")
    print("Tasks and evaluations have been saved to 'weekly_tasks.txt' and 'weekly_tasks.pdf'")
