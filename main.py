from random import sample, shuffle
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class Timetable:
    def __init__(self, courses, lecturers, classrooms, labs, hours_per_day, days_per_week):
        self.courses = courses
        self.lecturers = lecturers
        self.classrooms = classrooms
        self.labs = labs
        self.hours_per_day = hours_per_day
        self.days_per_week = days_per_week
        self.timetable = {course.name: {day: [] for day in range(1, days_per_week + 1)} for course in self.courses}
        for lab in self.labs:
            self.timetable[lab.name] = {day: [] for day in range(1, days_per_week + 1)}

    def allocate_lectures(self):
        days = list(range(1, self.days_per_week + 1))
        shuffle(days)  # Shuffle the days randomly
        labs_to_allocate = sample(self.labs, len(self.labs))  # Randomly select all labs
        lab_day_mapping = {lab: day for lab, day in zip(labs_to_allocate, days)}

        for lab, day in lab_day_mapping.items():
            available_lecturers = [lecturer for lecturer in self.lecturers if lab in lecturer.labs]
            if available_lecturers:
                lecturer = sample(available_lecturers, 1)[0]
                hour = 1
                while hour <= self.hours_per_day:
                    if hour == 4 or hour == 8 or hour == 10:  # Break timings
                        hour += 1
                        continue
                    classroom = sample(self.classrooms, 1)[0]
                    if self.is_available(lecturer, hour, classroom, day):
                        self.timetable[lab.name][day].append((hour, lecturer.name))
                        break
                    else:
                        hour += 1

        days = list(range(1, self.days_per_week + 1))
        for _ in range(self.days_per_week):
            selected_day = days.pop(0)
            subjects = sample(self.courses, len(self.courses))  # Shuffle subjects
            for subject in subjects:
                lecturer = sample([lecturer for lecturer in self.lecturers if subject in lecturer.courses], 1)[0]
                hour = 1
                while hour <= self.hours_per_day:
                    if hour == 4 or hour == 8 or hour == 10:  # Break timings
                        hour += 1
                        continue
                    classroom = sample(self.classrooms, 1)[0]
                    if self.is_available(lecturer, hour, classroom, selected_day):
                        self.timetable[subject.name][selected_day].append((hour, lecturer.name))
                        hour += 1
                        break  # Move to the next subject after allocating one hour
                    else:
                        hour += 1

    def is_available(self, lecturer, hour, classroom, day):
        # Placeholder for actual availability check
        return True


class Course:
    def __init__(self, name):
        self.name = name


class Lecturer:
    def __init__(self, name, courses=None, labs=None):
        self.name = name
        self.courses = courses or []
        self.labs = labs or []


class Classroom:
    def __init__(self, name):
        self.name = name


class Lab:
    def __init__(self, name):
        self.name = name

def visualize_timetable(timetable):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    subjects = list(timetable.timetable.keys())
    hours = range(1, timetable.hours_per_day + 1)

    # Create a 2D list to represent the timetable schedule for all 5 days
    schedule_matrix = [[0] * (timetable.hours_per_day * timetable.days_per_week) for _ in range(len(subjects))]

    for i, subject in enumerate(subjects):
        for day in range(1, timetable.days_per_week + 1):
            for hour, _ in timetable.timetable[subject][day]:
                schedule_matrix[i][(day - 1) * timetable.hours_per_day + hour - 1] = 1

    # Convert the schedule matrix to a NumPy array
    schedule_array = np.array(schedule_matrix)

    # Create a figure and axes
    fig, ax = plt.subplots(figsize=(20, 15))

    # Create the heatmap
    sns.heatmap(schedule_array, cmap=["#F8F9FA", "#FDD835"], linewidths=0.5, linecolor="lightgrey",
                xticklabels=[f"{day}\n{h}:00-{h+1}:00" for day in days_of_week for h in range(8, 17)],
                yticklabels=subjects, cbar=False, ax=ax)

    # Highlight cells with lectures
    for i in range(len(subjects)):
        for j in range(timetable.days_per_week * timetable.hours_per_day):
            if i < len(schedule_array) and j < len(schedule_array[i]) and schedule_array[i][j] == 1:
                ax.add_patch(plt.Rectangle((j, i), 1, 1, fill=False, edgecolor="black", lw=2))

    # Plot labs
    labs = [lab.name for lab in timetable.labs]
    for lab in labs:
        lab_index = subjects.index(lab)
        for day in range(1, timetable.days_per_week + 1):
            for hour, _ in timetable.timetable[lab][day]:
                hour_index = (day - 1) * timetable.hours_per_day + hour - 1
                ax.add_patch(plt.Rectangle((hour_index, lab_index), 1, 1, fill=False, edgecolor="blue", lw=2))

    # Set labels and title
    ax.set_xticks(np.arange(0.5, timetable.days_per_week * timetable.hours_per_day, timetable.hours_per_day))
    ax.set_xticklabels(days_of_week)
    ax.set_yticklabels(subjects, rotation=0)
    ax.set_xlabel("Day of the Week")
    ax.set_ylabel("Subject")
    ax.set_title("Timetable Visualization")

    # Invert y-axis to display subjects from top to bottom
    ax.invert_yaxis()

    # Add gridlines
    ax.grid(visible=True, color="lightgrey")

    # Adjust layout
    plt.tight_layout()

    # Show the plot
    plt.show()



