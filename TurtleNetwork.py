import json
import os
import sys

import pywaves as py
import requests
from flask import Flask, render_template, request, url_for, redirect, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from app.models.Gateway import Gateway
from app.models.Token import Token
from app.models.User import User


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

app.secret_key = "TurtleNetwork"

FEE = 2000000

NODE = 'https://privatenode.blackturtle.eu'
py.setNode(NODE, 'TN', 'L')
py.setMatcher('https://privatematcher.blackturtle.eu')
gateways = []
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def get_addr_gateway(url, addr):
    r = requests.get("https://" + url + ".blackturtle.eu/api/v1/coin-address/" + addr)
    return r.content.decode()


@login_manager.user_loader
def load_user(seed):
    return User(seed)


@app.route('/portfolio')
@login_required
def portfolio():
    result = requests.get(NODE + '/assets/balance/' + current_user.wallet.address)
    balances = json.loads(result.content)['balances']
    portfolio = []
    for balance in balances:
        asset = Token(balance['issueTransaction']['id'], balance['issueTransaction']['decimals'],
                      balance['balance'], balance['issueTransaction']['sender'],
                      balance['issueTransaction']['name'], balance['issueTransaction']['description'])
        portfolio.append(asset)
    return render_template('portfolio.html', portfolio=portfolio)


@app.route('/')
@login_required
def home():
    return render_template('home.html', address=current_user.wallet.address,
                           balance=float(current_user.wallet.balance()) / 10 ** 8,
                           extra_fees=current_user.extra_fees / 10 ** 8)


@app.route('/gateway/overview')
@login_required
def gateways_overview():
    return render_template('gateways.html', gateways=gateways, extra_fees=current_user.extra_fees,
                           address=current_user.wallet.address)


@app.route('/dex')
@login_required
def dex_overview():
    return render_template('dex.html')


@app.route('/alias')
@login_required
def alias_overview():
    return render_template('alias.html', address=current_user.wallet.address, extra_fees=current_user.extra_fees)


@app.route('/data')
@login_required
def data_overview():
    return render_template('data_transfer.html', address=current_user.wallet.address)


@app.route('/asset/create')
@login_required
def asset_create():
    return render_template('asset_create.html')


@app.route('/explorer')
@login_required
def explorer():
    return render_template('explorer.html')


@app.route('/lease/overview')
@login_required
def lease_overview():
    return render_template('lease.html', address=current_user.wallet.address, extra_fees=current_user.extra_fees)


@app.route('/gateway/<gateway>')
@login_required
def gateways_detail(gateway):
    gw: Gateway = next((x for x in gateways if x.name.lower() == gateway.lower()), None)
    index = gateways.index(gw)
    gw.set_personal_wallet(get_addr_gateway(gw.url, current_user.wallet.address))
    gateways[index] = gw
    return json.dumps(gw.__dict__)


@app.route('/gw/send/tn', methods=['POST'], strict_slashes=False)
@login_required
def gw_send_tn():
    data = request.data
    json_data = json.loads(data.decode())
    dest = json_data['addr']
    amount = float(json_data['amount']) * (10 ** 8)
    fee = float(json_data['fee']) * (10 ** 8)
    gateway = py.Address(address=get_addr_gateway('gateway', dest))
    result = current_user.wallet.sendWaves(gateway, int(amount), txFee=int(fee))
    return jsonify(result)


@app.route('/gw/send/<gateway>', methods=['POST'], strict_slashes=False)
@login_required
def gw_send_currencie(gateway):
    gw: Gateway = next((x for x in gateways if x.name.lower() == gateway.lower()), None)
    data = request.data
    gateway = py.Address(address=gw.general_addr)
    json_data = json.loads(data.decode())
    dest = json_data['addr']
    amount = float(json_data['amount']) * (10 ** 8)
    fee = float(json_data['fee']) * (10 ** 8)
    result = current_user.wallet.sendAsset(gateway, py.Asset(gw.asset_id), int(amount), txFee=int(fee), attachment=dest)
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


