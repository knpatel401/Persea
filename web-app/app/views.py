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
from sklearn.preprocessing import Normalizer
import pandas as pd
 
cachedStopWords = stopwords.words("english")
NUM_RESULTS = 10
title = []
question = []
answer = []
category = []
score = []
search_query = ''
title_query = ''
highlight_enabled = False
question_index = 0

class SearchForm(Form):
    """Fields for Search"""
    search_query = fields.StringField('Search Query:', validators=[])
    title_query = fields.StringField('', validators=[])
    question_query = fields.TextAreaField('', validators=[])
    answer_query = fields.TextAreaField('', validators=[])
    submit = fields.SubmitField('Submit')

def lookup_search(query):
    from IPython.core.display import display, HTML
    
    test_text = [query,query]
    dtm_test = vectorizer.transform(test_text) 
    dtm_test_lsa = lsa.transform(dtm_test)
    dtm_test_lsa = Normalizer(copy=False).transform(dtm_test_lsa)

    dot_prods = (np.matrix(dtm_test_lsa[0])*np.matrix(dtm_lsa).transpose())
    test = dot_prods.tolist()[0]
    #val= test.index(max(test))
    #print("Score = " + str(max(test)))
    
    if max(test) == 0:
        question = ['N/A']
        answer = ['N/A']
        category = ['N/A']
        title = ["<font color=\"red\">Sorry, no search result found</font>"]
        score = "0"
        return title,question,answer,category,score
    else:
        max_vals = heapq.nlargest(NUM_RESULTS, enumerate(test), key=lambda x: x[1])
        max_indices = [x[0] for x in max_vals]
        print max_indices
        score = [round(x[1],2) for x in max_vals]
        title = df_filtered.iloc[max_indices]['@Title'].values
        question = df_filtered.iloc[max_indices]['@Body'].values
        answer = df_filtered.iloc[max_indices]['@Answer'].values
        category = df_filtered.iloc[max_indices]['Category'].values

    return title,question,answer,category,score

def add_entry(new_title, new_question, new_answer):
    global df_filtered
    global dtm_lsa
    
    # add row to database
    new_row = pd.Series([new_title,new_question,new_answer,'','UserInput'],index=['@Title', '@Body', '@Answer', '@Tags', 'Category'])
    df_filtered = df_filtered.append(new_row, ignore_index=True)

    # calculate lsa components for new entry and add to dtm_lsa
    query = new_title
    test_text = [query,query]
    dtm_test = vectorizer.transform(test_text)
    dtm_test_lsa = lsa.transform(dtm_test)
    dtm_test_lsa = Normalizer(copy=False).transform(dtm_test_lsa)
    dtm_lsa = np.append(dtm_lsa, [dtm_test_lsa[0]],axis=0)
    a = dtm_test_lsa[0]
    
@app.route('/', methods=('GET', 'POST'))
def index():
    """Index page"""
    print("Index page")

    global title
    global question
    global answer
    global category
    global score
    global search_query
    global question_index
    global highlight_enabled
    
    form = SearchForm()
    question_submit = None
    answer_submit = None
    category_submit = None
    title_submit = None

    if form.validate_on_submit():

        # store the submitted values
        submitted_data = form.data
        print(submitted_data)
        print("search" in request.form)

        # Retrieve values from form
        if "search" in request.form:
            question_index = 0
            search_query = submitted_data['search_query']
            title,question,answer,category,score = lookup_search(search_query)

        if "add" in request.form:
            add_entry(submitted_data['title_query'],
                      submitted_data['question_query'],
                      submitted_data['answer_query'])

        if "view" in request.form:
            print "VIEW"
            if len(question) ==0:
                title.append(submitted_data['title_query'])
                question.append(submitted_data['question_query'])
                answer.append(submitted_data['answer_query'])
            else:
                title[question_index] = submitted_data['title_query']
                question[question_index] = submitted_data['question_query']
                answer[question_index] = submitted_data['answer_query']
            highlight_state = False
            return render_template('view.html', form=form, title=title, question=question,
                                   answer=answer, category=category,score=score,
                                   question_index=question_index,highlight_state=highlight_state)

        if "edit" in request.form:
            print "EDIT"
            if len(question) > question_index:
                form.title_query.process_data(title[question_index])
                form.question_query.process_data(question[question_index])
                form.answer_query.process_data(answer[question_index])
            highlight_state = False
            return render_template('edit.html', form=form, title=title_submit, question=question_submit,
                                   answer=answer_submit, category=category, score=score,
                                   question_index=question_index,highlight_state=highlight_state)


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
    elif "6" in request.form:            
        question_index = 6
    elif "7" in request.form:            
        question_index = 7
    elif "8" in request.form:            
        question_index = 8
    elif "9" in request.form:            
        question_index = 9
    print request.form
    if "highlight" in request.form:
        if highlight_enabled:
            highlight_enabled = False
        else:
            highlight_enabled = True
    
    # highlight search terms
    title_submit = list(title)
    question_submit = list(question)
    answer_submit = list(answer)
    category_submit = list(category)
    if highlight_enabled:
        highlight_state = True
        search_terms = search_query.split()
        print search_terms
        for term in search_terms:
            if term not in cachedStopWords:
                #pattern = re.compile(term, re.IGNORECASE)
                print(term)
                pattern = re.compile(r'\b(%s)\b' % term, re.IGNORECASE)
                #for idx in range(len(title)):
                idx = question_index
                title_submit[question_index] = pattern.sub('<mark>'+term+'</mark>',title_submit[question_index])
                question_submit[question_index] = pattern.sub('<mark>'+term+'</mark>',question_submit[question_index])
                answer_submit[question_index] = pattern.sub('<mark>'+term+'</mark>',answer_submit[question_index])
    else:
        highlight_state = False
    print(score)

    print "SEARCH"

    return render_template('search.html', form=form, title=title_submit, question=question_submit,
                           answer=answer_submit, category=category, score=score,
                           question_index=question_index, highlight_state=highlight_state)
