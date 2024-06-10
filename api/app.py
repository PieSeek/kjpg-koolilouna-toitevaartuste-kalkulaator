from flask import Flask, render_template, request
import csv

app = Flask(__name__)

# See osa ütleb Flaskile, et käivita see funktsioon, kui keegi läheb veebilehe juurde
@app.route('/', methods=['GET', 'POST'])
def index():
    # See osa kontrollib, kas kasutaja saatis vormi (klõpsis nuppu)
    if request.method == 'POST':
        # See osa võtab kasutaja sisestatud kuupäeva ja suuruse vormist
        soovitud = request.form['soovitud']
        suurus = request.form['suurus']
        # See osa kontrollib, kas mõlemad väljad on täidetud
        if soovitud and suurus:
            # See osa loob faili nime kuupäeva ja suuruse põhjal
            failiNimi = 'api/' + soovitud + '-' + suurus + '.csv'
            andmed = []
            # See osa avab CSV faili, et seda lugeda
            csvfail = open(failiNimi, encoding='UTF-8')
            loetudCSV = csv.reader(csvfail, delimiter=';')
            # See osa loeb CSV faili read ja lisab need andmed nimekirja
            for rida in loetudCSV:
                andmed.append(rida)
            # See osa sulgeb CSV faili
            csvfail.close()
            # See osa näitab kasutajale toiduainete nimekirja, mida saab valida
            return render_template('checklist.html', andmed=andmed, soovitud=soovitud, suurus=suurus)
        else:
            # See osa näitab veateadet, kui mõlemad väljad pole täidetud
            return render_template('index.html', error='Palun sisesta nii kuupäev kui ka suurus')
    # See osa näitab algset veebilehte, kui keegi esimest korda selle avab
    return render_template('index.html')

# See osa ütleb Flaskile, et käivita see funktsioon, kui keegi läheb /result lehele
@app.route('/result', methods=['POST'])
def result():
    # See osa võtab kasutaja valitud toidud vormist nimekirjana
    andmed = request.form.getlist('toit')
    # See osa võtab kasutaja sisestatud kuupäeva ja suuruse vormist
    soovitud = request.form['soovitud']
    suurus = request.form['suurus']
    lõuna = []
    # See osa läbib kasutaja valitud toidud
    for toit in andmed:
        # See osa loob faili nime kuupäeva ja suuruse põhjal
        csv_file_path = 'api/' + soovitud + '-' + suurus + '.csv'
        # See osa avab CSV faili, et seda lugeda
        csvfail = open(csv_file_path, encoding='UTF-8')
        loetudCSV = csv.reader(csvfail, delimiter=';')
        # See osa läbib CSV faili read
        for rida in loetudCSV:
            # See osa kontrollib, kas toiduaine nimi vastab valitud toidule
            if rida[0] == toit:
                # See osa lisab vastava rea lõuna nimekirja
                lõuna.append(rida[1:])
        # See osa sulgeb CSV faili
        csvfail.close()

    c = []
    # See osa läbib lõuna nimekirja
    for a in lõuna:
        väärtused = []
        # See osa teisendab iga rea väärtused numbriteks
        for b in a:
            väärtused.append(float(b))
        # See osa lisab teisendatud väärtused c nimekirja
        c.append(väärtused)

    # See funktsioon summeerib antud nimekirjade väärtused veergude kaupa
    def sum_lists(*args):
        return list(map(sum, zip(*args)))

    # See osa arvutab valitud toiduainete kogusumma kaalule, kaloritele, valkudele, rasvadele ja süsivesikutele
    kaal = sum(c[i][0] for i in range(len(c)))
    kalorid = round(sum(c[i][1] for i in range(len(c))), 2)
    valgud = round(sum(c[i][2] for i in range(len(c))), 2)
    rasvad = round(sum(c[i][3] for i in range(len(c))), 2)
    süsivesikud = round(sum(c[i][4] for i in range(len(c))), 2)

    # See osa näitab kasutajale arvutatud toitainete väärtusi
    return render_template('result.html', kaal=kaal, kalorid=kalorid, valgud=valgud, rasvad=rasvad, süsivesikud=süsivesikud)

# See osa käivitab kogu rakenduse
if __name__ == '__main__':
    app.run(debug=False)
