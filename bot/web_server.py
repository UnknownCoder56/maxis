"""
Flask web server for bot status page
"""

import threading
from flask import Flask, send_from_directory
from bs4 import BeautifulSoup
from discord.ext import commands

from bot.main import Main
from bot.helper import resource_path

app = Flask(__name__, static_folder=str(resource_path("public")), static_url_path="/")

# Store the HTML template
HTML_TEMPLATE = None


def load_html_template():
    """Load and prepare HTML template"""
    global HTML_TEMPLATE
    try:
        html_path = resource_path("index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            HTML_TEMPLATE = f.read()
    except Exception as e:
        print(f"Error loading HTML template: {e}")
        HTML_TEMPLATE = ""


@app.route("/")
def index():
    """Serve bot status page"""
    if HTML_TEMPLATE is None:
        load_html_template()

    # Generate invite link
    invite_url = "https://discord.com/api/oauth2/authorize?client_id=891518158790361138&permissions=8&scope=bot"

    # Parse HTML and update invite link
    soup = BeautifulSoup(HTML_TEMPLATE if HTML_TEMPLATE else "", "html.parser")

    # Find and update invite link
    invite_link = soup.find("a", class_="button")
    if invite_link and "Invite it to your server" in invite_link.get_text():
        invite_link["href"] = invite_url

    # Update bot status
    status_paragraphs = soup.find_all("p", align="center")
    for p in status_paragraphs:
        if "Bot status:" in p.get_text():
            p.string = f"Bot status: Online - {len(globalBot.guilds)} servers"
            break

    return str(soup)


@app.route("/<path:filename>")
def public_files(filename):
    """Serve static files from public directory"""
    return send_from_directory(str(resource_path("public")), filename)


def start_web_server(bot: commands.Bot, port: int = 8080):
    global globalBot
    globalBot = bot
    """Start Flask web server in a separate thread"""

    def run_server():
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    print(f"Web server started on http://localhost:{port}/")
