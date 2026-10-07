# TOEIC 600 衝刺本（離線獨立版）

以多益 600 分為目標的英文學習 App。這個資料夾是可以直接放上任何靜態網站主機的 PWA：安裝到手機或電腦後，第一次開啟就會把內容存起來，之後可以離線使用。

## 內容

- 單字 804 個（15 個主題），間隔複習、選擇題測驗、聽音拼字
- Part 1 照片 20 題、Part 2 應答 60 題、Part 3/4 對話與獨白 24 組
- Part 5 句子填空 225 題、Part 6/7 閱讀 18 組（含雙篇、三篇）
- 模擬測驗：迷你 20 題／15 分鐘、半版 100 題／60 分鐘
- 文法重點 13 項、弱點分析、錯題本、12 週計畫

和 Claude 上的版本相比，獨立版**沒有 AI 批改與對話**，進度只存在這台裝置的瀏覽器裡。兩個版本之間可以用「設定 → 備份與轉移」的備份碼搬移進度。

## 檔案

| 檔案 | 用途 |
|---|---|
| `index.html` | 整個 App（HTML、CSS、JS、題庫都在裡面） |
| `manifest.webmanifest` | App 名稱、圖示、顏色，讓瀏覽器可以安裝 |
| `sw.js` | Service worker：離線快取 |
| `icons/` | App 圖示 |

## 在電腦上試用

```bash
python -m http.server 8600 --directory toeic600-pwa
```

然後打開 http://localhost:8600 。Service worker 只能在 `https://` 或 `localhost` 底下運作，直接雙擊 `index.html` 打開的話不能離線。

## 放上網路（擇一）

- **GitHub Pages**：把這個資料夾的內容推到一個 GitHub repository，到 Settings → Pages 選擇分支，幾分鐘後就有 `https://<帳號>.github.io/<repo>/` 的網址。
- **Netlify Drop**：到 https://app.netlify.com/drop ，把整個資料夾拖進去。
- **Cloudflare Pages / Vercel**：建立新專案，上傳這個資料夾即可，不需要建置指令。

## 更新內容

App 的原始檔放在 `source/toeic600.html`（同時也是 Claude 版），產生器是 `source/build_pwa.py`。修改原始檔後，在 repository 根目錄重新產生：

```bash
python source/build_pwa.py source/toeic600.html . "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
```

最後一個參數是用來產生圖示的 Edge／Chrome 執行檔路徑。

`sw.js` 的快取版本會跟著內容自動改變，使用者下次連網開啟時就會拿到新版。
