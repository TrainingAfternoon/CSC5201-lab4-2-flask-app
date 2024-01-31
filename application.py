from flask import Flask, render_template
from fortune import fortune

import cowsay

application = app = Flask(__name__)

@application.route('/')
def get_fortune() -> str:
    ret = cowsay.get_output_string('cow', fortune())
    return render_template('index.html', user_fortune=ret)

if __name__ == "__main__":
    application.run()
