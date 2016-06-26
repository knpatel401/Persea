from flask import render_template
from flask import request
from flask_wtf import Form
from wtforms import fields
from wtforms.validators import Required
import numpy as np
from . import app,vectorizer,lsa,dtm_lsa,df_filtered
import re
from nltk.corpus import stopwords
import heapq

cachedStopWords = stopwords.words("english")
NUM_RESULTS = 10
title = []
question = []
answer = []
score = []
search_query = ''
title_query = ''
highlight_enabled = False
question_index = 0

class SearchForm(Form):
    """Fields for Search"""
    search_query = fields.StringField('Search Query:', validators=[Required()])
    title_query = fields.StringField('', validators=[])
#    title_query = fields.TextAreaField('', validators=[])
    #answer_query = fields.StringField('', validators=[Required()])
    submit = fields.SubmitField('Submit')

def lookup_search(query):
    from sklearn.preprocessing import Normalizer
    from IPython.core.display import display, HTML

    test_text = [query,query]
    dtm_test = vectorizer.transform(test_text) 
    dtm_test_lsa = lsa.transform(dtm_test)
    dtm_test_lsa = Normalizer(copy=False).transform(dtm_test_lsa)

    dot_prods = (np.matrix(dtm_test_lsa[0])*np.matrix(dtm_lsa).transpose())
    test = dot_prods.tolist()[0]
    val= test.index(max(test))
    print("Score = " + str(max(test)))
    
    if max(test) == 0:
        question = False
        answer = False
        title = "<font color=\"red\">Sorry, no search result found</font>"
        score = "0"
        return title,question,answer,score
    else:
        max_vals = heapq.nlargest(NUM_RESULTS, enumerate(test), key=lambda x: x[1])
        max_indices = [x[0] for x in max_vals]
        print max_indices
        score = [round(x[1],2) for x in max_vals]
        title = df_filtered.iloc[max_indices]['@Title'].values
        question = df_filtered.iloc[max_indices]['@Body'].values
        answer = df_filtered.iloc[max_indices]['@Answer'].values
        #question = df_filtered[val:val+1]['@Body'].values[0]
        #answer = df_filtered[val:val+1]['@Answer'].values[0]

        
    return title,question,answer,score
    
@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    print("Index page")

    global title
    global question
    global answer
    global score
    global search_query
    global question_index
    global highlight_enabled
    
    form = SearchForm()
    question_submit = None
    answer_submit = None
    title_submit = None

    print("test1")

    if form.validate_on_submit():

        print("test2")

        # store the submitted values
        submitted_data = form.data
        print(submitted_data)
        print("search" in request.form)

        # Retrieve values from form
        if "search" in request.form:
            question_index = 0
            search_query = submitted_data['search_query']
            title,question,answer,score = lookup_search(search_query)


        if "add" in request.form:
            title[question_index] = submitted_data['search_query']
            #question = submitted_data['question_text']


    # TODO: find a cleaner way to do this
    if "0" in request.form:
        question_index = 0
    if "1" in request.form:
        question_index = 1
    elif "2" in request.form:
        question_index = 2
    elif "3" in request.form:
        question_index = 3
    elif "4" in request.form:            
        question_index = 4
    elif "5" in request.form:            
        question_index = 5

    if "highlight" in request.form:
        if highlight_enabled:
            highlight_enabled = False
        else:
            highlight_enabled = True
    
    # highlight search terms
    title_submit = list(title)
    question_submit = list(question)
    answer_submit = list(answer)
    if highlight_enabled:
        highlight_state = "ON"
        search_terms = search_query.split()
        for term in search_terms:
            if term not in cachedStopWords:
                #pattern = re.compile(term, re.IGNORECASE)
                print(term)
                pattern = re.compile(r'\b(%s)\b' % term, re.IGNORECASE)
                #for idx in range(len(title)):
                idx = question_index
                print "Before: " + title[question_index]
                title_submit[question_index] = pattern.sub('<mark>'+term+'</mark>',title[question_index])
                print "After: " + title[question_index]
                question_submit[question_index] = pattern.sub('<mark>'+term+'</mark>',question[question_index])
                answer_submit[question_index] = pattern.sub('<mark>'+term+'</mark>',answer[question_index])
    else:
        highlight_state = "OFF"
    print(score)

    return render_template('index.html', form=form, title=title_submit, question=question_submit, answer=answer_submit, score=score, question_index=question_index,highlight_state=highlight_state)
