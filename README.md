## concept
Containers of selenium server and application server to run webdriver.

Webdriver connects selenium server @`http://selenium-chrome:4444/wd/hub`.

Using SeleniumHQ/docker-selenium for selenium server.
https://github.com/SeleniumHQ/docker-selenium

## How to use
### basic
1. Run `docker-compose up -d` to start containers
2. Run `docker-compose exec app {executtion-command} {script}` to execute script to scraping({script} must exists in `app/` directory e.g. test.py)
### optional
3. Access `localhost:5900` with VNC software

## テストの設計
- 開始ページにget
- 前提条件の確認
- assert()メソッドを作って判定＋エビデンス
- assert()が失敗したら中止
- log出力