import yfinance as yf
import smtplib
import ssl
import json  # NEW: We need this to read the incoming email from the user
from http.server import BaseHTTPRequestHandler # NEW: Vercel's way to handle web requests

# --- This is our main function that Vercel will call ---
class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # 1. Get the user's email from the request
        content_len = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(content_len)
        body_data = json.loads(raw_body)
        
        # Get the 'email' that our website form will send
        # We add a fallback 'default' for safety
        receiver_email = body_data.get('email', 'default@example.com')
        
        # Check if we got a real email
        if receiver_email == 'default@example.com' or '@' not in receiver_email:
            self.send_response(400) # Bad Request
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'A valid email is required'}).encode())
            return

        try:
            # 2. Fetch the market data (same as before)
            stock_ticker = "MSFT"
            crypto_ticker = "BTC-USD"
            commodity_ticker = "GC=F"

            msft = yf.Ticker(stock_ticker)
            btc = yf.Ticker(crypto_ticker)
            gold = yf.Ticker(commodity_ticker)

            msft_price = msft.info['previousClose']
            btc_price = btc.info['previousClose']
            gold_price = gold.info['previousClose']

            # 3. Format the email message (same as before)
            email_subject = "Here's Your Market Intelligence Demo"
            email_body = f"""
Hi,

Here is your on-demand market intelligence report.

--- STOCKS ---
Microsoft ({stock_ticker}): ${msft_price:,.2f}

--- CRYPTO ---
Bitcoin ({crypto_ticker}): ${btc_price:,.2f}

--- COMMODITIES ---
Gold ({commodity_ticker}): ${gold_price:,.2f}
"""
            
            # 4. Email Configuration (!! USE YOUR APP PASSWORD !!)
            SENDER_EMAIL = "favour.afolayan.dev@gmail.com"
            SENDER_PASSWORD = "tpubujrdzgdyryor"
            
            final_email_message = f"""\
From: {SENDER_EMAIL}
To: {receiver_email}
Subject: {email_subject}

{email_body}
"""
            
            # 5. Send the email (same as before)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, receiver_email, final_email_message)

            # 6. Send a "Success" response back to the website
            self.send_response(200) # 200 means "OK"
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Send a nice message back to the frontend
            self.wfile.write(json.dumps({'message': f'Email sent to {receiver_email}!'}).encode())

        except Exception as e:
            # 7. Send an "Error" response if anything fails
            self.send_response(500) # 500 means "Internal Server Error"
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
            
        return