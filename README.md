# concept
The minimum selenium environment dedicated to writing scripts.

# How to use
1. `docker-compose up -d`
2. Access to `localhost:8081`


共通して、操作後にスクリーンショットを保存する
### google
指定されたURLを開いて保存するだけのシンプルなテストスクリプト
### select radio checkbox label
仮想ブラウザ上で各inputの操作をするテストスクリプト(label はチェックボックス等がラップされ直接押下できない場合に利用)

### shinro
### bus
### analizer
ページ内のリンクを全取得して、オブジェクト画像と遷移先URLを表示する
### capture
URLと走査したいXPATHを入力することで
該当するXPATHのオブジェクトの抜き出し
＋ページ内での位置を番号付きで表示する