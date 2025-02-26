#use port 8080

import http.server
import socketserver
import os

# Configuration
PORT = 8080  # Change if needed
UPLOAD_DIR = "uploads"  # Directory where files will be stored

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileUploadHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """Serve a simple file upload HTML form."""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"""
        <html>
        <body>
            <h2>Upload File</h2>
            <form action="/" method="post" enctype="multipart/form-data">
                <input type="file" name="file">
                <input type="submit" value="Upload">
            </form>
        </body>
        </html>
        """)

    def do_POST(self):
        """Handle file upload via HTTP POST request."""
        content_length = int(self.headers['Content-Length'])
        boundary = self.headers.get('Content-Type').split("boundary=")[-1].encode()
        body = self.rfile.read(content_length)

        # Extract file content
        parts = body.split(b'--' + boundary)
        for part in parts:
            if b'filename="' in part:
                headers, file_data = part.split(b'\r\n\r\n', 1)
                filename = headers.split(b'filename="')[1].split(b'"')[0].decode()

                # Save the uploaded file
                filepath = os.path.join(UPLOAD_DIR, filename)
                with open(filepath, "wb") as f:
                    f.write(file_data.strip(b'\r\n--'))

                self.send_response(200)
                self.end_headers()
                self.wfile.write(f"File {filename} uploaded successfully!".encode())
                return

        self.send_response(400)
        self.end_headers()
        self.wfile.write(b"Invalid request!")

# Start the server
with socketserver.TCPServer(("", PORT), FileUploadHandler) as httpd:
    print(f"File upload server running on http://0.0.0.0:{PORT}")
    httpd.serve_forever()
