import streamlit as st
import pandas as pd

from sklearn.metrics import accuracy_score, recall_score, precision_score

# 【変更する】正解データを読み込む
df_ans = pd.read_csv('FakeNews_Det_test_Answer.csv')

# 【変更する】目的変数の変数名
column_name = 'isfake'

# 【変更する】演習のタイトル
st.title('FakeNews Detect Competition')

# 【必要なら変更する】Accuracy / Precision / Recall / F1 以外でランキングを作成する場合は変更・
ranking_df = pd.read_csv('ranking.csv')

st.sidebar.title('オプション')
st.sidebar.write('ランキングボードを並び替えする基準とする評価指標を選択してください。')
option = ['Accuracy', 'Recall', 'Precision']
selected_score = st.sidebar.selectbox('Select your option', option)
st.sidebar.write('ランキングボードの結果を CSV ファイルで出力したい場合')
st.subheader('CSV ファイルを提出')

# streamlitでテキストを入力
name = st.text_input('ニックネームを入力してください。（重複する名前は使えません。）')
group_name = st.text_input('グループ名を入力してください。')

# streamlitでファイルをアップロード
uploaded_file = st.file_uploader("CSV ファイルをアップロードしてください。", type="csv")

# 表のアップロード方法についてサンプルを提示
st.write('提出する CSV ファイルは以下の形式で提出してください。インデックス列は不要です。')

# 【変更する】クラス番号や回帰予測値などに合わせて、変更する
df = pd.DataFrame({'isfake': [0, 1, 0, 1]})
st.dataframe(df)


# アップロードしたファイルを読み込み
st.write('CSV ファイルを選択したら以下の「評価」ボタンをクリックしてください。')
try:
    if st.button('評価') and uploaded_file is not None:

        # 読み込み
        input_df = pd.read_csv(uploaded_file)

        # 分類問題のスコアを計算
        score_acc = round(accuracy_score(df_ans[column_name], input_df[column_name]), 4)
        score_recall = round(recall_score(df_ans[column_name], input_df[column_name], average='macro'), 4)
        score_precision = round(precision_score(df_ans[column_name], input_df[column_name], average='macro'), 4)
        
        df_score = pd.DataFrame({'Name': [name],
                                 'Group': [group_name],
                                 'Accuracy': [score_acc],
                                 'Recall': [score_recall],
                                 'Precision': [score_precision]})
        
        # ranking_df に df_score と同じ行があれば
        if ranking_df[ranking_df['Name'] == name].empty:
            ranking_df = pd.concat([ranking_df, df_score], axis=0)
        
        ranking_df.to_csv('ranking.csv', index=False)
        # print(df_score)
        st.write('推論できました！ランキングボードを確認してみましょう。')
except:
    st.write('<span style="color:red">エラーが発生したため正しく推論結果を保存できませんでした。提出フォーマット等を再度確認してみましょう。</span>', unsafe_allow_html=True)

st.sidebar.download_button('csvファイルを出力', ranking_df.to_csv(index=False), 'ranking.csv')

# ランキングボードのソートオプションを更新
if selected_score == 'Accuracy':
    score_column = 'Accuracy'
elif selected_score == 'Recall':
    score_column = 'Recall'
else:
    score_column = 'Precision'

ranking_df = ranking_df.sort_values(score_column, ascending=False)
rank = ranking_df[score_column].rank(method='min', ascending=False).astype(int)
ranking_df.insert(0, 'Rank', rank)
ranking_df = ranking_df.sort_values('Rank', ascending=True)
ranking_df = ranking_df.reset_index(drop=True)

st.subheader('ランキングボード')
st.table(ranking_df)
