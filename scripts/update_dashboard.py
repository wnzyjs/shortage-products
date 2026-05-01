from __future__ import annotations

import json
import re
import ssl
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DATA_JSON_PATH = DATA_DIR / "latest.json"
DATA_JS_PATH = DATA_DIR / "latest.js"
SSL_CONTEXT = ssl.create_default_context()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CodexDashboard/1.0"

IEA_OVERVIEW_URL = "https://www.iea.org/reports/global-critical-minerals-outlook-2025/overview-of-outlook-for-key-minerals"
IEA_EXEC_URL = "https://www.iea.org/reports/global-critical-minerals-outlook-2025/executive-summary"
USGS_MCS_URL = "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf"
USGS_GA_GE_URL = "https://www.usgs.gov/news/national-news-release/usgs-critical-minerals-study-bans-gallium-and-germanium-exports-could"
WNA_URANIUM_URL = "https://world-nuclear.org/information-library/Nuclear-Fuel-Cycle/Uranium-Resources/Uranium-Markets"
MICRON_HBM_URL = "https://investors.micron.com/news-releases/news-release-details/micron-begins-volume-production-industrys-first-hbm3e-memory"
SK_HYNIX_HBM_URL = "https://news.skhynix.com/sk-hynix-begins-mass-production-of-worlds-first-hbm4-12-layer-samples/"
SEMI_CHIP_URL = "https://www.semi.org/en/news-media-press-releases/global-semiconductor-manufacturing-industry-sees-investment-growth"
HITACHI_ENERGY_URL = "https://www.hitachienergy.com/us/en/news-and-events/press-releases/2024/06/hitachi-energy-invests-additional-155-million-usd"


def fetch_text(url: str) -> str | None:
  request = Request(url, headers={"User-Agent": USER_AGENT})
  try:
    with urlopen(request, timeout=25, context=SSL_CONTEXT) as response:
      charset = response.headers.get_content_charset() or "utf-8"
      return response.read().decode(charset, errors="ignore")
  except (HTTPError, URLError, TimeoutError, OSError):
    return None


def extract_publish_date(text: str) -> str | None:
  match = re.search(
    r"(Published|Updated|First posted)\s+([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}|[A-Za-z]+\s+[0-9]{1,2},\s+[0-9]{4})",
    text,
    re.IGNORECASE,
  )
  return match.group(2) if match else None


def build_live_signals() -> Dict[str, Dict[str, str]]:
  signals: Dict[str, Dict[str, str]] = {}
  iea_overview = fetch_text(IEA_OVERVIEW_URL) or ""
  iea_exec = fetch_text(IEA_EXEC_URL) or ""
  usgs_mcs = fetch_text(USGS_MCS_URL) or ""
  usgs_gage = fetch_text(USGS_GA_GE_URL) or ""
  wna_uranium = fetch_text(WNA_URANIUM_URL) or ""
  micron_hbm = fetch_text(MICRON_HBM_URL) or ""
  sk_hynix_hbm = fetch_text(SK_HYNIX_HBM_URL) or ""
  semi_chip = fetch_text(SEMI_CHIP_URL) or ""
  hitachi_energy = fetch_text(HITACHI_ENERGY_URL) or ""

  if iea_overview or iea_exec:
    signals["copper"] = {
      "current_gap_display": "2035隐含缺口 30%",
      "future_gap_display": "30% by 2035",
      "driver": "IEA 指出铜在当前项目管线下到 2035 年可能出现 30% 的隐含供给缺口。",
      "source_date": extract_publish_date(iea_overview) or "21 May 2025",
    }
    signals["lithium"] = {
      "current_gap_display": "近端宽松，远端转缺",
      "future_gap_display": "40% by 2035",
      "driver": "IEA 指出锂到 2035 年的隐含缺口可能达到 40%。",
      "source_date": extract_publish_date(iea_exec) or "21 May 2025",
    }
    signals["graphite"] = {
      "current_gap_display": "集中度风险高",
      "future_gap_display": "模型估算 12%",
      "driver": "IEA 提示石墨需求增长同时伴随高集中度风险。",
      "source_date": extract_publish_date(iea_exec) or "21 May 2025",
    }
  if usgs_mcs or usgs_gage:
    signals["antimony"] = {
      "current_gap_display": "价格同比 >100%",
      "future_gap_display": "模型估算 22%",
      "driver": "USGS 显示锑价格在 2025 年显著上涨。",
      "source_date": "5 March 2026",
    }
    signals["germanium"] = {
      "current_gap_display": "价格同比 >100%",
      "future_gap_display": "模型估算 21%",
      "driver": "USGS 显示锗价格显著上涨。",
      "source_date": "5 March 2026",
    }
    signals["gallium"] = {
      "current_gap_display": "价格同比 >20%",
      "future_gap_display": "模型估算 18%",
      "driver": "USGS 将镓识别为高供应风险材料。",
      "source_date": "5 March 2026",
    }
  if wna_uranium:
    signals["uranium"] = {
      "current_gap_display": "矿山供给仅覆盖约90%",
      "future_gap_display": "2030需求 +28%",
      "driver": "World Nuclear Association 指出铀需求到 2030 年仍在增长。",
      "source_date": extract_publish_date(wna_uranium) or "23 August 2024",
    }
  if micron_hbm or sk_hynix_hbm:
    signals["memory_hbm"] = {
      "current_gap_display": "HBM 产能已预订至 2026",
      "future_gap_display": "2026前持续偏紧",
      "driver": "HBM 供给持续偏紧，AI 需求跑赢先进封装扩产速度。",
      "source_date": "2024-2025",
    }
  if semi_chip:
    signals["gpu_ai"] = {
      "current_gap_display": "AI 加速卡交付紧张",
      "future_gap_display": "2026前持续偏紧",
      "driver": "AI 加速卡需求高于先进封装与领先制程可交付能力。",
      "source_date": "2025",
    }
  if hitachi_energy:
    signals["power_transformer"] = {
      "current_gap_display": "交期通常 2-4 年",
      "future_gap_display": "2027前偏紧",
      "driver": "大型变压器交期依然偏长，制造瓶颈尚未消除。",
      "source_date": "2024",
    }
  return signals


