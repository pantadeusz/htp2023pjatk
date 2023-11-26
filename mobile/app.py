from flask import Flask, render_template, send_file

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')

if __name__ == '__main__':
    app.run()
