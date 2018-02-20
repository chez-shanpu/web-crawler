# web-crawler
あくあたん工房の春休み課題

### コマンドについて
このプログラムは実行後、指定のコマンドを入力することでそれぞれ以下の動作をします。
- "exit"
プログラムが終了します。
- "print"
指定のデータテーブルの内容を列挙します。
- "delete"
コマンド入力後に入力した条件(例：date='2017.4.17')に合致したデータテーブルの列が削除されます。なお条件に何も入力しなかった場合、すべての列が削除されます。
- "update"
SET sentenceで入力した内容に条件に合致した列が更新されます。条件に何も入力しなかった場合、すべての列が更新されます。
- "acquire"
実行前に設定されたURLでデータを再取得しデータテーブルに反映させます。