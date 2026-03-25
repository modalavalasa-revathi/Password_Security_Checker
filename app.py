from flask import Flask, render_template, request
import random
import string

app = Flask(__name__)

# Common breached passwords
breached_passwords = [
    "123456",
    "password",
    "123456789",
    "qwerty",
    "abc123",
    "111111",
    "123123",
    "password123"
]

def check_password_strength(password):

    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append("Add numbers")

    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append("Add uppercase letters")

    if any(char in "!@#$%^&*()" for char in password):
        score += 1
    else:
        suggestions.append("Add special symbols")

    if score <= 1:
        strength = "Weak"
        color = "red"
        width = "30%"
    elif score <= 3:
        strength = "Medium"
        color = "orange"
        width = "60%"
    else:
        strength = "Strong"
        color = "green"
        width = "100%"

    return strength, suggestions, color, width


def check_breach(password):

    if password.lower() in breached_passwords:
        return "⚠ This password is found in common breaches!", "red"
    else:
        return "✔ This password was NOT found in common breaches.", "green"


def generate_password():

    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = ''.join(random.choice(characters) for i in range(12))
    return password


@app.route('/', methods=['GET','POST'])
def index():

    result = ""
    suggestions = []
    color = ""
    width = "0%"
    breach_message = ""
    breach_color = ""
    generated_password = ""

    if request.method == "POST":

        if "generate" in request.form:
            generated_password = generate_password()

        else:
            password = request.form['password']

            result, suggestions, color, width = check_password_strength(password)

            breach_message, breach_color = check_breach(password)

    return render_template("index.html",
                           result=result,
                           suggestions=suggestions,
                           color=color,
                           width=width,
                           breach_message=breach_message,
                           breach_color=breach_color,
                           generated_password=generated_password)


if __name__ == "__main__":
    app.run(debug=True)