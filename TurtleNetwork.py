import pywaves as py
##hypercorn app:app -b 0.0.0.0:4000 -w 3
# import quart.flask_patch
import requests
import json
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from pyfladesk import init_gui

PORT = 4000
app = Flask(__name__)
app.secret_key = "TurtleNetwork"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

py.setNode('https://privatenode.blackturtle.eu', 'TN', 'L')
py.setMatcher('https://privatematcher.blackturtle.eu')
gateways = []


class User(UserMixin):
    def __init__(self, seed):
        self.id = seed
        self.wallet = self.get_wallet()

    def get_wallet(self):
        return py.Address(seed=self.id)


class Gateway():
    def __init__(self, personal_addr, general_addr, fee, name, assetId):
        self.personal_addr = personal_addr
        self.general_addr = general_addr
        self.fee = fee
        self.name = name
        self.assetId = assetId


def get_addr_gateway(url, addr):
    r = requests.get("https://" + url + ".blackturtle.eu/api/v1/coin-address/" + addr)
    return r.content.decode()


@login_manager.user_loader
def load_user(seed):
    return User(seed)


@app.route('/')
@login_required
def home():
    return render_template('home.html', address=current_user.wallet.address,
                           balance=float(current_user.wallet.balance()) / 10 ** 8,
                           gateways=gateways)

@app.route('/gw/send/tn', methods=['POST'], strict_slashes=False)
@login_required
def send_tn():
    data = request.data
    dataJ = json.loads(data.decode())
    dest = dataJ['addr']
    amount = float(dataJ['amount']) * (10 ** 8)
    gateway = py.Address(address=get_addr_gateway('gateway',dest))
    result = current_user.wallet.sendWaves(gateway, int(amount), txFee=2000000)
    return jsonify(result)

@app.route('/gw/send/<gateway>', methods=['POST'], strict_slashes=False)
@login_required
def send_currencie(gateway):
    gw: Gateway = next((x for x in gateways if x.name == gateway), None)
    data = request.data
    gateway = py.Address(address=gw.general_addr)
    dataJ = json.loads(data.decode())
    print(dataJ)
    dest = dataJ['addr']
    amount = float(dataJ['amount']) * (10 ** 8)
    result = current_user.wallet.sendAsset(gateway, py.Asset(gw.assetId), int(amount), txFee=2000000, attachment=dest)
    return jsonify(result)


@app.route('/logout', methods=['GET'], strict_slashes=False)
@login_required
def do_logout():
    logout_user()
    gateways.clear()
    return login()


@app.route('/login', methods=['GET'], strict_slashes=False)
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'], strict_slashes=False)
def do_admin_login():
    data = request.form
    seed = data['seed']
    login_user(User(seed))
    gateways.append(
        Gateway(get_addr_gateway("wavesgateway", current_user.wallet.address), '3JbpUeiV6BN9k2cMccKE5LZrrQ8wN44pxWy',
                0.01, 'waves', 'EzwaF58ssALcUCZ9FbyeD1GTSteoZAQZEDTqBAXHfq8y'))
    return redirect(url_for('home'))


if __name__ == '__main__':
    print("start app")
    init_gui(app,window_title="Turtle Network Wallet",)
