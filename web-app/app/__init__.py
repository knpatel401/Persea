from flask import Flask
from sklearn.externals import joblib
import pickle
import numpy as np
import xmltodict
import pandas as pd

app = Flask(__name__)
app.config.from_object("app.config")

# unpickle my model
vectorizer = pickle.load(open("models/vectorizer.pkl","rb"))
lsa = pickle.load(open("models/lsa.pkl","rb"))
dtm_lsa = np.load('models/dtm_lsa.npy')
df_filtered = pd.read_pickle('models/df_filtered.pkl')

from .views import *
 

# Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    """Page Not Found"""
    return render_template('404.html'), 404
