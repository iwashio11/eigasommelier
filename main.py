import pandas as pd
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('new5.html')

@app.route('/answer', methods=['POST'])
def answer():
    df = pd.read_csv('data.csv')
    idx = df.columns

    # ユーザーからの入力を取得
    input_dict = {
        'ほのぼの': '心温まる映画が好きですか？'
    }
    user_input = request.form['action']
    Yes_input = [key for key, value in input_dict.items() if user_input == 'yes']

    # ユーザーの好みからスコアを計算
    sample_input_num = len(Yes_input)
    user_score = []
    for id in idx:
        if id == "種類":
            pass
        elif id in Yes_input:
            user_score.append(1/sample_input_num)
        else:
            user_score.append(0)

    # cos類似度の計算
    def cos_sim(v1, v2):
        return np.dot(v1,v2) / (np.linalg.norm(v1)*np.linalg.norm(v2))

    # 最大値の導出
    movies = []
    for i in range(len(df)):
        vec = []
        movie = []
        for j in range(len(df.columns)):
            if j == 0:
                movie.append(df.iloc[i,j])
            else:
                vec.append(df.iloc[i,j])
        movie.append(vec)
        movies.append(movie)

    title = ""
    max_score = 0
    for movie in movies:
        score = cos_sim(user_score, movie[1])
        if score > max_score:
            max_score = score
            title = movie[0]

    return render_template('answer.html', title=title, max_score=max_score)

if __name__ == '__main__':
    app.run(debug=True)