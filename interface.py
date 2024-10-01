from flask import Flask, render_template, request, redirect, url_for
import requests
import json


@app.route('/interface')
def interface():
    return render_template('../templates/interface.html')

@app.route('/interface/start')
def start_server():
    print("Test")
    return "Success"
    #return redirect(url_for('interface'))