from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Mwerxz23",
    "database": "sparks",
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/view")
def view():
    conn = mysql.connector.connect(**db_config)

    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, curr_bal, city FROM bank_user")
    data = cursor.fetchall()
    conn.close()
    return render_template("view.html", data=data)


@app.route("/search", methods=["POST", "GET"])
def search():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, curr_bal, city FROM bank_user")
    data = cursor.fetchall()
    conn.close()

    name = request.form.get("name")
    matched_user = []
    if name:
        for user in data:
            if user[1].startswith(name):
                matched_user.append(user)
    else:
        matched_user = data
    return render_template("search.html", users=matched_user)


@app.route("/transfer", methods=["POST", "GET"])
def transfer():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, curr_bal, city FROM bank_user")
    data = cursor.fetchall()
    conn.close()
    name = request.form.get("name")
    matched_user = []
    if name:
        for user in data:
            if user[1].startswith(name):
                matched_user.append(user)
    else:
        matched_user = data
    return render_template("transfer.html", users=matched_user)


@app.route("/tr", methods=["POST", "GET"])
def trans():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, name, email, curr_bal, city FROM bank_user")
    data = cursor.fetchall()
    conn.close()
    sender = request.form.get("sender")
    return render_template("tr.html", sender=sender)


@app.route("/transferamount", methods=["GET", "POST"])
def amount():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    sender = request.form.get("sender")

    receiver = request.form.get("Name")

    Amount = int(request.form.get("amount"))
    cursor.execute(
        "SELECT user_id, name, curr_bal FROM bank_user WHERE name IN (%s, %s)",
        (sender, receiver),
    )
    users = cursor.fetchall()
    if len(users) == 2:
        sender_info = [user for user in users if user[1] == sender][0]
        receiver_info = [user for user in users if user[1] == receiver][0]
        sender_id = sender_info[0]
        receiver_id = receiver_info[0]
        sender_balance = int(sender_info[2])
        receiver_balance = receiver_info[2]
        if sender_balance >= Amount:
            new_sender_balance = sender_balance - Amount
            cursor.execute(
                "UPDATE bank_user SET curr_bal = %s WHERE user_id = %s",
                (new_sender_balance, sender_id),
            )

            new_receiver_balance = receiver_balance + Amount
            cursor.execute(
                "UPDATE bank_user SET curr_bal = %s WHERE user_id = %s",
                (new_receiver_balance, receiver_id),
            )

            cursor.execute(
                "INSERT INTO transfer (sender, receiver, amount) VALUES (%s, %s, %s)",
                (sender_id, receiver_id, Amount),
            )

            conn.commit()
            conn.close()
            return redirect('/')
        else:
            conn.close()
            return "Insufficient balance"
    else:
        conn.close()
        return "Sender or receiver not found"


if __name__ == "__main__":
    app.run(debug=True)