@app.route('/assets/burn/<asset>', methods=['POST'], strict_slashes=False)
@login_required
def burn_asset(asset):
    py_asset = py.Asset(assetId=asset)
    data = json.loads(request.data.decode())
    amount = float(data['amount']) * (10 ** py_asset.decimals)
    fee = float(data['fee']) * (10 ** 8)
    burn = current_user.wallet.burnAsset(py_asset, int(amount), txFee=int(fee))
    return jsonify(burn)


@app.route('/tn/send/', methods=['POST'], strict_slashes=False)
@login_required
def send_tn():
    data = json.loads(request.data.decode())
    amount = float(data['amount']) * (10 ** 8)
    recipient = data['addr']
    attachment = data['attachment']
    fee = float(data['fee']) * (10 ** 8)
    alias = json.loads(active_alias(recipient))
    if 'address' not in alias:
        send = current_user.wallet.sendWaves(py.Address(address=recipient), int(amount), attachment=attachment,
                                             txFee=int(fee))
    else:
        send = current_user.wallet.sendWaves(py.Address(address=alias['address']), int(amount), attachment=attachment,
                                             txFee=int(fee))
    return jsonify(send)


@app.route('/assets/send/<asset>', methods=['POST'], strict_slashes=False)
@login_required
def send_asset(asset):
    py_asset = py.Asset(assetId=asset)
    data = json.loads(request.data.decode())
    addr = data['addr']
    amount = float(data['amount']) * (10 ** py_asset.decimals)
    fee = float(data['fee']) * (10 ** 8)
    alias = json.loads(active_alias(addr))
    if 'address' not in alias:
        send = current_user.wallet.sendAsset(py.Address(addr), py_asset, int(amount), txFee=int(fee))
    else:
        send = current_user.wallet.sendAsset(py.Address(alias['address']), py_asset, int(amount), txFee=int(fee))

    return jsonify(send)


@app.route('/state/transactions/<addr>/<amount>')
def history_tx(addr, amount):
    r = requests.get(NODE + "/transactions/address/" + addr + "/limit/" + amount)
    return r.content.decode()


@app.route('/address/data/<addr>')
def address_data(addr):
    r = requests.get(NODE + "/addresses/data/" + addr)
    return r.content.decode()


@app.route('/create/alias', methods=['POST'], strict_slashes=False)
@login_required
def create_alias():
    data = json.loads(request.data.decode())
    alias = data['alias']
    fee = float(data['fee']) * (10 ** 8)
    data = current_user.wallet.createAlias(alias, txFee=int(fee))
    return jsonify(data)


@app.route('/state/aliases/by-address/<addr>')
def active_alias_by_addr(addr):
    r = requests.get(NODE + "/alias/by-address/" + addr)
    return r.content.decode()


@app.route('/state/aliases/by-alias/<alias>')
def active_alias(alias):
    r = requests.get(NODE + "/alias/by-alias/" + alias)
    return r.content.decode()


@app.route('/state/leases/<addr>')
def active_leasing(addr):
    r = requests.get(NODE + "/leasing/active/" + addr)
    return r.content.decode()


@app.route('/state/leases/cancel/<id>')
@login_required
def cancel_active_leasing(id):
    send = current_user.wallet.leaseCancel(leaseId=id, txFee=FEE)
    return jsonify(send)


@app.route('/state/leases/start', methods=['POST'], strict_slashes=False)
@login_required
def start_leasing():
    data = json.loads(request.data.decode())
    amount = float(data['amount']) * (10 ** 8)
    recipient = data['addr']
    alias = json.loads(active_alias(recipient))
    if 'address' not in alias:
        send = current_user.wallet.lease(py.Address(address=recipient), int(amount), txFee=FEE)
    else:
        send = current_user.wallet.lease(py.Address(address=alias['address']), int(amount), txFee=FEE)
    return jsonify(send)


@app.route('/details/<assetid>', strict_slashes=False)
@login_required
def details_asset(assetid):
    asset_details = py.Asset(assetId=assetid)
    if asset_details.decimals == 0:
        asset_balance = current_user.wallet.balance(assetId=assetid)
    else:
        asset_balance = current_user.wallet.balance(assetId=assetid) / (10 ** asset_details.decimals)
    asset_smart = asset_details.isSmart()
    return render_template('details.html', asset_details=asset_details, asset_balance=asset_balance,
                           asset_smart=asset_smart, extra_fees=current_user.extra_fees)


