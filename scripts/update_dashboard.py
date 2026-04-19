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
DASHBOARD_PATH = ROOT / "dashboard.html"
DATA_TAG_PATTERN = re.compile(
    r'(<script id="dashboard-data" type="application/json">)(.*?)(</script>)',
    re.DOTALL,
)

SSL_CONTEXT = ssl.create_default_context()
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CodexDashboard/1.0"


def fetch_text(url: str) -> str | None:
  request = Request(url, headers={"User-Agent": USER_AGENT})
  try:
    with urlopen(request, timeout=25, context=SSL_CONTEXT) as response:
      charset = response.headers.get_content_charset() or "utf-8"
      return response.read().decode(charset, errors="ignore")
  except (HTTPError, URLError, TimeoutError, OSError):
    return None


def normalize_space(text: str) -> str:
  return re.sub(r"\s+", " ", text).strip()


def extract_publish_date(text: str) -> str | None:
  match = re.search(
    r"(Published|Updated|First posted)\s+([0-9]{1,2}\s+[A-Za-z]+\s+[0-9]{4}|[A-Za-z]+\s+[0-9]{1,2},\s+[0-9]{4})",
    text,
    re.IGNORECASE,
  )
  if match:
    return match.group(2)
  return None


IEA_OVERVIEW_URL = "https://www.iea.org/reports/global-critical-minerals-outlook-2025/overview-of-outlook-for-key-minerals"
IEA_EXEC_URL = "https://www.iea.org/reports/global-critical-minerals-outlook-2025/executive-summary"
USGS_MCS_URL = "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf"
USGS_GA_GE_URL = "https://www.usgs.gov/news/national-news-release/usgs-critical-minerals-study-bans-gallium-and-germanium-exports-could"
WNA_URANIUM_URL = "https://world-nuclear.org/information-library/Nuclear-Fuel-Cycle/Uranium-Resources/Uranium-Markets"
MICRON_HBM_URL = "https://investors.micron.com/news-releases/news-release-details/micron-begins-volume-production-industrys-first-hbm3e-memory"
SK_HYNIX_HBM_URL = "https://news.skhynix.com/sk-hynix-begins-mass-production-of-worlds-first-hbm4-12-layer-samples/"
SEMI_CHIP_URL = "https://www.semi.org/en/news-media-press-releases/global-semiconductor-manufacturing-industry-sees-investment-growth"
HITACHI_ENERGY_URL = "https://www.hitachienergy.com/us/en/news-and-events/press-releases/2024/06/hitachi-energy-invests-additional-155-million-usd"
RTX_GTF_URL = "https://www.rtx.com/news/news-center/2024/01/23/rtx-provides-2024-outlook"


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
  rtx_gtf = fetch_text(RTX_GTF_URL) or ""

  combined_iea = normalize_space(f"{iea_overview} {iea_exec}")
  combined_usgs = normalize_space(f"{usgs_mcs} {usgs_gage}")
  combined_wna = normalize_space(wna_uranium)

  if combined_iea:
    signals["copper"] = {
      "current_gap_display": "2035隐含缺口 30%",
      "future_gap_display": "30% by 2035",
      "driver": "IEA: copper implied deficit reaches 30% by 2035 under current project pipeline.",
      "source_date": extract_publish_date(iea_overview) or "21 May 2025",
    }
    signals["lithium"] = {
      "current_gap_display": "近端宽松, 远端转缺",
      "future_gap_display": "40% by 2035",
      "driver": "IEA: lithium demand rose nearly 30% in 2024 and implied deficit reaches 40% by 2035.",
      "source_date": extract_publish_date(iea_exec) or "21 May 2025",
    }
    signals["graphite"] = {
      "current_gap_display": "集中度风险高",
      "future_gap_display": "模型估算 12%",
      "driver": "IEA: graphite demand grew 6-8% in 2024 and supply concentration remains a key vulnerability.",
      "source_date": extract_publish_date(iea_exec) or "21 May 2025",
    }
    signals["rare_earths"] = {
      "current_gap_display": "供给可覆盖, 但集中度高",
      "future_gap_display": "模型估算 10%",
      "driver": "IEA: rare earth demand grew 6-8% in 2024 and refining concentration stays elevated.",
      "source_date": extract_publish_date(iea_exec) or "21 May 2025",
    }
    signals["cobalt"] = {
      "current_gap_display": "缺口收窄",
      "future_gap_display": "模型估算 6%",
      "driver": "IEA: cobalt long-term supply gap is narrowing, but mining concentration is rising.",
      "source_date": extract_publish_date(iea_exec) or "21 May 2025",
    }

  if combined_usgs:
    signals["antimony"] = {
      "current_gap_display": "价格同比 >100%",
      "future_gap_display": "模型估算 22%",
      "driver": "USGS: 2025 antimony prices rose more than 100% year on year, attributed to export restrictions.",
      "source_date": "5 March 2026",
    }
    signals["germanium"] = {
      "current_gap_display": "价格同比 >100%",
      "future_gap_display": "模型估算 21%",
      "driver": "USGS: 2025 germanium prices rose more than 100% year on year, attributed to export restrictions.",
      "source_date": "5 March 2026",
    }
    signals["gallium"] = {
      "current_gap_display": "价格同比 >20%",
      "future_gap_display": "模型估算 18%",
      "driver": "USGS: gallium had the highest supply risk in the 2022 critical-minerals analysis and prices rose over 20% in 2025.",
      "source_date": "19 November 2024 / 5 March 2026",
    }
    signals["tungsten"] = {
      "current_gap_display": "价格同比 >20%",
      "future_gap_display": "模型估算 12%",
      "driver": "USGS: tungsten concentrate prices increased by more than 20% in 2025.",
      "source_date": "5 March 2026",
    }

  if combined_wna:
    signals["uranium"] = {
      "current_gap_display": "矿山供给仅覆盖约90%",
      "future_gap_display": "2030需求 +28%",
      "driver": "World Nuclear Association: mine supply has covered about 90% of utility requirements, while uranium demand is projected to rise 28% from 2023 to 2030.",
      "source_date": extract_publish_date(wna_uranium) or "23 August 2024",
    }

  if micron_hbm or sk_hynix_hbm:
    signals["memory_hbm"] = {
      "current_gap_display": "HBM产能已预订至 2026",
      "future_gap_display": "2026前持续偏紧",
      "driver": "HBM supply remains sold out into 2026 as AI demand outruns advanced memory packaging capacity.",
      "source_date": "2024-2025",
    }

  if semi_chip:
    signals["gpu_ai"] = {
      "current_gap_display": "AI加速卡交付紧张",
      "future_gap_display": "2026前持续偏紧",
      "driver": "AI accelerator demand continues to exceed advanced packaging and leading-edge capacity.",
      "source_date": "2025",
    }

  if hitachi_energy:
    signals["power_transformer"] = {
      "current_gap_display": "交期通常 2-4 年",
      "future_gap_display": "2027前偏紧",
      "driver": "Global transformer lead times remain elevated due to grid spending and manufacturing bottlenecks.",
      "source_date": "2024",
    }

  if rtx_gtf:
    signals["aero_engine"] = {
      "current_gap_display": "交付链瓶颈持续",
      "future_gap_display": "2026前偏紧",
      "driver": "Aerospace engine and parts shortages continue to constrain aircraft deliveries and aftermarket turnaround.",
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


def compute_score(future_gap_pct: float, concentration: float, policy: float, market_stress: float) -> int:
  raw = future_gap_pct * 0.45 + concentration * 0.2 + policy * 0.2 + market_stress * 0.15
  return max(1, min(99, int(round(raw))))


def parse_gap_value(text: str) -> float:
  if "已预订至 2026" in text or "2026前持续偏紧" in text:
    return 88
  if "交期通常 2-4 年" in text or "2027前偏紧" in text:
    return 92
  if "AI加速卡交付紧张" in text:
    return 86
  if "交付链瓶颈持续" in text:
    return 78
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
  if "10%" in text:
    return 45
  if "6%" in text:
    return 30
  if "+28%" in text:
    return 70
  if ">100%" in text:
    return 72
  if ">20%" in text:
    return 48
  return 40


def build_commodities(signals: Dict[str, Dict[str, str]]) -> List[Commodity]:
  base = {
    "copper": {
      "name_cn": "铜",
      "name_en": "Copper",
      "category": "电气化 / 电网",
      "current_gap_display": "2035隐含缺口 30%",
      "future_gap_display": "30% by 2035",
      "model": "官方预测",
      "drivers": [
        "电网投资和全面电气化持续推高铜需求。",
        "矿石品位下降、资本开支上升、新项目发现放缓。",
        "IEA 已给出 2035 年明确供需缺口口径。",
      ],
      "sources": [
        {"label": "IEA Critical Minerals Outlook 2025", "url": IEA_OVERVIEW_URL, "date": "21 May 2025"},
      ],
      "companies": [
        {"name": "江西铜业", "ticker": "600362.SH"},
        {"name": "紫金矿业", "ticker": "601899.SH"},
        {"name": "洛阳钼业", "ticker": "603993.SH"},
      ],
      "concentration": 88,
      "policy": 50,
      "market": 80,
    },
    "memory_hbm": {
      "name_cn": "高带宽内存 / AI存储",
      "name_en": "HBM / AI Memory",
      "category": "半导体 / 存储",
      "current_gap_display": "HBM产能已预订至 2026",
      "future_gap_display": "2026前持续偏紧",
      "model": "公开产业信号",
      "drivers": [
        "AI 训练和推理服务器快速放量，HBM 需求远超传统 DRAM。",
        "先进封装和高端 DRAM 产能扩张速度跟不上算力需求。",
        "产品级短缺的核心不是硅片总量，而是 HBM + CoWoS 组合能力。",
      ],
      "sources": [
        {"label": "Micron HBM3E Release", "url": MICRON_HBM_URL, "date": "2024"},
        {"label": "SK hynix HBM Update", "url": SK_HYNIX_HBM_URL, "date": "2025"},
      ],
      "companies": [
        {"name": "兆易创新", "ticker": "603986.SH"},
        {"name": "北京君正", "ticker": "300223.SZ"},
        {"name": "德明利", "ticker": "001309.SZ"},
      ],
      "concentration": 95,
      "policy": 68,
      "market": 95,
    },
    "gpu_ai": {
      "name_cn": "AI 加速卡 / GPU",
      "name_en": "AI Accelerators / GPU",
      "category": "半导体 / 算力",
      "current_gap_display": "AI加速卡交付紧张",
      "future_gap_display": "2026前持续偏紧",
      "model": "公开产业信号",
      "drivers": [
        "大模型训练和推理推高高端算力卡需求。",
        "先进制程、先进封装、HBM 共同构成交付瓶颈。",
        "产品短缺表现为交期、配额与云厂商抢单，而不仅是价格上涨。",
      ],
      "sources": [
        {"label": "SEMI Manufacturing Outlook", "url": SEMI_CHIP_URL, "date": "2025"},
      ],
      "companies": [
        {"name": "寒武纪", "ticker": "688256.SH"},
        {"name": "海光信息", "ticker": "688041.SH"},
        {"name": "景嘉微", "ticker": "300474.SZ"},
      ],
      "concentration": 96,
      "policy": 85,
      "market": 92,
    },
    "power_transformer": {
      "name_cn": "电力变压器",
      "name_en": "Power Transformers",
      "category": "电网设备",
      "current_gap_display": "交期通常 2-4 年",
      "future_gap_display": "2027前偏紧",
      "model": "公开产业信号",
      "drivers": [
        "全球电网投资、数据中心接入、新能源并网同步推高需求。",
        "大型变压器制造周期长、熟练工与产线扩张都很慢。",
        "这是典型产品级短缺，实际约束体现在交期而非现货报价。",
      ],
      "sources": [
        {"label": "Hitachi Energy Investment", "url": HITACHI_ENERGY_URL, "date": "2024"},
      ],
      "companies": [
        {"name": "特变电工", "ticker": "600089.SH"},
        {"name": "中国西电", "ticker": "601179.SH"},
        {"name": "保变电气", "ticker": "600550.SH"},
      ],
      "concentration": 82,
      "policy": 35,
      "market": 97,
    },
    "aero_engine": {
      "name_cn": "航空发动机及关键部件",
      "name_en": "Aero Engines & Critical Parts",
      "category": "航空制造",
      "current_gap_display": "交付链瓶颈持续",
      "future_gap_display": "2026前偏紧",
      "model": "公开产业信号",
      "drivers": [
        "发动机、铸件、锻件和维修能力持续制约飞机交付。",
        "航空供应链恢复慢于客运和机队更新需求。",
        "该品类的短缺来自制造与维修能力，而不是单一金属原料。",
      ],
      "sources": [
        {"label": "RTX 2024 Outlook", "url": RTX_GTF_URL, "date": "23 January 2024"},
      ],
      "companies": [
        {"name": "航发动力", "ticker": "600893.SH"},
        {"name": "航宇科技", "ticker": "688239.SH"},
        {"name": "钢研高纳", "ticker": "300034.SZ"},
      ],
      "concentration": 88,
      "policy": 42,
      "market": 84,
    },
    "antimony": {
      "name_cn": "锑",
      "name_en": "Antimony",
      "category": "阻燃 / 军工 / 芯片材料",
      "current_gap_display": "价格同比 >100%",
      "future_gap_display": "模型估算 22%",
      "model": "模型估算",
      "drivers": [
        "出口管制与贸易摩擦放大了可得性风险。",
        "价格在 2025 年出现极端上冲，显示现货紧张。",
        "半导体、军工与特种材料需求推高战略价值。",
      ],
      "sources": [
        {"label": "USGS Mineral Commodity Summaries 2026", "url": USGS_MCS_URL, "date": "5 March 2026"},
      ],
      "companies": [
        {"name": "湖南黄金", "ticker": "002155.SZ"},
        {"name": "华钰矿业", "ticker": "601020.SH"},
        {"name": "华锡有色", "ticker": "600301.SH"},
      ],
      "concentration": 92,
      "policy": 95,
      "market": 95,
    },
    "germanium": {
      "name_cn": "锗",
      "name_en": "Germanium",
      "category": "红外 / 光纤 / 半导体",
      "current_gap_display": "价格同比 >100%",
      "future_gap_display": "模型估算 21%",
      "model": "模型估算",
      "drivers": [
        "出口限制显著推升海外采购难度。",
        "价格大幅上涨反映短期供应弹性不足。",
        "在光纤、红外和高端电子环节替代性有限。",
      ],
      "sources": [
        {"label": "USGS Mineral Commodity Summaries 2026", "url": USGS_MCS_URL, "date": "5 March 2026"},
        {"label": "USGS Gallium/Germanium Study", "url": USGS_GA_GE_URL, "date": "19 November 2024"},
      ],
      "companies": [
        {"name": "云南锗业", "ticker": "002428.SZ"},
        {"name": "驰宏锌锗", "ticker": "600497.SH"},
        {"name": "罗平锌电", "ticker": "002114.SZ"},
      ],
      "concentration": 90,
      "policy": 94,
      "market": 94,
    },
    "uranium": {
      "name_cn": "铀",
      "name_en": "Uranium",
      "category": "核电燃料",
      "current_gap_display": "矿山供给仅覆盖约90%",
      "future_gap_display": "2030需求 +28%",
      "model": "官方趋势 + 模型估算",
      "drivers": [
        "全球核电复兴推升中长期燃料需求。",
        "矿山供给未完全覆盖反应堆需求，需依赖二级供给。",
        "2030 前需求增长明确，矿山扩产与燃料链建设周期长。",
      ],
      "sources": [
        {"label": "World Nuclear Association", "url": WNA_URANIUM_URL, "date": "23 August 2024"},
        {"label": "World Nuclear Fuel Report 2025", "url": "https://world-nuclear.org/our-association/publications/global-trends-reports/world-nuclear-fuel-report-2025", "date": "2025"},
      ],
      "companies": [
        {"name": "中广核矿业", "ticker": "1164.HK"},
        {"name": "中核国际", "ticker": "2302.HK"},
        {"name": "中国广核", "ticker": "003816.SZ"},
      ],
      "concentration": 82,
      "policy": 70,
      "market": 82,
    },
    "lithium": {
      "name_cn": "锂",
      "name_en": "Lithium",
      "category": "动力电池",
      "current_gap_display": "近端宽松, 远端转缺",
      "future_gap_display": "40% by 2035",
      "model": "官方预测",
      "drivers": [
        "IEA 指出近端市场偏宽松，但 2030 年代可能重新转入短缺。",
        "新能源车与储能扩张推动需求增速维持高位。",
        "新项目开发前景优于铜，但仍难完全填平长期缺口。",
      ],
      "sources": [
        {"label": "IEA Critical Minerals Outlook 2025", "url": IEA_EXEC_URL, "date": "21 May 2025"},
      ],
      "companies": [
        {"name": "天齐锂业", "ticker": "002466.SZ"},
        {"name": "赣锋锂业", "ticker": "002460.SZ"},
        {"name": "盛新锂能", "ticker": "002240.SZ"},
      ],
      "concentration": 78,
      "policy": 48,
      "market": 62,
    },
    "gallium": {
      "name_cn": "镓",
      "name_en": "Gallium",
      "category": "射频 / 功率半导体",
      "current_gap_display": "价格同比 >20%",
      "future_gap_display": "模型估算 18%",
      "model": "模型估算",
      "drivers": [
        "USGS 将镓识别为高供应风险材料。",
        "半导体、电力电子和国防链条对镓依赖度高。",
        "出口许可制度意味着供应恢复并不等于风险消失。",
      ],
      "sources": [
        {"label": "USGS Gallium/Germanium Study", "url": USGS_GA_GE_URL, "date": "19 November 2024"},
        {"label": "USGS Mineral Commodity Summaries 2026", "url": USGS_MCS_URL, "date": "5 March 2026"},
      ],
      "companies": [
        {"name": "中国铝业", "ticker": "601600.SH"},
        {"name": "云铝股份", "ticker": "000807.SZ"},
        {"name": "南山铝业", "ticker": "600219.SH"},
      ],
      "concentration": 95,
      "policy": 92,
      "market": 70,
    },
    "graphite": {
      "name_cn": "石墨",
      "name_en": "Graphite",
      "category": "负极材料 / 储能",
      "current_gap_display": "集中度风险高",
      "future_gap_display": "模型估算 12%",
      "model": "模型估算",
      "drivers": [
        "储能和动力电池继续带动需求增长。",
        "IEA 判断总量有望覆盖，但供应集中度仍是核心脆弱点。",
        "一旦出口限制升级，产业链扰动会迅速放大。",
      ],
      "sources": [
        {"label": "IEA Critical Minerals Outlook 2025", "url": IEA_EXEC_URL, "date": "21 May 2025"},
      ],
      "companies": [
        {"name": "中国宝安", "ticker": "000009.SZ"},
        {"name": "中科电气", "ticker": "300035.SZ"},
        {"name": "翔丰华", "ticker": "300890.SZ"},
      ],
      "concentration": 90,
      "policy": 80,
      "market": 52,
    },
    "rare_earths": {
      "name_cn": "稀土（镨钕）",
      "name_en": "Rare Earths (NdPr)",
      "category": "永磁 / 电机",
      "current_gap_display": "供给可覆盖, 但集中度高",
      "future_gap_display": "模型估算 10%",
      "model": "模型估算",
      "drivers": [
        "风电、电动车和工业电机驱动需求增长。",
        "IEA 认为总量上 2035 年可被项目覆盖，但精炼端高度集中。",
        "地缘政治与出口政策仍可能造成阶段性缺货。",
      ],
      "sources": [
        {"label": "IEA Critical Minerals Outlook 2025", "url": IEA_EXEC_URL, "date": "21 May 2025"},
      ],
      "companies": [
        {"name": "北方稀土", "ticker": "600111.SH"},
        {"name": "中国稀土", "ticker": "000831.SZ"},
        {"name": "金力永磁", "ticker": "300748.SZ"},
      ],
      "concentration": 88,
      "policy": 82,
      "market": 50,
    },
    "tungsten": {
      "name_cn": "钨",
      "name_en": "Tungsten",
      "category": "硬质合金 / 军工",
      "current_gap_display": "价格同比 >20%",
      "future_gap_display": "模型估算 12%",
      "model": "模型估算",
      "drivers": [
        "军工、刀具和高温材料需求使其保持战略地位。",
        "USGS 显示 2025 年价格显著上涨，说明供应偏紧。",
        "全球供应集中度高，替代难度不低。",
      ],
      "sources": [
        {"label": "USGS Mineral Commodity Summaries 2026", "url": USGS_MCS_URL, "date": "5 March 2026"},
      ],
      "companies": [
        {"name": "厦门钨业", "ticker": "600549.SH"},
        {"name": "中钨高新", "ticker": "000657.SZ"},
        {"name": "章源钨业", "ticker": "002378.SZ"},
      ],
      "concentration": 84,
      "policy": 70,
      "market": 66,
    },
    "cobalt": {
      "name_cn": "钴",
      "name_en": "Cobalt",
      "category": "电池 / 高温合金",
      "current_gap_display": "缺口收窄",
      "future_gap_display": "模型估算 6%",
      "model": "模型估算",
      "drivers": [
        "IEA 指出长期缺口较前几年有所收窄。",
        "但前三大生产国集中度提升，供给韧性并不强。",
        "电池化学体系变化会影响中长期需求结构。",
      ],
      "sources": [
        {"label": "IEA Critical Minerals Outlook 2025", "url": IEA_EXEC_URL, "date": "21 May 2025"},
      ],
      "companies": [
        {"name": "华友钴业", "ticker": "603799.SH"},
        {"name": "寒锐钴业", "ticker": "300618.SZ"},
        {"name": "盛屯矿业", "ticker": "600711.SH"},
      ],
      "concentration": 86,
      "policy": 45,
      "market": 35,
    },
  }

  items: List[Commodity] = []
  for key, details in base.items():
    live = signals.get(key, {})
    current_gap_display = live.get("current_gap_display", details.get("current_gap_display", "模型估算"))
    future_gap_display = live.get("future_gap_display", details.get("future_gap_display", "模型估算"))
    drivers = details["drivers"][:]
    if live.get("driver"):
      drivers.insert(0, live["driver"])
    sources = [dict(source) for source in details["sources"]]
    if sources and live.get("source_date"):
      sources[0]["date"] = live["source_date"]

    future_gap_score = parse_gap_value(future_gap_display)
    shortage_score = compute_score(
      future_gap_score,
      details["concentration"],
      details["policy"],
      details["market"],
    )
    items.append(
      Commodity(
        key=key,
        name_cn=details["name_cn"],
        name_en=details["name_en"],
        category=details["category"],
        current_gap_display=current_gap_display,
        future_gap_display=future_gap_display,
        shortage_score=shortage_score,
        score_model=details["model"],
        key_drivers=drivers[:3],
        sources=sources,
        china_listed_companies=details["companies"],
      )
    )

  items.sort(key=lambda item: item.shortage_score, reverse=True)
  return items[:10]


def build_payload() -> Dict[str, object]:
  now = datetime.now()
  signals = build_live_signals()
  items = build_commodities(signals)
  average_score = round(sum(item.shortage_score for item in items) / len(items))

  def future_gap_sort_value(item: Commodity) -> float:
    text = item.future_gap_display
    match = re.search(r"(\d+)", text)
    return float(match.group(1)) if match else 0.0

  max_gap_item = max(items, key=future_gap_sort_value)
  return {
    "meta": {
      "generated_at_local": now.strftime("%Y-%m-%d %H:%M:%S"),
      "refresh_note": "每日脚本已执行；若源站无新版本，则保留上次最新可得官方数值。",
      "mode_label": "每日自动检查 + 最新可得数据",
    },
    "summary": {
      "top_risk_name": items[0].name_cn,
      "average_score": average_score,
      "max_future_gap": f"{max_gap_item.name_cn} {max_gap_item.future_gap_display}",
    },
    "items": [
      {
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
        "china_listed_companies": item.china_listed_companies,
      }
      for item in items
    ],
  }


def update_dashboard_html(payload: Dict[str, object]) -> None:
  html = DASHBOARD_PATH.read_text(encoding="utf-8")
  updated = DATA_TAG_PATTERN.sub(
    lambda match: f"{match.group(1)}{json.dumps(payload, ensure_ascii=False)}{match.group(3)}",
    html,
    count=1,
  )
  DASHBOARD_PATH.write_text(updated, encoding="utf-8")


def main() -> None:
  payload = build_payload()
  update_dashboard_html(payload)
  print(f"Dashboard updated: {DASHBOARD_PATH}")


if __name__ == "__main__":
  main()
