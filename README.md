# station-flask-api

iTunesのplistをJSONに変換する処理と、ALACファイルをFLACに変換する処理を行う。

## Dockerの実行方法
1. Docker Imageの作成  
   このREADME.mdがあるディレクトリで  
   `# docker image build -t flask .`  
   を実行する。

2. イメージを実行する  
   このREADME.mdがあるディレクトリで  
   `docker run -p 14125:14125 -v ${PWD}/app:/app -d flask`  
   を実行する。  
   ※${RUN} はそのままの文字列。

## APIの使用方法
1. ALACファイルをFLACに変換する機能  
   192.168.X.X:14125/convert/alac-to-flac/  
   に対し、Bodyの中にfileを仕込み、更にその中に変換したいalacファイルを添付してPOST送信する。
   ※192.168.X.Xは、このDockerが実行されているサーバのアドレス等を指定する

2. plist.xmlをjsonに変換する機能  
   (鋭意実装中につき、使用方法は後ほど執筆する)