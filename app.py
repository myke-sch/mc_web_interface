import subprocess

import psutil
from flask import Flask, request, render_template, redirect, url_for
from rcon.source import Client
from time import sleep
import minecraft_status

app = Flask(__name__)


def rcon_message():
    with Client('212.47.76.18', 25575, passwd='JarryLarry') as client:
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
        with Client('212.47.76.18', 25575, passwd='JarryLarry') as client:
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
def index():
    # error_message = getWhitelistedPlayers(1)
    # return render_template('interface.html', error_message=error_message)

    if minecraft_status.get_info("212.47.76.18", 25565) is not None:
        statusMessage = "Server is running"
        server_information = minecraft_status.get_info("212.47.76.18", 25565)
        # print(server_information)
        playersCount = server_information['players']['online']
        players = server_information
        playersOnline = []
        if 'sample' in server_information['players']:
            print(players['players']['sample'])
            for player in players['players']['sample']:
                print(player)
                playersOnline.append(player['name'])
            return render_template('index.html', statusMessage=statusMessage, players=playersCount,
                                   playerNames=playersOnline)
        return render_template('index.html', statusMessage=statusMessage, players=playersCount)

    else:
        statusMessage = "Server is offline"
        return render_template('index.html', statusMessage=statusMessage)


@app.route('/start')
def start_server():
    process = subprocess.Popen(['.\\test.bat'])
    sleep(20)
    status_message = "Starting the server please wait"

    # server_change("Starting the server please wait")
    # return redirect(url_for('interface',))
    return render_template('server_change.html', status_message=status_message, time=20000,
                           redirectURL=url_for('index'))


@app.route('/serverControl', methods=['POST'])
def controlServer():
    password = request.form.get('passwordField')
    print(password)

    if password == "mika":

        if request.form.get('start'):
            # process = subprocess.Popen(['.\\test.bat'])
            status_message = "Starting the server please wait"
            return render_template('server_change.html', status_message=status_message, time=20000,
                                   redirectURL=url_for('index'))
        if request.form.get('stop'):
            process = subprocess.Popen(['.\\test.bat'])
            status_message = "Stopping the server please wait"
            return render_template('server_change.html', status_message=status_message, time=5000,
                                   redirectURL=url_for('index'))
        if request.form.get('restart'):
            process = subprocess.Popen(['.\\test.bat'])
            status_message = "Restarting the server please wait"
            return render_template('server_change.html', status_message=status_message, time=30000,
                                   redirectURL=url_for('index'))

        else:
            return render_template('error.html')
    else:

        return "Wrong password"


@app.route('/stop')
def stop_server():
    process = subprocess.Popen(['.\\test.bat'])
    status_message = "Stopping the server please wait"
    return render_template('server_change.html', status_message=status_message, time=5000, redirectURL=url_for('index'))


@app.route('/restart')
def restart_server():
    process = subprocess.Popen(['.\\test.bat'])
    sleep(30)
    status_message = "Restarting the server please wait"
    return render_template('server_change.html', status_message=status_message, time=30000,
                           redirectURL=url_for('index'))


@app.route('/whitelist', methods=["GET", "POST"])
def whitelistPlayer():
    subprocess.call(["screen", "-S", "minecraft", "-p", "0", "-X", "stuff", "'say test^M"])
    sleep(3)
    return redirect(url_for('index'))


# siehe ChatGpt
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
