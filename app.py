from flask import Flask, request, send_file, render_template_string
from pytube import YouTube
import os

app = Flask(__name__)
//assalamualaikum
@app.route('/')
def home():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YouTube Downloader</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
        </head>
        <body>
            <div class="container" style="margin-top: 50px;">
                <h4 class="center-align">YouTube Downloader</h4>
                <form method="post" action="/download">
                    <div class="input-field">
                        <input type="text" name="url" id="url" required>
                        <label for="url">YouTube URL</label>
                    </div>
                    <div class="input-field">
                        <select name="format" id="format" required>
                            <option value="" disabled selected>Choose format</option>
                            <option value="mp4">MP4</option>
                            <option value="mp3">MP3</option>
                        </select>
                        <label for="format">Select Format</label>
                    </div>
                    <div class="input-field">
                        <select name="resolution" id="resolution" required>
                            <option value="" disabled selected>Choose resolution</option>
                            <option value="720p">720p</option>
                            <option value="480p">480p</option>
                            <option value="360p">360p</option>
                        </select>
                        <label for="resolution">Select Resolution</label>
                    </div>
                    <div class="center-align">
                        <button type="submit" class="btn waves-effect waves-light">Download</button>
                    </div>
                </form>
            </div>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
            <script>
                document.addEventListener('DOMContentLoaded', function() {
                    var elems = document.querySelectorAll('select');
                    M.FormSelect.init(elems, {});
                });
            </script>
        </body>
        </html>
    ''')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.form['url']
    format = request.form['format']
    resolution = request.form['resolution']
    
    yt = YouTube(url)
    title = yt.title
    stream = yt.streams.filter(res=resolution).first()
    if format == 'mp4':
        file_extension = '.' + stream.mime_type.split('/')[1]
    else:
        stream = yt.streams.filter(only_audio=True).first()
        file_extension = '.mp3'
    
    output_file = stream.download(filename=title)
    base, ext = os.path.splitext(output_file)
    new_file = base + file_extension
    os.rename(output_file, new_file)
    
    return send_file(new_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=8100)

