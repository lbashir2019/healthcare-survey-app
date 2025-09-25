from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from user import User  # Make sure user.py is in the same folder

app = Flask(__name__)

# === MongoDB Connection ===
client = MongoClient("mongodb://localhost:27017/")
db = client["surveyDB"]
collection = db["users"]

# === Flask Routes ===
@app.route("/", methods=["GET", "POST"])
def survey():
    if request.method == "POST":
        # Get form data
        age = int(request.form.get("age"))
        gender = request.form.get("gender")
        income = float(request.form.get("income"))

        # Collect expenses
        expenses = {}
        categories = ["utilities", "entertainment", "school_fees", "shopping", "healthcare"]
        for cat in categories:
            if request.form.get(cat):  # checkbox checked
                amount = request.form.get(f"{cat}_amount")
                expenses[cat] = float(amount) if amount else 0

        # === Save to MongoDB ===
        user_data = {
            "age": age,
            "gender": gender,
            "income": income,
            "expenses": expenses
        }
        collection.insert_one(user_data)

        # === Process with User class ===
        user = User(age, gender, income, expenses)
        user.save_to_csv("survey_data.csv")  # Saves CSV in project folder

        return redirect("/thankyou")

    return render_template("survey.html")


@app.route("/thankyou")
def thankyou():
    return "<h2>Thank you! Your data has been saved.</h2>"


# === Run App ===
if __name__ == "__main__":
    app.run(debug=True)
