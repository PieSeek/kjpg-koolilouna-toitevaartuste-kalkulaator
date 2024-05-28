from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        soovitud = request.form['soovitud']
        suurus = request.form['suurus']
        if soovitud and suurus:
            failiNimi = 'api/' + soovitud + '-' + suurus + '.csv'
            andmed = []
            csvfail = open(failiNimi, encoding='UTF-8')
            loetudCSV = csv.reader(csvfail, delimiter=';')
            for rida in loetudCSV:
                andmed.append(rida)
            csvfail.close()
            return render_template('checklist.html', andmed=andmed, soovitud=soovitud, suurus=suurus)
        else:
            return render_template('index.html', error='Palun sisesta nii kuupäev kui ka suurus')
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    andmed = request.form.getlist('toit')
    soovitud = request.form['soovitud']
    suurus = request.form['suurus']
    lõuna = []
    for toit in andmed:
        csv_file_path = soovitud + '-' + suurus + '.csv'
        csvfail = open(csv_file_path, encoding='UTF-8')
        loetudCSV = csv.reader(csvfail, delimiter=';')
        for rida in loetudCSV:
            if rida[0] == toit:
                lõuna.append(rida[1:])
        csvfail.close()

    c = []
    for a in lõuna:
        väärtused = []
        for b in a:
            väärtused.append(float(b))
        c.append(väärtused)

    def sum_lists(*args):
        return list(map(sum, zip(*args)))

    kaal = sum(c[i][0] for i in range(len(c)))
    kalorid = round(sum(c[i][1] for i in range(len(c))), 2)
    valgud = round(sum(c[i][2] for i in range(len(c))), 2)
    rasvad = round(sum(c[i][3] for i in range(len(c))), 2)
    süsivesikud = round(sum(c[i][4] for i in range(len(c))), 2)

    return render_template('result.html', kaal=kaal, kalorid=kalorid, valgud=valgud, rasvad=rasvad, süsivesikud=süsivesikud)

if __name__ == '__main__':
    app.run(debug=False)
