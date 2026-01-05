from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import datetime
import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build

__version__ = "0.6.0"

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

# This is a placeholder for your client secrets file.
# You will need to replace this with your own credentials.
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']


def get_current_timestamp():
    """Gets the current timestamp and formats it."""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S.%f")

def get_uploaded_files():
    """Gets a list of uploaded files."""
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return [f for f in os.listdir(upload_folder) if f != '.gitkeep']

def process_command(command):
    """Processes a user command."""
    if command.lower() == 'list files':
        files = get_uploaded_files()
        return "<br>".join(files) if files else "No files found."
    elif command.lower() == 'clear uploads':
        for f in get_uploaded_files():
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], f))
        return "All uploaded files have been deleted."
    else:
        return f"Unknown command: {command}"

@app.route('/')
def index():
    """Renders the main page."""
    timestamp = get_current_timestamp()
    files = get_uploaded_files()
    drive_configured = os.path.exists(CLIENT_SECRETS_FILE)
    return render_template('index.html', timestamp=timestamp, version=__version__, files=files, drive_configured=drive_configured)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash("No file part", "danger")
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash("No selected file", "danger")
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        base, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            filename = f"{base}_{counter}{extension}"
            counter += 1
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f"File '{filename}' has been uploaded successfully.", "success")
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Deletes a file."""
    filename = secure_filename(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        flash(f"File '{filename}' has been deleted.", "success")
    else:
        flash(f"File '{filename}' not found.", "danger")
    return redirect(url_for('index'))

@app.route('/command', methods=['POST'])
def handle_command():
    command = request.form.get('command')
    if command:
        flash(process_command(command))
    return redirect(url_for('index'))

@app.route('/authorize')
def authorize():
    """Redirects to the Google authorization page."""
    if not os.path.exists(CLIENT_SECRETS_FILE):
        flash("Google Drive is not configured. Please add your client_secret.json file.")
        return redirect(url_for('index'))
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_url, state = flow.authorization_url(
        access_type='offline', include_granted_scopes='true')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    """Handles the OAuth2 callback."""
    state = session['state']
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for('oauth2callback', _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('list_drive_files'))

@app.route('/drive_files')
def list_drive_files():
    """Lists files in the user's Google Drive."""
    if 'credentials' not in session:
        return redirect('authorize')
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])
    drive = build('drive', 'v3', credentials=credentials)
    results = drive.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    return render_template('drive_files.html', files=items)

if __name__ == "__main__":
    # This is important to allow HTTP for local development.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.run(debug=True, host='0.0.0.0', port=8080)
