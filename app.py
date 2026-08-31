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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/timetable")
def get_timetable():
    return jsonify(timetable)


@app.route("/college-info")
def get_college_info():
    return jsonify(college_info)


@app.route("/assignments")
def get_assignments():
    return jsonify(assignments)


@app.route("/events")
def get_events():
    return jsonify(events)


@app.route("/ask", methods=["POST"])
def ask():

    data = request.get_json()
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
    # IS COLLEGE OPEN TODAY?
    # -------------------------

    elif (
        "is college open today" in question
        or "college open today" in question
        or "is college today" in question
    ):

        today = datetime.now().strftime("%A")

        if today == "Sunday":
            answer = "No. Today is Sunday, so college is closed."
        else:
            answer = (
                f"Yes. Today is {today}, and college is open "
                f"from 8:30 AM to 4:00 PM."
            )


    # -------------------------
    # SUNDAY
    # -------------------------

    elif "sunday" in question:

        answer = f"Sunday is a {college_info['sunday']}."


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
    # ASSIGNMENTS
    # -------------------------

    elif (
        "assignment" in question
        or "assignments" in question
        or "my homework" in question
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
    # TOMORROW
    # -------------------------

    elif "tomorrow" in question:

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_day = tomorrow.strftime("%A")

        if tomorrow_day in timetable:

            classes = timetable[tomorrow_day]

            answer = (
                f"Tomorrow is {tomorrow_day}. "
                "Your timetable is: "
                + ", ".join(classes)
                + "."
            )

        else:

            answer = (
                f"Tomorrow is {tomorrow_day}, "
                "and there are no classes."
            )


    # -------------------------
    # TODAY
    # -------------------------

    elif "today" in question:

        today = datetime.now().strftime("%A")

        if today in timetable:

            answer = (
                f"Today's timetable for {today}: "
                + ", ".join(timetable[today])
                + "."
            )

        else:

            answer = "Today is a holiday."


    # -------------------------
    # MONDAY
    # -------------------------

    elif "monday" in question:

        answer = (
            "Monday timetable: "
            + ", ".join(timetable["Monday"])
            + "."
        )


    # -------------------------
    # TUESDAY
    # -------------------------

    elif "tuesday" in question:

        answer = (
            "Tuesday timetable: "
            + ", ".join(timetable["Tuesday"])
            + "."
        )


    # -------------------------
    # WEDNESDAY
    # -------------------------

    elif "wednesday" in question:

        answer = (
            "Wednesday timetable: "
            + ", ".join(timetable["Wednesday"])
            + "."
        )


    # -------------------------
    # THURSDAY
    # -------------------------

    elif "thursday" in question:

        answer = (
            "Thursday timetable: "
            + ", ".join(timetable["Thursday"])
            + "."
        )


    # -------------------------
    # FRIDAY
    # -------------------------

    elif "friday" in question:

        answer = (
            "Friday timetable: "
            + ", ".join(timetable["Friday"])
            + "."
        )


    # -------------------------
    # SATURDAY
    # -------------------------

    elif "saturday" in question:

        answer = (
            "Saturday timetable: "
            + ", ".join(timetable["Saturday"])
            + "."
        )


    # -------------------------
    # NEXT CLASS
    # -------------------------

    elif "next class" in question:

        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_day = tomorrow.strftime("%A")

        if tomorrow_day in timetable:

            answer = (
                f"Your next scheduled class is on "
                f"{tomorrow_day}: "
                + timetable[tomorrow_day][0]
                + "."
            )

        else:

            answer = "There is no scheduled class information."


    # -------------------------
    # GENERAL TIMETABLE
    # -------------------------

    elif (
        "timetable" in question
        or "time table" in question
    ):
        answer = (
            "Click the 📅 Timetable button "
            "to see your weekly timetable."
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
