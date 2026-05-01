# 全球紧缺商品与关键产品 Dashboard

## 入口

- GitHub Pages 入口文件：`index.html`
- 兼容旧链接：`dashboard.html` 会自动跳转到 `index.html`
- 页面数据文件：`data/latest.json`

## 当前更新方式

这个项目已经改成手动刷新页面数据：

1. 打开网页
2. 点击“更新数据”按钮
3. 页面会重新请求当前站点已发布的 `data/latest.json`

注意：

- 这个按钮不会在浏览器里直接执行 Python 抓数脚本
- GitHub Pages 是静态托管，网页按钮不能直接抓取并生成新文件
- 如果你要真正生成新的数据，仍需本地运行一次更新脚本，然后把新的 `data/latest.json` 推到 GitHub

## 本地生成新数据

```powershell
& "C:\Users\Jason Yang\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" ".\scripts\update_dashboard.py"
```

运行后会更新：

- `data/latest.json`

然后把仓库 push 到 GitHub，网页上的“更新数据”按钮就能重新加载到这份最新已发布数据。

## 为什么之前 GitHub 上无法显示

主要有两个原因：

- 之前页面入口不是标准的 `index.html`
- 之前的数据直接写回 HTML，结构和编码更容易在静态托管场景下出问题

现在已经改成更适合 GitHub Pages 的静态结构：

- `index.html` 负责展示
- `data/latest.json` 负责存数据
- `assets/app.js` 负责前端刷新
