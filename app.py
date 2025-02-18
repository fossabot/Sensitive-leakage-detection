from flask import Flask, request, render_template, send_file
import joblib
import os
import pandas as pd
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
    download_link = None
    result = ['正常文本', '弱口令', '令牌']
    if request.method == 'POST':
        input_text = request.form['text']
        file = request.files['file']
        
        if file and file.filename.endswith('.xlsx'):
            # 保存上传的文件
            file_path = os.path.join('uploads', file.filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            
            # 读取 Excel 文件
            df = pd.read_excel(file_path)
            if 'text' not in df.columns:
                return "Excel 文件中必须包含名为 'text' 的列", 400
            
            predictions = {}
            for line in df['text']:
                prediction = predict_text(line.strip(), model, vectorizer)
                predictions[line.strip()] = result[prediction]
            
            # 将预测结果写入新的 Excel 文件
            output_df = pd.DataFrame(list(predictions.items()), columns=['输入文本', '预测结果'])
            output_file_path = os.path.join('downloads', 'predictions.xlsx')
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            output_df.to_excel(output_file_path, index=False)
            
            download_link = '/download/predictions.xlsx'
        
        elif input_text:
            lines = input_text.split('\n')
            predictions = {}
            for line in lines:
                prediction = predict_text(line.strip(), model, vectorizer)
                predictions[line.strip()] = result[prediction]
    
    return render_template('index.html', predictions=predictions, download_link=download_link)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('downloads', filename), as_attachment=True)

# 运行 Flask 应用
if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)