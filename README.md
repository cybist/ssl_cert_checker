# ssl_cert_checker
各ドメインのSSL証明書の有効期限を一元管理します。
日次バッチで、設定ファイルに登録されたドメインリストを元にopensslで有効期限を取得し、この情報がストアされたlevelDBを元にWEBアプリで一覧表示をおこないます。

## 確認済動作要件
* Ubuntu 16.04.7
* Python 3.7.4
* PHP 7.4.0
* Vue.js 2.6.12
* Toml 0.10.2
* levelDB 1.3.0

## インストール
```
sudo apt-get install libleveldb-dev

cd /usr/local/src/
git clone https://github.com/reeze/php-leveldb.git
cd php-leveldb/
phpize
./configure --prefix=/home/you/.phpenv/versions/7.4.0/lib/php/leveldb --with-leveldb=/home/you/.phpenv/versions/7.4.0/include/php/include/leveldb --with-php-config=/home/you/.phpenv/versions/7.4.0/bin/php-config
make
make install
vi ~/.phpenv/versions/7.4.0/etc/php.ini
    extension=/home/you/.phpenv/versions/7.4.0/lib/php/extensions/no-debug-non-zts-20180731/leveldb.so

sudo service php-fpm restart

sudo pip install plyvel
sudo pip install toml

# for app
mkdir ~/projects/
cd ~/projects/
git clone https://github.com/cybist/ssl_cert_checker.git ssl_cert_checker/
cd ssl_cert_checker/
vi configs/common.toml
    #有効期限切れ間近(25日前)を検知した場合にChatWorkへ自動通知する場合は
    #CW_API_TOKEN と CW_ROOM_ID を設定
    #
    #[DOMAIN_LIST]を適宜編集

cd api/
composer require yosymfony/toml

cd ../app/
vi vue.config.js
    #publicPathとpublicを適宜編集

npm install
npm run build

cd ../batch/
python ssl_check.py

sudo vi /etc/nginx/conf.dssl_cert_checker.conf
    server {
        listen 80 default;
        server_name ssl-check.yourdomain.xyz;
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name ssl-check.yourdomain.xyz;

        ssl_certificate /etc/letsencrypt/live/ssl-check.yourdomain.xyz/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/ssl-check.yourdomain.xyz/privkey.pem;

        access_log /home/you/projects/ssl_cert_checker/logs/ssl-check.access.log;
        error_log /home/you/projects/ssl_cert_checker/logs/ssl-check.error.log;

        location / {
            root /home/you/projects/ssl_cert_checker/app/dist;
            index index.html;
        }

        location /api/ {
            root /home/you/projects/ssl_cert_checker/api;
            index index.php;
            try_files $uri $uri/ /index.php?$args;
        }

        location ~ \.php$ {
            root /home/you/projects/ssl_cert_checker/api;
            index index.php;
            try_files $uri = 404;
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            fastcgi_pass   unix:/home/you/.phpenv/versions/7.4.0/var/run/php-fpm.sock;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
            include        fastcgi_params;
        }
    }

sudo nginx -t
sudo service nginx restart

crontab
    5 4 * * * cd /home/you/projects/ssl_cert_checker/batch/ && /usr/local/bin/python3.7 ssl_check.py & > /dev/null 2>&1
```

ブラウザで以下にアクセスして一覧画面が表示されれば成功です。
https://ssl-check.yourdomain.xyz/
<img alt="ssl_cert_checker" src="https://camo.qiitausercontent.com/97e40ff815d3ecb107f9bd5111dcdb99aab6cd75/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3238323333322f38613733303866302d623765612d656133372d353763362d3733333235643633396130322e706e67" />