if __name__ == "__main__":
    # Define courses, lecturers, classrooms, and labs
    course_ProjectManagement = Course("Project Management")
    course_WirelessNetwork = Course("Wireless Network")
    course_ParallelComputing = Course("Parallel Computing")
    course_MachineLearning = Course("Machine Learning")
    course_SoftwareEngineering = Course("Software Engineering")
    course_PCS = Course("PCS")

    lab_WirelessNetworkLab = Lab("Wireless Network Lab")
    lab_ParallelComputingLab = Lab("Parallel Computing Lab")
    lab_MachineLearningLab = Lab("Machine Learning Lab")
    lab_SoftwareEngineeringLab = Lab("Software Engineering Lab")

    lecturer_ProjectManagement = Lecturer("Miss.Priyanka Narwade", [course_ProjectManagement], [])
    lecturer_WirelessNetwork = Lecturer("Dr.M.M Chandane", [course_WirelessNetwork], [lab_WirelessNetworkLab])
    lecturer_ParallelComputing = Lecturer("Dr.PM Chawan", [course_ParallelComputing], [lab_ParallelComputingLab])
    lecturer_MachineLearning = Lecturer("Dr.S.S Sharwane", [course_MachineLearning], [lab_MachineLearningLab])
    lecturer_SoftwareEngineering = Lecturer("Dr.Bedkar", [course_SoftwareEngineering], [lab_SoftwareEngineeringLab])
    lecturer_PCS = Lecturer("Dr.Nilima Chaudhary", [course_PCS], [])

    classroom_a = Classroom("AL002")
    classroom_b = Classroom("AL003")
    classroom_c = Classroom("AL004")
    classroom_d = Classroom("AL301")
    classroom_e = Classroom("AL302")

    lab_a = Lab("CS IT LAB1")
    lab_b = Lab("CS IT LAB2")
    lab_c = Lab("CS IT LAB3")

    # Create a timetable object
    timetable = Timetable([course_ProjectManagement, course_WirelessNetwork, course_ParallelComputing,
                           course_MachineLearning, course_SoftwareEngineering, course_PCS],
                          [lecturer_ProjectManagement, lecturer_WirelessNetwork, lecturer_ParallelComputing,
                           lecturer_MachineLearning, lecturer_SoftwareEngineering, lecturer_PCS],
                          [classroom_a, classroom_b, classroom_c, classroom_d, classroom_e],
                          [lab_WirelessNetworkLab, lab_ParallelComputingLab, lab_MachineLearningLab,
                           lab_SoftwareEngineeringLab, lab_a, lab_b, lab_c],
                          hours_per_day=9,
                          days_per_week=5)  # Assuming a 5-day work week

    # Allocate lectures and labs
    timetable.allocate_lectures()

    # Visualize the timetable
    visualize_timetable(timetable)
