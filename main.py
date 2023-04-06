from flask import Flask, render_template, request
import configparser

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.ini')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        for section in config.sections():
            for key in config[section]:
                if key in request.form:
                    value = request.form[key]
                    config.set(section, key, value)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
    return render_template('index.html', config=config)


@app.route('/resize', methods=['POST'])
def run():
    import subprocess
    subprocess.Popen(['python', 'resize.py'])
    print('Script is running...')
    return render_template('resize_status.html', status='Script is running...')


if __name__ == '__main__':
    app.run(debug=True, port=int('5099'))
