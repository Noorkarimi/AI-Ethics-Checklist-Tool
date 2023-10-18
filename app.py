from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        responses = request.form
        # Here you can process the responses, save to a database, etc.
        return "Responses submitted successfully"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

