from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta

from college_data import (
    timetable,
    student_info,
    college_info,
    assignments,
    events
)

app = Flask(__name__)


# =========================
# HOME
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# TIMETABLE
# =========================

@app.route("/timetable")
def get_timetable():
    return jsonify(timetable)


# =========================
# COLLEGE INFORMATION
# =========================

@app.route("/college-info")
def get_college_info():
    return jsonify(college_info)


# =========================
# ASSIGNMENTS
# =========================

@app.route("/assignments")
def get_assignments():
    return jsonify(assignments)


# =========================
# EVENTS
# =========================

@app.route("/events")
def get_events():
    return jsonify(events)


# =========================
# ASK ASSISTANT
# =========================

@app.route("/ask", methods=["POST"])
def ask():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "answer": "Please ask me a question."
            })

        question = data.get("question", "").lower().strip()

        # -------------------------
        # NAME
        # -------------------------

        if (
            "who am i" in question
            or "my name" in question
            or "what is my name" in question
        ):
            answer = f"Your name is {student_info['name']}."


        # -------------------------
        # COLLEGE NAME
        # -------------------------

        elif (
            "college name" in question
            or "name of college" in question
            or "which college" in question
            or "what college" in question
        ):
            answer = f"Your college is {college_info['college_name']}."


        # -------------------------
        # COURSE
        # -------------------------

        elif (
            "course" in question
            or "what do i study" in question
            or "what am i studying" in question
            or "which course" in question
        ):
            answer = f"Your course is {student_info['course']}."


        # -------------------------
        # YEAR
        # -------------------------

        elif (
            "what year" in question
            or "which year" in question
            or "my year" in question
        ):
            answer = f"You are currently in {student_info['year']}."


        # -------------------------
        # COLLEGE TIMING
        # -------------------------

        elif (
            "timing" in question
            or "college time" in question
            or "college timings" in question
            or "when does college open" in question
        ):
            answer = (
                f"College timings are "
                f"{college_info['college_timing']}."
            )


        # -------------------------
        # LIBRARY
        # -------------------------

        elif (
            "library" in question
            or "where is library" in question
            or "library location" in question
        ):
            answer = f"The library is {college_info['library']}."


        # -------------------------
        # SUNDAY
        # -------------------------

        elif "sunday" in question:

            answer = f"Sunday is a {college_info['sunday']}."


        # -------------------------
        # ASSIGNMENTS
        # -------------------------

        elif (
            "assignment" in question
            or "assignments" in question
            or "homework" in question
        ):
            answer = (
                "Your assignments are: "
                + ", ".join(assignments)
                + "."
            )


        # -------------------------
        # EVENTS
        # -------------------------

        elif (
            "event" in question
            or "events" in question
            or "college event" in question
        ):
            answer = (
                "Your college events are: "
                + ", ".join(events)
                + "."
            )


        # -------------------------
        # TUESDAY
        # -------------------------

        elif "tuesday" in question:

            classes = timetable.get("Tuesday", [])

            if classes:
                answer = (
                    "Tuesday timetable: "
                    + " | ".join(classes)
                )
            else:
                answer = "There is no Tuesday timetable available."


        # -------------------------
        # TODAY
        # -------------------------

        elif "today" in question:

            today = datetime.now().strftime("%A")

            if today == "Sunday":
                answer = "Today is Sunday. College is closed."

            elif today in timetable:

                classes = timetable[today]

                answer = (
                    f"Today's timetable for {today}: "
                    + " | ".join(classes)
                )

            else:
                answer = (
                    f"Today is {today}. "
                    "No timetable has been added yet."
                )


        # -------------------------
        # TOMORROW
        # -------------------------

        elif "tomorrow" in question:

            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_day = tomorrow.strftime("%A")

            if tomorrow_day == "Sunday":

                answer = (
                    "Tomorrow is Sunday. "
                    "College is closed."
                )

            elif tomorrow_day in timetable:

                classes = timetable[tomorrow_day]

                answer = (
                    f"Tomorrow is {tomorrow_day}. "
                    "Your timetable is: "
                    + " | ".join(classes)
                )

            else:

                answer = (
                    f"Tomorrow is {tomorrow_day}. "
                    "No timetable has been added yet."
                )


        # -------------------------
        # GENERAL TIMETABLE
        # -------------------------

        elif (
            "timetable" in question
            or "time table" in question
        ):
            answer = (
                "You can click the Timetable button "
                "to see the available timetable."
            )


        # -------------------------
        # GREETING
        # -------------------------

        elif (
            "hello" in question
            or "hi" in question
            or "hey" in question
        ):
            answer = (
                f"Hello {student_info['name']}! "
                "Welcome to your College AI Assistant."
            )


        # -------------------------
        # THANK YOU
        # -------------------------

        elif "thank" in question:

            answer = "You're welcome!"


        # -------------------------
        # UNKNOWN
        # -------------------------

        else:

            answer = (
                "Sorry, I don't know that yet. "
                "You can ask about your name, college, "
                "course, year, timings, library, "
                "assignments, events, or timetable."
            )


        return jsonify({
            "answer": answer
        })

    except Exception as error:

        print("ERROR:", error)

        return jsonify({
            "answer": "There was a problem processing your question."
        }), 500


# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )