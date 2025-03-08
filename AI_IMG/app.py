from flask import Flask, render_template, request, redirect, url_for, flash
import openai
import os

app = Flask(__name__)
#app.secret_key = os.getenv('SECRET_KEY', 'fallback_key')
#openai.api_key = "xxxx-proj-xxxx-xxxx-xxxx"  

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        if not prompt:
            flash('Please provide a prompt.', 'warning')
            return redirect(url_for('home'))

        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"
            )
            image_url = response['data'][0]['url']
            return render_template('result.html', image_url=image_url, prompt=prompt)
        except openai.error.OpenAIError as e:
            flash(f"Error generating image: {str(e)}", "danger")
            return redirect(url_for('home'))
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
