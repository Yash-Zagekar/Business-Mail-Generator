from flask import Flask, request, jsonify
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text

app = Flask(__name__)

chain = Chain()
portfolio = Portfolio()

# Root endpoint
@app.route("/")
def root():
    return jsonify({"message": "Welcome to the Flask Backend!"})

# Endpoint to generate email
@app.route("/generate_email/", methods=["GET"])
def generate_email():
    try:
        url = request.args.get('url')
        if not url:
            return jsonify({"error": "URL parameter is missing"}), 400

        loader = WebBaseLoader([url])
        data = clean_text(loader.load().pop().page_content)
        portfolio.load_portfolio()
        jobs = chain.extract_jobs(data)

        emails = []
        for job in jobs:
            skills = job.get('skills', [])
            links = portfolio.query_links(skills)
            email = chain.write_mail(job, links)
            emails.append(email)

        return jsonify({"emails": emails})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
