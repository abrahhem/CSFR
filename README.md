# Anti-CSRF Protection in Python Server

This project demonstrates how to implement protection against Cross-Site Request Forgery (CSRF) attacks in a Python server. The server provides a purchasing page where the user is required to confirm their purchase by submitting a form with an anti-CSRF token.

## Installation

1. Clone the repository to your local machine:
```bash
git clone https://github.com/abrahhem/CSFR.git
```
2. Install the required dependencies. Assuming you have Python installed, run the following command:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
    python server.py
```
2. Access the shoes list page by opening your web browser and navigating to http://localhost:8000/.

3. Fill out the form on the purchasing page, and when you click "Buy Now," you will be presented with an "Are you sure?" form.

4. In the "Are you sure?" form, you will find a hidden input field named csrf containing a random anti-CSRF token. This token is unique to the user's session and helps protect against CSRF attacks.

5. Submit the "Are you sure?" form, and the server will validate the anti-CSRF token.
