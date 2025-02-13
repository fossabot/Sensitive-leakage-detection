from flask import Flask, request, render_template
import joblib
import os

script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)

# 初始化 Flask 应用
app = Flask(__name__)

# 加载模型和向量化器
model = joblib.load('model/logistic_regression_model.pkl')
vectorizer = joblib.load('model/count_vectorizer.pkl')

# 定义预测函数
def predict_text(text, model, vectorizer):
    """
    使用加载的模型和向量化器对输入文本进行预测
    """
    # 将输入文本转换为特征向量
    text_counts = vectorizer.transform([text])
    
    # 进行预测
    prediction = model.predict(text_counts)
    print(prediction)
    return prediction[0]

# 定义主页路由
@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    result = ['normal/正常', 'weak/弱口令', 'tokens/令牌']
    if request.method == 'POST':
        input_text = request.form['text']
        prediction = predict_text(input_text, model, vectorizer)
    return render_template('index.html', prediction=result[prediction] if prediction is not None else None)

# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)