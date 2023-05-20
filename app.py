import http.server
import socketserver
import secrets
import os

PORT = 8080

# Generate a random CSRF token
def generate_csrf_token():
    return secrets.token_hex(16)


class ShoeStoreHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            shoes_html_list = ''
            shoe_template = '''
                <div class="shoe-item">
                    <img class="shoe-image" src="/shoe/{}" alt="Shoe {}">
                    <h3>Shoe {}</h3>
                    <a class="buy-button" href="/purchase/{}">Buy Now $</a>
                </div>
            '''
            shoes = sorted(os.listdir('./templates/images'))
            for i, shoe in enumerate(shoes, start=1):
                shoes_html_list += shoe_template.format(shoe, i, i, i)

            with open('./templates/index.html', 'r') as file:
                html = file.read()
                html = html.replace('{{ shoes }}', shoes_html_list)

            self.wfile.write(html.encode())

        elif self.path.startswith('/shoe/'):
            shoe_id = self.path.split('/')[-1].split('.')[0]
            image_path = f'./templates/images/{shoe_id}.jpeg'
            try:
                with open(image_path, 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_response(404)
                self.end_headers()

        elif self.path.startswith('/purchase/'):
            shoe_id = self.path.split('/')[-1]
            csrf_token = generate_csrf_token()
            session['csrf_tokens'].append(csrf_token)
            shoe_img = f'shoe{shoe_id}.jpeg'
            with open('./templates/purchase.html', 'r') as file:
                html = file.read()
                html = html.replace('{{ csrf_token }}', csrf_token)
                html = html.replace('{{ shoe_img }}', shoe_img)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html.encode())

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/confirm':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode()

            # Initialize variables to store the extracted values
            auth = ''
            submitted_token = ''

            # Split the post_data string by '&' to get individual key-value pairs
            pairs = post_data.split('&')

            # Extract the values of auth and csrf
            for pair in pairs:
                key, value = pair.split('=')
                if key == 'auth':
                    auth = value
                elif key == 'csrf':
                    submitted_token = value
 
            if submitted_token in session['csrf_tokens']:
                session['csrf_tokens'].remove(submitted_token)
                if auth == "yes":
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    with open('./templates/confirmation.html', 'r') as file:
                        html = file.read()
                    self.wfile.write(html.encode())
                else:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    with open('./templates/cancel.html', 'r') as file:
                        html = file.read()
                    self.wfile.write(html.encode())
            else:
                self.send_response(403)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('./templates/csrf_error.html', 'r') as file:
                    html = file.read()
                self.wfile.write(html.encode())
            

        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    session = {
        'csrf_tokens': []
    }

    with socketserver.TCPServer(("", PORT), ShoeStoreHandler) as httpd:
        print(f"Server running on port {PORT}")
        httpd.serve_forever()
