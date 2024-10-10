import subprocess

import psutil
from flask import Flask, request, render_template, redirect, url_for
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


def getWhitelistedPlayers(outputMode):
    playerList = []
    playerListOutput = []
    try:
        with Client('62.171.167.28', 25575, passwd='JarryLarry') as client:
            response = client.run('whitelist list')

        response = response[35:]
        response = response.replace("'", "")
        response = response.replace(",", "")
        for i in response.split():
            playerList.append(i.lower())
            playerListOutput.append(i)
        # print(i)
        # print(response[35:])

        print(playerList)
        outputString = "Whitelisted Players: \n"
        for n in playerListOutput:
            outputString += "\t" + n + "\n"

        if outputMode:
            return outputString
        else:
            return playerList
    except:
        error_message = "Could not load Whitelist"
        print("Error could not connect to Server")
        return error_message


@app.route("/")
def interface():
    error_message = getWhitelistedPlayers(1)
    return render_template('interface.html', error_message=error_message)


@app.route('/start')
def start_server():
    process = subprocess.Popen(['.\\test.bat'])
    status_message = "Starting the server please wait"
    # server_change("Starting the server please wait")
    # return redirect(url_for('interface',))
    return render_template('server_change.html', status_message=status_message, redirectURL=url_for('interface', ))


@app.route('/stop')
def stop_server():
    process = subprocess.Popen(['.\\test.bat'])
    status_message = "Stopping the server please wait"
    return render_template('server_change.html', status_message=status_message, redirectURL=url_for('interface', ))


@app.route('/restart')
def restart_server():
    process = subprocess.Popen(['.\\test.bat'])
    status_message = "Restarting the server please wait"
    return render_template('server_change.html', status_message=status_message, redirectURL=url_for('interface', ))


@app.route('/whitelist', methods=["GET", "POST"])
def whitelistPlayer():
    if request.method == "POST":
        username = request.form['username']
        if username.lower() in getWhitelistedPlayers(0):
            return "You are already whitelisted"
        else:
            command: str = "whitelist add " + username
            with Client('62.171.167.28', 25575, passwd='JarryLarry') as client:
                response = client.run(command)

            responseCMD: str = response

        if responseCMD == "Added " + username.lower() + " to the whitelist":
            return "Whitelist was succesful"
        else:
            return redirect(url_for('interface'))

#siehe ChatGpt
@app.route('/removeWl', methods=["GET", "POST"])
def removeWhitelist():
    if request.method == "POST":
        username = request.form['username']
        print(username.lower())
        if username.lower() in getWhitelistedPlayers(0):
            command: str = "whitelist remove " + username
            with Client('62.171.167.28', 25575, passwd='JarryLarry') as client:
                response = client.run(command)

            responseCMD: str = response

            if responseCMD == "Removed " + username.lower() + " from the whitelist":
                return "Whitelist was succesful"
            else:
                return redirect(url_for('interface'))
        else:
            return "Player not found"


if __name__ == '__main__':
    app.run(debug=True)
