# Notion テンプレート販売ビジネス 自動化エージェントチーム

Reddit・ProductHunt でリサーチ → Claude API で設計書＆販売コピー生成 → Playwright でサムネイル生成 → Gumroad に自動出品、という一連のワークフローを 5 つのエージェントで自動化するシステムです。

## ファイル構成

```
notion-template-business/
├── .env                    # API キー（要設定）
├── requirements.txt        # 依存ライブラリ
├── orchestrator.py         # 全体制御スクリプト
├── agents/
│   ├── research_agent.py   # Agent 1: 売れ筋テーマ調査
│   ├── design_agent.py     # Agent 2: テンプレート設計書生成
│   ├── copy_agent.py       # Agent 3: 販売コピー生成
│   ├── thumbnail_agent.py  # Agent 4: サムネイル画像生成
│   └── publish_agent.py    # Agent 5: Gumroad 出品
├── data/                   # 中間データ（自動生成）
│   ├── research_result.json
│   ├── design_spec.md
│   └── sales_copy.json
└── output/                 # 成果物（自動生成）
    ├── thumbnail.html
    └── thumbnail.png
```

---

## 環境構築

### 1. Python のバージョン確認

Python 3.11 以上が必要です。

```bash
python --version
```

### 2. 仮想環境の作成と有効化

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. 依存ライブラリのインストール

```bash
pip install -r requirements.txt
```

### 4. Playwright のブラウザインストール

```bash
playwright install chromium
```

### 5. API キーの設定

`.env` ファイルを編集して各 API キーを入力します。

```env
ANTHROPIC_API_KEY=sk-ant-...
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
REDDIT_USER_AGENT=notion-template-bot/1.0
PRODUCTHUNT_API_KEY=...
GUMROAD_ACCESS_TOKEN=...
GUMROAD_PRODUCT_URL=          # 商品公開後に実際の URL を記入
NOTION_API_KEY=...
NOTION_PARENT_PAGE_ID=...
X_API_KEY=...
X_API_SECRET=...
X_BEARER_TOKEN=...
X_ACCESS_TOKEN=...
X_ACCESS_TOKEN_SECRET=...
GMAIL_ADDRESS=your@gmail.com
GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

#### 各 API キーの取得方法

| サービス | 取得場所 |
|---|---|
| Anthropic (Claude) | https://console.anthropic.com/ → API Keys |
| Reddit | https://www.reddit.com/prefs/apps → "create another app" (script タイプ) |
| ProductHunt | https://www.producthunt.com/v2/oauth/applications |
| Gumroad | https://app.gumroad.com/settings/advanced → Generate Token |
| Notion | https://www.notion.so/my-integrations → New integration |
| X (Twitter) | https://developer.twitter.com/en/portal/projects-and-apps |
| Gmail | 下記「Gmail アプリパスワードの取得手順」参照 |

> **注意:** Reddit と ProductHunt の API キーが未設定でも、フォールバックデータを使い処理を続行します。Gumroad は Agent 6 でのみ必要です。

#### Gmail アプリパスワードの取得手順

> **前提:** Google アカウントで 2 段階認証が有効になっている必要があります。

1. https://myaccount.google.com/security を開く
2. **2 段階認証プロセス** をクリック
3. ページ下部の **アプリ パスワード** をクリック
4. アプリ名に任意の名前（例: `NotionTemplateBot`）を入力 → **作成**
5. 表示された 16 桁のパスワード（例: `dgyq dfmf axxx vdqs`）をコピー
6. `.env` の `GMAIL_APP_PASSWORD` にスペースなしで貼り付け（例: `dgyqdfmfaxxxvdqs`）

> **注意:** アプリパスワードは通常の Gmail パスワードとは別物です。2 段階認証が無効の場合は https://myaccount.google.com/security から有効化してください。

#### X (Twitter) アプリの権限設定（必須）

X API で投稿するには **Read and Write** 権限が必要です。

1. https://developer.twitter.com/en/portal/projects-and-apps を開く
2. 対象アプリを選択 → **Settings** タブ
3. **User authentication settings** → Edit
4. **App permissions** を **Read and Write** に変更して保存
5. **Keys and tokens** タブで **Access Token and Secret** を再生成
6. 新しいトークンを `.env` の `X_ACCESS_TOKEN` / `X_ACCESS_TOKEN_SECRET` に記入

---

## 毎日の運用フロー

```
06:00 【自動】分析 → 新商品作成 → Notion ページ生成
      【手動】output/publish_summary.txt を確認して Gumroad に登録
             python update_gumroad_url.py https://takasoccerfan.gumroad.com/l/xxxxx

09:00 【自動】X 投稿文生成 → data/twitter_draft.txt に保存 → Gmail 送信
      【手動】twitter_draft.txt をコピーして X に投稿

21:00 【自動】X 投稿文生成 → data/twitter_draft.txt に保存 → Gmail 送信
      【手動】twitter_draft.txt をコピーして X に投稿
