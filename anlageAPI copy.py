import anlageTurnTableController
from flask import Flask, render_template, request

turntables = {
    231: anlageTurnTableController.AnlageController("192.168.200.231"),
    232: anlageTurnTableController.AnlageController("192.168.200.232"),
    233: anlageTurnTableController.AnlageController("192.168.200.233"),
    234: anlageTurnTableController.AnlageController("192.168.200.234")
    # Add more turntables and their addresses here
}
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<turntable>/ejectA')
def ejectA(turntable):
    anlageTurntable = turntables[int(turntable)]
    anlageTurntable.ejector_a("eject")
    return render_template('response.html', response="ejectedA")

@app.route('/<turntable>/ejectB')
def ejectB(turntable):
    anlageTurntable = turntables[int(turntable)]
    anlageTurntable.ejector_b("eject")
    return render_template('response.html', response="ejectedB")

@app.route('/<turntable>/turn')
def turn(turntable):
    anlageTurntable = turntables[int(turntable)]
    anlageTurntable.turn_turn_table()
    return render_template('response.html', response="turned")

@app.route('/<turntable>/borePart')
def borePart(turntable):
    anlageTurntable = turntables[int(turntable)]
    anlageTurntable.bore_part()
    return render_template('response.html', response="bored")

@app.route('/<turntable>/start')
def start(turntable):
    anlageTurntable = turntables[int(turntable)]
    anlageTurntable.default_behaviour(True)
    return render_template('response.html', response="started")

@app.route('/<turntable>/stop')
def stop(turntable):
    anlageTurntable = turntables[int(turntable)]
    anlageTurntable.default_behaviour(False)
    return render_template('response.html', response="stopped")

@app.route('/<turntable>/checkPart')
def checkpart(turntable):
    anlageTurntable = turntables[int(turntable)]
    if anlageTurntable.check_part() == True:
        return render_template('response.html', response="check:true")
    else:
        return render_template('response.html', response="check:false")

@app.route('/<turntable>/send-message', methods=['POST', 'GET'])
def sendmessage(turntable):
    anlageTurntable = turntables[int(turntable)]
    message = request.form.get('message')
    response = ""

    # Handle different messages and perform desired actions
    if message != "/disconnect":
        if message == "ejectB":
                response = "Ejected part"
                anlageTurntable.ejector_b("eject")
        elif message == "ejectA":
            response = "Ejected part."
            anlageTurntable.ejector_a("eject")
        elif message == "turn":
            response = "Turned."
            anlageTurntable.turn_turn_table()
        elif message == "borePart":
            response = "Bored part."
            anlageTurntable.bore_part()
        elif message == "start":
            response = "Starting Default-Routine."
            anlageTurntable.default_behaviour(True)
        elif message == "stop":
            response = "Stopping Default-Routine."
            anlageTurntable.default_behaviour(False)
        elif message == "checkPart":
            if anlageTurntable.check_part() == True:
                response = "Part Check: True"
            else:
                response = "Part Check: False"

    return render_template('index.html', response=response, ip = turntable)

if __name__ == '__main__':
    app.run(host='192.168.200.176', port=5000)
