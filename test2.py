import pickle, os

# 講義資料情報を保存するフォルダが無ければ新規作成
if not os.path.exists('lectures.pickle'):
    with open('lectures.pickle', mode='wb') as f:
        pickle.dump([], f)
