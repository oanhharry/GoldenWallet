from flask import *
from mongoengine import *

app = Flask(__name__)

app.secret_key = "123456789"

@app.route('/', methods = ['GET', 'POST'])
def index():
    error = 0
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        form = request.form
        income = form['income']
        goal = form['goal']
        month = form['month']
        max = form['max']
        bank = form['bank']
        if income == "" or goal == "" or month == "" or max == "" or bank == "":
            error = 1
            return render_template('error.html',error=error)
        elif float(max)> float(income):
            error = 3
            return render_template('error.html', error = error)
        else:
            saving = (int(goal)*float(bank)/12)/(pow((1+float(bank)/12),int(month))-1)
            session['income']= income
            session['goal']=goal
            session['saving']=saving
            session['bank']=bank
            session['month']=month

            if saving > float(max) :
                error = 2
                return render_template('error.html',error=error)
            else:
                return redirect (url_for('saving'))

@app.route('/saving')
def saving():
    colors = ["#f54844", "#dbdad3"]
    labels = ["Tiết kiệm","Thu nhập"]

    goal = int(session['goal'])
    month = int(session['month'])
    bank = float(session['bank'])
    saving = float(session['saving'])
    income = float(session['income'])
    ratio_save_income = round(saving/income*100,2)

    pie_labels = labels
    pie_values = [round(saving,2), session['income']]

    bar_values= []
    bar_labels = []
    max = goal +50
    var = 0
    for i in range(int(month)):
        name = "Tháng thứ " + str(i + 1)
        var = var + saving*(pow((1+bank/12),i))
        bar_labels.append(name)
        bar_values.append(round(var))

    return render_template('saving.html',saving=round(saving,2), max=max, set=zip(pie_values, labels, colors),labels=bar_labels, values=bar_values, ratio_save_income = ratio_save_income)

@app.route('/analysis', methods = ['GET', 'POST'])
def analysis():
    error = 0
    income = float(session['income'])
    saving = float(session['saving'])
    money = round(income - saving,2)
    if request.method == "GET":
        return render_template('detail.html', money = money)
    elif request.method == "POST":
        form = request.form
        n1 = float(form['n1'])
        n2 = float(form['n2'])
        n3 = float(form['n3'])
        n4 = float(form['n4'])
        n5 = float(form['n5'])
        if (n1 + n2 + n3 + n4 + n5) != 1:
            error = 1
            return render_template('detail.html', money = money,error=error)
        else:
            return render_template('spending.html', money = money, n1=round(round(n1,1)*money,2), n2=round(round(n2,1)*money,2), n3=round(round(n3,1)*money,2), n4=round(round(n4,1)*money,2), n5=round(round(n5,1)*money))

if __name__ == '__main__':
  app.run(debug=True)