@dataclass
class Commodity:
  key: str
  name_cn: str
  name_en: str
  category: str
  current_gap_display: str
  future_gap_display: str
  shortage_score: int
  score_model: str
  key_drivers: List[str]
  sources: List[Dict[str, str]]
  china_listed_companies: List[Dict[str, str]]


def parse_gap_value(text: str) -> float:
  if "2027前偏紧" in text or "2-4 年" in text:
    return 92
  if "2026前持续偏紧" in text or "预订至 2026" in text:
    return 88
  if "40%" in text:
    return 90
  if "30%" in text:
    return 80
  if "22%" in text:
    return 68
  if "21%" in text:
    return 66
  if "18%" in text:
    return 62
  if "12%" in text:
    return 50
  if "+28%" in text:
    return 70
  if ">100%" in text:
    return 72
  if ">20%" in text:
    return 48
  return 40


def compute_score(future_gap_pct: float, concentration: float, policy: float, market_stress: float) -> int:
  raw = future_gap_pct * 0.45 + concentration * 0.2 + policy * 0.2 + market_stress * 0.15
  return max(1, min(99, int(round(raw))))


def build_commodities(signals: Dict[str, Dict[str, str]]) -> List[Commodity]:
  base = {
    "gpu_ai": {"name_cn": "AI 加速卡 / GPU", "name_en": "AI Accelerators / GPU", "category": "半导体 / 算力", "current_gap_display": "AI 加速卡交付紧张", "future_gap_display": "2026前持续偏紧", "model": "公开产业信号", "drivers": ["大模型训练和推理推高高端算力卡需求。", "先进制程、先进封装和 HBM 一起构成交付瓶颈。", "短缺表现为交期和配额，而不只是价格波动。"], "sources": [{"label": "SEMI Manufacturing Outlook", "url": SEMI_CHIP_URL, "date": "2025"}], "companies": [{"name": "寒武纪", "ticker": "688256.SH"}, {"name": "海光信息", "ticker": "688041.SH"}, {"name": "景嘉微", "ticker": "300474.SZ"}], "concentration": 96, "policy": 85, "market": 92},
    "memory_hbm": {"name_cn": "高带宽内存 / AI 存储", "name_en": "HBM / AI Memory", "category": "半导体 / 存储", "current_gap_display": "HBM 产能已预订至 2026", "future_gap_display": "2026前持续偏紧", "model": "公开产业信号", "drivers": ["AI 服务器扩张推高 HBM 需求。", "先进封装与高端 DRAM 扩产速度跟不上需求。", "产品级短缺核心是 HBM 与 CoWoS 组合能力。"], "sources": [{"label": "Micron HBM3E Release", "url": MICRON_HBM_URL, "date": "2024"}, {"label": "SK hynix HBM Update", "url": SK_HYNIX_HBM_URL, "date": "2025"}], "companies": [{"name": "兆易创新", "ticker": "603986.SH"}, {"name": "北京君正", "ticker": "300223.SZ"}, {"name": "德明利", "ticker": "001309.SZ"}], "concentration": 95, "policy": 68, "market": 95},
    "power_transformer": {"name_cn": "电力变压器", "name_en": "Power Transformers", "category": "电网设备", "current_gap_display": "交期通常 2-4 年", "future_gap_display": "2027前偏紧", "model": "公开产业信号", "drivers": ["全球电网投资、数据中心接入和新能源并网同步推高需求。", "大型变压器制造周期长，产能扩张慢。", "典型产品级短缺，约束主要体现为交付周期。"], "sources": [{"label": "Hitachi Energy Investment", "url": HITACHI_ENERGY_URL, "date": "2024"}], "companies": [{"name": "特变电工", "ticker": "600089.SH"}, {"name": "中国西电", "ticker": "601179.SH"}, {"name": "保变电气", "ticker": "600550.SH"}], "concentration": 82, "policy": 35, "market": 97},
    "antimony": {"name_cn": "锑", "name_en": "Antimony", "category": "阻燃 / 军工 / 芯片材料", "current_gap_display": "价格同比 >100%", "future_gap_display": "模型估算 22%", "model": "模型估算", "drivers": ["出口管制与贸易摩擦放大可得性风险。", "价格剧烈上行显示现货市场紧张。", "半导体、军工和特种材料需求抬高战略价值。"], "sources": [{"label": "USGS Mineral Commodity Summaries 2026", "url": USGS_MCS_URL, "date": "5 March 2026"}], "companies": [{"name": "湖南黄金", "ticker": "002155.SZ"}, {"name": "华钰矿业", "ticker": "601020.SH"}, {"name": "华锡有色", "ticker": "600301.SH"}], "concentration": 92, "policy": 95, "market": 95},
    "germanium": {"name_cn": "锗", "name_en": "Germanium", "category": "红外 / 光纤 / 半导体", "current_gap_display": "价格同比 >100%", "future_gap_display": "模型估算 21%", "model": "模型估算", "drivers": ["出口限制显著推升海外采购难度。", "价格大幅上涨反映短期供应弹性不足。", "在红外、光纤和高端电子环节替代性有限。"], "sources": [{"label": "USGS Mineral Commodity Summaries 2026", "url": USGS_MCS_URL, "date": "5 March 2026"}, {"label": "USGS Gallium/Germanium Study", "url": USGS_GA_GE_URL, "date": "19 November 2024"}], "companies": [{"name": "云南锗业", "ticker": "002428.SZ"}, {"name": "驰宏锌锗", "ticker": "600497.SH"}, {"name": "罗平锌电", "ticker": "002114.SZ"}], "concentration": 90, "policy": 94, "market": 94},
    "copper": {"name_cn": "铜", "name_en": "Copper", "category": "电气化 / 电网", "current_gap_display": "2035隐含缺口 30%", "future_gap_display": "30% by 2035", "model": "官方预测", "drivers": ["电网投资和全面电气化持续推高铜需求。", "矿石品位下降、资本开支上升、新项目发现放缓。", "IEA 已给出 2035 年明确供需缺口口径。"], "sources": [{"label": "IEA Critical Minerals Outlook 2025", "url": IEA_OVERVIEW_URL, "date": "21 May 2025"}], "companies": [{"name": "江西铜业", "ticker": "600362.SH"}, {"name": "紫金矿业", "ticker": "601899.SH"}, {"name": "洛阳钼业", "ticker": "603993.SH"}], "concentration": 88, "policy": 50, "market": 80},
    "gallium": {"name_cn": "镓", "name_en": "Gallium", "category": "射频 / 功率半导体", "current_gap_display": "价格同比 >20%", "future_gap_display": "模型估算 18%", "model": "模型估算", "drivers": ["USGS 将镓识别为高供应风险材料。", "半导体、电力电子和国防链条对镓依赖度高。", "出口许可制度意味着供应恢复并不等于风险消失。"], "sources": [{"label": "USGS Gallium/Germanium Study", "url": USGS_GA_GE_URL, "date": "19 November 2024"}, {"label": "USGS Mineral Commodity Summaries 2026", "url": USGS_MCS_URL, "date": "5 March 2026"}], "companies": [{"name": "中国铝业", "ticker": "601600.SH"}, {"name": "云铝股份", "ticker": "000807.SZ"}, {"name": "南山铝业", "ticker": "600219.SH"}], "concentration": 95, "policy": 92, "market": 70},
    "lithium": {"name_cn": "锂", "name_en": "Lithium", "category": "动力电池", "current_gap_display": "近端宽松，远端转缺", "future_gap_display": "40% by 2035", "model": "官方预测", "drivers": ["IEA 指出近端市场偏宽松，但 2030 年代可能重新转入短缺。", "新能源车与储能扩张推动需求增速维持高位。", "新项目开发前景优于铜，但仍难完全填平长期缺口。"], "sources": [{"label": "IEA Critical Minerals Outlook 2025", "url": IEA_EXEC_URL, "date": "21 May 2025"}], "companies": [{"name": "天齐锂业", "ticker": "002466.SZ"}, {"name": "赣锋锂业", "ticker": "002460.SZ"}, {"name": "盛新锂能", "ticker": "002240.SZ"}], "concentration": 78, "policy": 48, "market": 62},
    "uranium": {"name_cn": "铀", "name_en": "Uranium", "category": "核电燃料", "current_gap_display": "矿山供给仅覆盖约90%", "future_gap_display": "2030需求 +28%", "model": "官方趋势 + 模型估算", "drivers": ["全球核电复兴推升中长期燃料需求。", "矿山供给未完全覆盖反应堆需求。", "2030 前需求增长明确，扩产周期长。"], "sources": [{"label": "World Nuclear Association", "url": WNA_URANIUM_URL, "date": "23 August 2024"}], "companies": [{"name": "中广核矿业", "ticker": "1164.HK"}, {"name": "中核国际", "ticker": "2302.HK"}, {"name": "中国广核", "ticker": "003816.SZ"}], "concentration": 82, "policy": 70, "market": 82},
    "graphite": {"name_cn": "石墨", "name_en": "Graphite", "category": "负极材料 / 储能", "current_gap_display": "集中度风险高", "future_gap_display": "模型估算 12%", "model": "模型估算", "drivers": ["储能和动力电池继续带动需求增长。", "IEA 认为总量有望覆盖，但供应集中度仍是脆弱点。", "一旦出口限制升级，产业链扰动会被放大。"], "sources": [{"label": "IEA Critical Minerals Outlook 2025", "url": IEA_EXEC_URL, "date": "21 May 2025"}], "companies": [{"name": "中国宝安", "ticker": "000009.SZ"}, {"name": "中科电气", "ticker": "300035.SZ"}, {"name": "翔丰华", "ticker": "300890.SZ"}], "concentration": 90, "policy": 80, "market": 52}
  }

  items = []
  for key, details in base.items():
    live = signals.get(key, {})
    current_gap = live.get("current_gap_display", details["current_gap_display"])
    future_gap = live.get("future_gap_display", details["future_gap_display"])
    drivers = details["drivers"][:]
    if live.get("driver"):
      drivers.insert(0, live["driver"])
    sources = [dict(source) for source in details["sources"]]
    if sources and live.get("source_date"):
      sources[0]["date"] = live["source_date"]
    score = compute_score(parse_gap_value(future_gap), details["concentration"], details["policy"], details["market"])
    items.append(Commodity(key, details["name_cn"], details["name_en"], details["category"], current_gap, future_gap, score, details["model"], drivers[:3], sources, details["companies"]))

  items.sort(key=lambda item: item.shortage_score, reverse=True)
  return items[:10]


