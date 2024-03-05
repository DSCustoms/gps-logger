from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Read all log files
    logs = {}
    for file in os.listdir('/home/pi/gps_logs/'):
        with open(f'/home/pi/gps_logs/{file}', 'r') as f:
            logs[file] = [parse_line(line) for line in f if parse_line(line) is not None]

    return render_template('index.html', logs=logs)

def parse_line(line):
    parts = line.strip().split(',')
    if len(parts) >= 3:
        return {'time': parts[0], 'lat': parts[1], 'lon': parts[2]}
    else:
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
