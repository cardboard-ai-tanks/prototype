◆ラズパイインストール
2019-04-08-raspbian-stretch.img　をDLして、BaleneBaleneEtcherでSDカードに書き込む
詳しいバーション
pi@raspberrypi:~ $ lsb_release -a
No LSB modules are available.
Distributor ID:    Raspbian
Description:    Raspbian GNU/Linux 9.9 (stretch)
Release:    9.9
Codename:    stretch
SD Cardは３２GB
サンディスク ( SANDISK ) 32GB microSD Extreme PRO R=100MB/s W=90MB/s SDアダプタ付き ［海外パッケージ］ SDSQXCG-032G-GN6MA
https://www.raspberrypi.org/downloads/raspbian/
から2019-04-08-raspbian-stretch.imgをダウンロードできる。３．４８GB

ラズパイ起動したらSSH接続できるように設定する。
RaspbianのデフォルトではSSHが無効化されているため、有効化する
$ sudo touch /boot/ssh
$ sudo reboot

◆モーターを動かそう
いい感じに接続して、gpioたたけば、すぐモーター制御できるよ。
#GPIOの初期化
echo 4 > /sys/class/gpio/export
echo 17 > /sys/class/gpio/export
echo 9 > /sys/class/gpio/export
echo 11 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio4/direction
echo out > /sys/class/gpio/gpio17/direction
echo out > /sys/class/gpio/gpio9/direction
echo out > /sys/class/gpio/gpio11/direction

#モーター回転！
echo 1 > /sys/class/gpio/gpio4/value

#モーター止まれ！
echo 0 > /sys/class/gpio/gpio4/value
安定化電源で５Vでやってるけど、本番はトルクあげるために単三電池４本の６Vだよ
次は、Webブラウザから動くようにする。webiopiをインストールする。
このサイトから　WebIOPi-0.7.1.tar.gz　をダンロードする。
http://webiopi.trouch.com/DOWNLOADS.html
cd ~
mkdir tank
cd tank
wget https://sourceforge.net/projects/webiopi/files/WebIOPi-0.7.1.tar.gz
tar xvf WebIOPi-0.7.1.tar.gz
ラズパイ３用のパッチあてる。（これないとマジでGPIOを制御できない）
$ cd WebIOPi-0.7.1
$ wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi-pi2bplus.patch
$ patch -p1 -i webiopi-pi2bplus.patch
$ sudo ./setup.sh
途中でこのメッセージがでるから y 入力
Do you want to access WebIOPi over Internet ? [y/n]
WebIOPiのサービススクリプトをダウンロードして、サービスを走らせる。

$ cd /etc/systemd/system/
$ sudo wget https://raw.githubusercontent.com/doublebind/raspi/master/webiopi.service
$ sudo systemctl start webiopi
$ sudo systemctl enable webiopi
WebからGPIOを制御してみよう。
http://[ラズパイipアドレス]:8000/
ログイン ID : webiopi パスワード : raspberry　
でログインできます

◆webiopiの設定
webiopiのhtmlルートフォルダの設定をしておこう

sudo vi /etc/webiopi/config
====================変更内容==================
[SCRIPTS]
# Load custom scripts syntax :
# name = sourcefile
#   each sourcefile may have setup, loop and destroy functions and macros
#myscript = /home/pi/webiopi/examples/scripts/macros/script.py
myscript = /home/pi/tank/www/python/tank.py

# Use doc-root to change default HTML and resource files location
#doc-root = /home/pi/webiopi/examples/scripts/macros
doc-root = /home/pi/tank/www/html

# Use welcome-file to change the default "Welcome" file
#welcome-file = index.html
welcome-file = tank.html
===========================================

# 再起動
sudo reboot


◆UI画面
/home/pi/tank/www/html/tank.html 



ブラウザからアクセスすると戦車制御UIを表示します。
http://[IP ADDRESS FOR RASPBERRY PI]/
ブラウザから戦車コントローラーへアクセス。
発射ボタンはまだない


◆カメラ
raspi-configでカメラを有効にする。

◆起動時にIP通知
・discordでwebhook URLを取得(何号機かによって変える)
・通知用のshファイル作成
・sytemdに登録

/home/pi/tank/notifyip.sh を作成
#!/bin/sh

sleep 15
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
  printf "My IP address is %s\n" "$_IP"
  curl -H "Accept: application/json" -H "Content-type: application/json" -X POST -d '{"content": "hello from '"$_IP"'"}' 'https://discordapp.com/api/webhooks/588040369124671546/d-ENUy_43IVypKqUz-UHsI-CNzKJbEdX7YYAKMXm4jRVhXPquUM7It_QBYBoveZp9HZm'
fi


sudo vim.tiny /etc/systemd/system/notifyip.service


[Unit]
Description = notify ip

[Service]
ExecStart=/home/pi/tank/notifyip.sh
Restart=no
Type=oneshot

[Install]
WantedBy=multi-user.target

systemctl enable notifyip


systemctl enable notifyip
systemctl start notifyip
起動時にstream開始
・sytemdに登録

sudo vim.tiny  /etc/systemd/system/stream.service

[Unit]
Description = Movie Streaming

[Service]
ExecStart=/home/pi/tank/camera/stream.sh
Restart=always
Type=simple

[Install]
WantedBy=multi-user.target

systemctl enable stream
systemctl start stream
・CORSが発生してキャンバス描画ができないのでnginxでリバースプロキシを設定する
sudo apt-get install -y nginx


vim.tiny /etc/nginx/sites-enabled/default


以下を追加
        location /:8000/macros {
            rewrite /:8000/(.*) /$1  break;
            proxy_set_header Authorization "Basic d2ViaW9waTpyYXNwYmVycnk=";
            proxy_pass http://localhost:8000/;
        }

        location / {
            proxy_set_header Authorization "Basic d2ViaW9waTpyYXNwYmVycnk=";
            proxy_pass http://localhost:8000/;
        }

        location /image {
            rewrite /image/(.*) /$1  break;
            proxy_set_header Authorization "Basic cGk6MXFhenhjdmI=";
            proxy_pass http://localhost:8080/;


sudo service nginx restart


・tinyyolo3を動かす
raspi側
mkdir /home/pi/tank/www/html/dist

PC側
scp bundle.js pi@raspiのIP:/home/pi/tank/www/html/dist/
scp index.html pi@raspiのIP:/home/pi/tank/www/html/
添付ファイル種類：code
bundle.js
1.10 MB
・webiopiの設定を変更
sudo vim.tiny /etc/webiopi/config

index.htmlに戻しておく
# Use welcome-file to change the default "Welcome" file
welcome-file = index.html
#welcome-file = tank.html
webiopiを再起動
systemctl restart webiopi
添付ファイル種類：webcode
index.html
3.16 KB
一号用のwebhook URL
https://discordapp.com/api/webhooks/588116153101189130/mn2Ll-cet-eiRI5HcT4YKnc6_9gMMMR5sUCzGm9Y9CjPTkTffvopwqQBtv9EtQ5Xv3R_