@app.route('/login', methods=['POST'], strict_slashes=False)
def do_admin_login():
    data = request.form
    seed = data['seed']
    pk = data['pk']
    login_user(User(pk, seed))
    gateways.append(
        Gateway('----------', '3JbpUeiV6BN9k2cMccKE5LZrrQ8wN44pxWy',
                0.01, 'Waves', 'EzwaF58ssALcUCZ9FbyeD1GTSteoZAQZEDTqBAXHfq8y', 'wavesgateway', 'wB-bg-WAV.png'),
    )
    gateways.append(
        Gateway('----------', '3JnNnw91XQr3pDmpGWud9xGfz9hEF1hSTfG',
                0.006, 'Litecoin', '3vB9hXHTCYbPiQNuyxCQgXF6AvFg51ozGKL9QkwoCwaS', 'litecoingw', 'wB-bg-LTC.png')
    )
    gateways.append(
        Gateway('----------', '3JeW3F1kEWxLsf8zg1uAZRPb7g5z6fuqEfF',
                0.001, 'Bitcoin', '5Asy9P3xjcvBAgbeyiitZhBRJZJ2TPGSZJz9ihDTnB3d', 'bitcoingw', 'wB-bg-BTC.png'))
    gateways.append(
        Gateway('----------', '3JbigZzoGyFWksZ5RLuh9K5ntyGZuXKTVas',
                0.001, 'Dash', 'A62sRG58HFbWUNvFoEEjX4U3txXKcLm11MXWWS429qpN', 'dashgw', 'wB-bg-DASH.png'))
    gateways.append(
        Gateway('----------', '3JsshGBTUXXqShXGQeNdtzw1EuQZFqxN4E3',
                0.03, 'Wagerr', '91NnG9iyUs3ZT3tqK1oQ3ddpgAkE7v5Kbcgp2hhnDhqd', 'wagerrgw', 'wB-bg-WGR.png'))
    gateways.append(
        Gateway('----------', '3JiEjoFbgVKLVxdJYFD1HL9HYDN3RupVNHd',
                0.003, 'Syscoin', 'HBxBjymrCC8TuL8rwCLr2vakDEq4obqkMwYYPEZtTauA', 'syscoingw', 'wB-bg-SYS.png'))
    gateways.append(
        Gateway('----------', '3JsenfjhSNRQsRZMXrkAtJMfjyzxrzSeCKr',
                0.0003, 'BCH', 'Fr2kNhe7XR3E16W7Mfh7NhNcsQWLXx3hSLjoFgpbFsNj', 'bchgw', 'wB-bg-BCH.png'))
    gateways.append(
        Gateway('----------', '3Jve26ckLkBivDbryLzpvoLyoRfxUaAE7tE',
                9, 'Dogecoin', 'HDeemVktm2Z68RMkyA7AexhpaCqot1By7adBzaN9j5Xg', 'dogegw', 'wB-bg-DOG.png'))
    gateways.append(
        Gateway('----------', '3Jbrk85BjtVtEyrVLVVF7yWjKcnGPA6Rk5C',
                0.00041, 'Ethereum', '6Mh41byVWPg8JVCfuwG5CAPCh9Q7gnuaAVxjDfVNDmcD', 'ethgw', 'wB-bg-ETH.png'))
    gateways.append(
        Gateway('----------', '33JgUZ2ytQicRQ1k38Y2nHeR9NxHK5fqEqbu',
                1, 'Afin', 'A8jSBb33GztWpuCypUW9hJYPnTtJGZ7SDuSZfHCaeV49', 'afingw', 'wB-bg-AFIN.png'))

    return redirect(url_for('home'))


def get_free_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    free_port = s.getsockname()[1]
    s.close()
    return free_port


PORT = get_free_port()


def run_server():
    app.run(host='127.0.0.1', port=PORT, threaded=True)


if __name__ == '__main__':
    run_server()

    # init_gui(app, window_title="Turtle Network Wallet", icon="static/favicon.ico")
