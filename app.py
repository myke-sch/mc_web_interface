from flask import Flask, request, render_template, redirect, url_for
import subprocess
import firstStart
import psutil
from time import sleep
from rcon.source import Client

app = Flask(__name__)


def rcon_message():
    with Client('62.171.167.28', 25575, passwd='JarryLarry') as client:
        response = client.run('list')

    print(response)


def test_pusutil():
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        if 'cmd' in proc.info['name']:
            print(proc.info)

def getWhitelistedPlayers():

    playerList = []
    with Client('62.171.167.28', 25575, passwd='JarryLarry') as client:
        response = client.run('whitelist list')

    response = response[35:]
    response = response.replace("'", "")
    response = response.replace(",", "")
    for i in response.split():
        playerList.append(i.lower())
        #print(i)
    #print(response[35:])

    print(playerList)
    return playerList


@app.route("/")
def interface():
    getWhitelistedPlayers()
    return render_template('interface.html')


@app.route('/start')
def start_server():
    process = subprocess.Popen(['.\\test.bat'])
    return redirect(url_for('interface'))


@app.route('/whitelist', methods=["GET", "POST"])
def whitelistPlayer():
    if request.method == "POST":
        username = request.form['username']
        if username.lower() in getWhitelistedPlayers():
            return "You are already whitelisted"
        else:
            command: str = "whitelist add " + username
            with Client('62.171.167.28', 25575, passwd='JarryLarry') as client:
                response = client.run(command)

            responseCMD : str = response


        if responseCMD == "Added " +  username.lower() +  " to the whitelist":
            return "Whitelist was succesful"
        else:
            return redirect(url_for('interface'))


if __name__ == '__main__':
    app.run()
