# 全球紧缺商品 Dashboard

本项目生成一个可直接双击打开的本地 Dashboard，展示：

- 全球最紧缺 10 大商品
- 当前缺口/市场压力
- 未来缺口预测
- 关键驱动因素
- 对应中国上市企业与股票代码
- 公开来源与更新时间

## 目录

- `dashboard.html`：最终看板，双击即可打开
- `assets/`：页面样式和脚本
- `scripts/update_dashboard.py`：抓取最新公开来源并重建看板
- `scripts/register_daily_update.ps1`：注册 Windows 每日计划任务

## 立即刷新一次

```powershell
& "C:\Users\Jason Yang\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" ".\scripts\update_dashboard.py"
```

## 开启每日自动更新

以管理员或当前用户 PowerShell 执行：

```powershell
.\scripts\register_daily_update.ps1
```

默认会在每天 `08:30` 运行一次更新脚本。

## 数据说明

- 看板每天运行一次更新逻辑，但不同权威来源的发布频率不同。
- 因此页面展示的是“最新可得官方数据”，不是所有品类都严格日频。
- 对于铜、锂等拥有明确官方缺口预测的品类，直接显示官方值。
- 对于锑、镓、锗、钨等没有统一全球缺口口径的品类，显示的是基于公开信号的模型估算值，并在页面上单独标识。