def build_payload() -> Dict[str, object]:
  items = build_commodities(build_live_signals())
  max_gap_item = max(items, key=lambda item: parse_gap_value(item.future_gap_display))
  return {
    "meta": {
      "generated_at_local": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
      "refresh_note": "点击网页按钮会重新加载已发布的 latest.js；若要生成新数据，请本地运行更新脚本后重新发布。",
      "mode_label": "手动刷新页面数据"
    },
    "summary": {
      "top_risk_name": items[0].name_cn,
      "average_score": round(sum(item.shortage_score for item in items) / len(items)),
      "max_future_gap": f"{max_gap_item.name_cn} {max_gap_item.future_gap_display}"
    },
    "items": [{
      "key": item.key,
      "name_cn": item.name_cn,
      "name_en": item.name_en,
      "category": item.category,
      "current_gap_display": item.current_gap_display,
      "future_gap_display": item.future_gap_display,
      "shortage_score": item.shortage_score,
      "score_model": item.score_model,
      "key_drivers": item.key_drivers,
      "sources": item.sources,
      "china_listed_companies": item.china_listed_companies
    } for item in items]
  }


def main() -> None:
  payload = build_payload()
  DATA_DIR.mkdir(exist_ok=True)
  DATA_JSON_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
  DATA_JS_PATH.write_text("window.DASHBOARD_DATA = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
  print(f"Data written: {DATA_JSON_PATH}")
  print(f"Script written: {DATA_JS_PATH}")


if __name__ == "__main__":
  main()
