from flask import Flask, request, render_template
from flask_cors import CORS
from data_scraping import review_scrape
from data_preprocessing import preprocessing
from fit_transform import fit_transform
from visualization import LDAvis, wordcloud
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/topics', methods=['GET', 'POST'])
def topic_modelling():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        url = request.form.get('link')
        url += '/review'

        bintang = request.form.get('bintang')

        print('scraping reviews...')
        review_scrape(url, bintang)

        print('preprocessing data...')
        df = preprocessing()

        print('fit transform...')
        LDAmodel_, corpus_t, dictionary_t = fit_transform(df)

        print('creating visualizations...')
        LDAvis(LDAmodel_, corpus_t, dictionary_t)
        for i in range(3):
            wordcloud(LDAmodel_, i)

        return render_template('prediction.html')
    return render_template('prediction.html')

    

if __name__ == "__main__":
    app.run(host="0.0.0.0")