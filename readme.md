GitHub Actions でスクレイピングして、Slack に DM で通知するボットです。

## 機能
- スクレイピングの成否を GitHub Actions で確認
- `false` の場合、Slack に「まだだよ」と通知
- 各ユーザーは `configs/{username}.json` で設定可能

## セットアップ手順
1. Slack Bot を作成してトークンを GitHub Secrets に保存
2. `configs/USERNAME.json` に設定を記述
3. `Actions > Scrape and Notify > Run workflow` から実行