from flask import Flask, request, render_template
import joblib
import os
from model.predict import load_model_and_vectorizer,predict_text

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

# 初始化 Flask 应用
app = Flask(__name__)

# 加载模型和向量化器
model, vectorizer = load_model_and_vectorizer('model/GaussianNB.pkl', 'model/tfidf_vectorizer.pkl')

# 定义主页路由
@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    result = ['正常文本', '弱口令', '令牌']
    if request.method == 'POST':
        input_text = request.form['text']
        prediction = predict_text(input_text, model, vectorizer)
    return render_template('index.html', prediction='{} = {}'.format(input_text,result[prediction]) if prediction is not None else None)

# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)