import joblib
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_directory)
def load_model_and_vectorizer(model_path, vectorizer_path):
    """
    加载训练好的模型和向量化器
    """
    model = joblib.load(model_path)
    vectorizer = joblib.load(vectorizer_path)
    return model, vectorizer

def predict_text(text, model, vectorizer, t = 'GaussianNB'):
    """
    使用加载的模型和向量化器对输入文本进行预测
    """
    # 将输入文本转换为特征向量
    text_counts = vectorizer.transform([text])
    
    # 进行预测
    if t == 'GaussianNB':
        prediction = model.predict(text_counts.toarray())
    else:
        prediction = model.predict(text_counts)
    
    return prediction[0]

if __name__ == '__main__':

    # 加载模型和向量化器
    model, vectorizer = load_model_and_vectorizer('GaussianNB.pkl', 'tfidf_vectorizer.pkl')

    # 示例预测
    input_text = "1"
    prediction = predict_text(input_text, model, vectorizer)

    result = ['normal/正常', 'weak/弱口令', 'tokens/令牌']
    print(f"预测出来的结果是: {result[prediction]}")