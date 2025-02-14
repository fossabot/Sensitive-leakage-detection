from flask import Flask, request, render_template
import joblib
import os
from model.predict import load_model_and_vectorizer, predict_text

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

# 初始化 Flask 应用
app = Flask(__name__)

# 加载模型和向量化器
model, vectorizer = load_model_and_vectorizer('model/GaussianNB.pkl', 'model/tfidf_vectorizer.pkl')

# 定义主页路由
@app.route('/', methods=['GET', 'POST'])
def home():
    predictions = None
    result = ['正常文本', '弱口令', '令牌']
    if request.method == 'POST':
        input_text = request.form['text']
        lines = input_text.split('\n')
        predictions = {}
        for line in lines:
            prediction = predict_text(line.strip(), model, vectorizer)
            predictions[line.strip()] = result[prediction]
    return render_template('index.html', predictions=predictions)

# 运行 Flask 应用
if __name__ == '__main__':
    app.run('0.0.0.0',port=5001,debug=True)