aws-billing
---

AWS請求額をSlackに通知するスクリプトです。

`SLACK_WEBHOOK_URL`を環境変数に設定して`billing.py`を実行すると、
当月の請求額を日付と共にリッチメッセージでSlackへ通知します。

## 使い方

```bash
$ make venv      # 仮想環境の作成
$ make install   # 依存関係のインストール
$ WEBHOOK_URL=<ウェブフックURL> make run
```

