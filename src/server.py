#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, redirect, url_for

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['json'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/social/moment', methods=['GET', 'POST'])
def update_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'exported_sns.json'))
            return '<!doctype html><title>File uploaded</title><h1>File uploaded</h1>'
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        '''

app.run(host="0.0.0.0")