```

---

## 実行方法

### スケジューラーの起動（通常の使い方）

```bash
python scheduler.py
```

起動したままにしておくと以下が自動実行されます：

| 時刻 | 処理 |
|---|---|
| 06:00 | analytics_agent → orchestrator（agents 1-5）→ latest_product.json 保存 |
| 09:00 | tweet 文案生成 → twitter_draft.txt 保存 → Gmail 送信 |
| 21:00 | tweet 文案生成 → twitter_draft.txt 保存 → Gmail 送信 |

### Gumroad URL の登録

Gumroad に手動登録後、以下のコマンドで URL を記録します。
次回の 09:00 / 21:00 tweet に新商品告知が含まれるようになります。

```bash
python update_gumroad_url.py https://takasoccerfan.gumroad.com/l/xxxxx
```

### 全 Agent を手動で順番に実行

```bash
python orchestrator.py                       # 全 agent (1-7)
python orchestrator.py --start-from 2        # Agent 2 から再開
python orchestrator.py --end-at 5            # Agent 1-5 のみ実行
python orchestrator.py --start-from 2 --end-at 5  # 範囲指定
```

### 各 Agent を単体で手動実行

```bash
python agents/analytics_agent.py   # ツイート分析
python agents/twitter_agent.py     # 文案生成
python agents/email_agent.py       # メール送信
```

### Windows タスクスケジューラーへの自動登録

PC 起動時に `scheduler.py` をバックグラウンドで自動起動するよう登録します。

#### ファイル構成

| ファイル | 役割 |
|---|---|
| `setup_scheduler.bat` | タスクスケジューラーへの登録スクリプト（1 回だけ実行） |
| `run_scheduler.bat` | Python 実行ラッパー（ログを `logs/scheduler.log` に出力） |
| `run_scheduler.vbs` | ウィンドウなしでバックグラウンド起動するサイレントランチャー |

#### 登録手順

1. `setup_scheduler.bat` を**右クリック → 管理者として実行**
2. `[OK] Task registered successfully.` と表示されれば完了
3. 次回 Windows ログイン時から自動起動

#### タスクの管理

```bat
# 今すぐ起動（再起動不要で動作確認）
schtasks /run /tn "NotionTemplateScheduler"

# 登録状況の確認
schtasks /query /tn "NotionTemplateScheduler"

# タスクの削除
schtasks /delete /tn "NotionTemplateScheduler" /f
```

#### ログの確認

```bash
# 最新のスケジューラーログを確認
type logs\scheduler.log
```

### 各 Agent を単体で実行

```bash
python agents/research_agent.py
python agents/design_agent.py
python agents/copy_agent.py
python agents/thumbnail_agent.py
python agents/publish_agent.py
```

---

## ワークフロー概要

```
Agent 1: research_agent
  └─ Reddit (r/Notion, r/productivity) + ProductHunt を調査
  └─ 「template」を含む投稿をスコアリング
  └─ TOP5 テーマを data/research_result.json に保存
        ↓
Agent 2: design_agent
  └─ TOP1 テーマを Claude API に渡す
  └─ データベース構成・ページ構成・使い方フローを生成
  └─ data/design_spec.md に保存
        ↓
Agent 3: copy_agent
  └─ design_spec.md を Claude API に渡す
  └─ タイトル・説明文・特徴・FAQ・価格を日英両方で生成
  └─ data/sales_copy.json に保存
        ↓
Agent 4: thumbnail_agent
  └─ sales_copy.json からタイトル・特徴・価格を取得
  └─ Jinja2 で HTML テンプレートを生成
  └─ Playwright で 1200×630px PNG に変換
  └─ output/thumbnail.png に保存
        ↓
Agent 5: publish_agent
  └─ Gumroad API で商品をドラフト登録
  └─ サムネイル画像をアップロード
  └─ 商品 URL をログ出力
```

---

## 出力ファイル

| ファイル | 内容 |
|---|---|
| `data/research_result.json` | TOP5 テーマとスコア |
| `data/design_spec.md` | Notion テンプレート設計書（Markdown） |
| `data/sales_copy.json` | 販売コピー（タイトル・説明・特徴・FAQ・価格） |
| `output/thumbnail.html` | サムネイル用 HTML（デバッグ用） |
| `output/thumbnail.png` | 販売用サムネイル画像（1200×630px） |

---

## 注意事項

- Agent 5 は Gumroad に**ドラフト（非公開）**で商品を登録します。公開前に必ずダッシュボードで内容を確認してください。
- Claude API の利用には料金が発生します。1 回の実行で Agent 2・3 それぞれ 1 回の API 呼び出しが行われます。
- `output/thumbnail.html` をブラウザで開くと、画像を生成せずにデザインを確認できます。

---

## トラブルシューティング

### `playwright install chromium` でエラーが出る

```bash
# 依存ライブラリが不足している場合（Linux）
playwright install-deps chromium
```

### `ModuleNotFoundError` が出る

```bash
pip install -r requirements.txt
```

### Reddit API エラーで処理が止まる

`.env` の `REDDIT_CLIENT_ID` と `REDDIT_CLIENT_SECRET` が正しいか確認してください。未設定でもフォールバックデータで処理は続行されます。

### Gumroad API エラー

`GUMROAD_ACCESS_TOKEN` の権限が `Edit products` になっているか確認してください。
