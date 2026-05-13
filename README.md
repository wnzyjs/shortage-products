# 全球紧缺商品与关键产品 Dashboard

## 入口

- GitHub Pages 入口：`index.html`
- 兼容旧链接：`dashboard.html` 会跳转到 `index.html`
- 页面数据文件：`data/latest.json`
- 页面脚本数据：`data/latest.js`

## 为什么按钮点了不更新

网页上的按钮只是“刷新当前站点已经发布的数据”，它不会直接在浏览器里执行 Python 抓数。

所以如果 GitHub 仓库里发布的 `data/latest.js` 没变，按钮点再多次，页面还是同一份数据。

## 真正在线更新的方式

项目已经加入 GitHub Actions：

- `.github/workflows/update-dashboard.yml`
- `.github/workflows/pages.yml`

工作方式是：

1. 在 GitHub 仓库页面打开 `Actions`
2. 运行 `Update Dashboard Data`
3. GitHub 云端会执行 `scripts/update_dashboard.py`
4. 工作流会自动更新：
   - `data/latest.json`
   - `data/latest.js`
5. 更新后的提交会触发 Pages 重新部署
6. 部署完成后，回到网页点击“刷新已发布数据”

## 本地手动生成数据

如果你想先在本地更新，再 push 到 GitHub：

```powershell
& "C:\Users\Jason Yang\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" ".\scripts\update_dashboard.py"
```

运行后会生成：

- `data/latest.json`
- `data/latest.js`

## GitHub Pages 建议设置

如果仓库还没启用 Pages：

1. 打开 GitHub 仓库 `Settings`
2. 进入 `Pages`
3. 将 Source 设置为 `GitHub Actions`

## 关键区别

- 网页按钮：刷新“已发布”数据
- GitHub Action：生成“新”数据

只有先让 GitHub Action 或本地脚本产出新的 `latest.js`，网页按钮刷新后才会看到变化。
