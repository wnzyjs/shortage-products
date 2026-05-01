window.DASHBOARD_DATA = {
  "meta": {
    "generated_at_local": "2026-05-01 18:09:11",
    "refresh_note": "点击网页按钮会重新加载已发布的 latest.js；若要生成新数据，请本地运行更新脚本后重新发布。",
    "mode_label": "手动刷新页面数据"
  },
  "summary": {
    "top_risk_name": "AI 加速卡 / GPU",
    "average_score": 78,
    "max_future_gap": "电力变压器 2027前偏紧"
  },
  "items": [
    {
      "key": "gpu_ai",
      "name_cn": "AI 加速卡 / GPU",
      "name_en": "AI Accelerators / GPU",
      "category": "半导体 / 算力",
      "current_gap_display": "AI 加速卡交付紧张",
      "future_gap_display": "2026前持续偏紧",
      "shortage_score": 90,
      "score_model": "公开产业信号",
      "key_drivers": [
        "大模型训练和推理推高高端算力卡需求。",
        "先进制程、先进封装和 HBM 一起构成交付瓶颈。",
        "短缺表现为交期和配额，而不只是价格波动。"
      ],
      "sources": [
        {
          "label": "SEMI Manufacturing Outlook",
          "url": "https://www.semi.org/en/news-media-press-releases/global-semiconductor-manufacturing-industry-sees-investment-growth",
          "date": "2025"
        }
      ],
      "china_listed_companies": [
        {
          "name": "寒武纪",
          "ticker": "688256.SH"
        },
        {
          "name": "海光信息",
          "ticker": "688041.SH"
        },
        {
          "name": "景嘉微",
          "ticker": "300474.SZ"
        }
      ]
    },
    {
      "key": "memory_hbm",
      "name_cn": "高带宽内存 / AI 存储",
      "name_en": "HBM / AI Memory",
      "category": "半导体 / 存储",
      "current_gap_display": "HBM 产能已预订至 2026",
      "future_gap_display": "2026前持续偏紧",
      "shortage_score": 86,
      "score_model": "公开产业信号",
      "key_drivers": [
        "AI 服务器扩张推高 HBM 需求。",
        "先进封装与高端 DRAM 扩产速度跟不上需求。",
        "产品级短缺核心是 HBM 与 CoWoS 组合能力。"
      ],
      "sources": [
        {
          "label": "Micron HBM3E Release",
          "url": "https://investors.micron.com/news-releases/news-release-details/micron-begins-volume-production-industrys-first-hbm3e-memory",
          "date": "2024"
        },
        {
          "label": "SK hynix HBM Update",
          "url": "https://news.skhynix.com/sk-hynix-begins-mass-production-of-worlds-first-hbm4-12-layer-samples/",
          "date": "2025"
        }
      ],
      "china_listed_companies": [
        {
          "name": "兆易创新",
          "ticker": "603986.SH"
        },
        {
          "name": "北京君正",
          "ticker": "300223.SZ"
        },
        {
          "name": "德明利",
          "ticker": "001309.SZ"
        }
      ]
    },
    {
      "key": "antimony",
      "name_cn": "锑",
      "name_en": "Antimony",
      "category": "阻燃 / 军工 / 芯片材料",
      "current_gap_display": "价格同比 >100%",
      "future_gap_display": "模型估算 22%",
      "shortage_score": 82,
      "score_model": "模型估算",
      "key_drivers": [
        "出口管制与贸易摩擦放大可得性风险。",
        "价格剧烈上行显示现货市场紧张。",
        "半导体、军工和特种材料需求抬高战略价值。"
      ],
      "sources": [
        {
          "label": "USGS Mineral Commodity Summaries 2026",
          "url": "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf",
          "date": "5 March 2026"
        }
      ],
      "china_listed_companies": [
        {
          "name": "湖南黄金",
          "ticker": "002155.SZ"
        },
        {
          "name": "华钰矿业",
          "ticker": "601020.SH"
        },
        {
          "name": "华锡有色",
          "ticker": "600301.SH"
        }
      ]
    },
    {
      "key": "germanium",
      "name_cn": "锗",
      "name_en": "Germanium",
      "category": "红外 / 光纤 / 半导体",
      "current_gap_display": "价格同比 >100%",
      "future_gap_display": "模型估算 21%",
      "shortage_score": 81,
      "score_model": "模型估算",
      "key_drivers": [
        "出口限制显著推升海外采购难度。",
        "价格大幅上涨反映短期供应弹性不足。",
        "在红外、光纤和高端电子环节替代性有限。"
      ],
      "sources": [
        {
          "label": "USGS Mineral Commodity Summaries 2026",
          "url": "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf",
          "date": "5 March 2026"
        },
        {
          "label": "USGS Gallium/Germanium Study",
          "url": "https://www.usgs.gov/news/national-news-release/usgs-critical-minerals-study-bans-gallium-and-germanium-exports-could",
          "date": "19 November 2024"
        }
      ],
      "china_listed_companies": [
        {
          "name": "云南锗业",
          "ticker": "002428.SZ"
        },
        {
          "name": "驰宏锌锗",
          "ticker": "600497.SH"
        },
        {
          "name": "罗平锌电",
          "ticker": "002114.SZ"
        }
      ]
    },
    {
      "key": "power_transformer",
      "name_cn": "电力变压器",
      "name_en": "Power Transformers",
      "category": "电网设备",
      "current_gap_display": "交期通常 2-4 年",
      "future_gap_display": "2027前偏紧",
      "shortage_score": 79,
      "score_model": "公开产业信号",
      "key_drivers": [
        "全球电网投资、数据中心接入和新能源并网同步推高需求。",
        "大型变压器制造周期长，产能扩张慢。",
        "典型产品级短缺，约束主要体现为交付周期。"
      ],
      "sources": [
        {
          "label": "Hitachi Energy Investment",
          "url": "https://www.hitachienergy.com/us/en/news-and-events/press-releases/2024/06/hitachi-energy-invests-additional-155-million-usd",
          "date": "2024"
        }
      ],
      "china_listed_companies": [
        {
          "name": "特变电工",
          "ticker": "600089.SH"
        },
        {
          "name": "中国西电",
          "ticker": "601179.SH"
        },
        {
          "name": "保变电气",
          "ticker": "600550.SH"
        }
      ]
    },
    {
      "key": "copper",
      "name_cn": "铜",
      "name_en": "Copper",
      "category": "电气化 / 电网",
      "current_gap_display": "2035隐含缺口 30%",
      "future_gap_display": "30% by 2035",
      "shortage_score": 76,
      "score_model": "官方预测",
      "key_drivers": [
        "电网投资和全面电气化持续推高铜需求。",
        "矿石品位下降、资本开支上升、新项目发现放缓。",
        "IEA 已给出 2035 年明确供需缺口口径。"
      ],
      "sources": [
        {
          "label": "IEA Critical Minerals Outlook 2025",
          "url": "https://www.iea.org/reports/global-critical-minerals-outlook-2025/overview-of-outlook-for-key-minerals",
          "date": "21 May 2025"
        }
      ],
      "china_listed_companies": [
        {
          "name": "江西铜业",
          "ticker": "600362.SH"
        },
        {
          "name": "紫金矿业",
          "ticker": "601899.SH"
        },
        {
          "name": "洛阳钼业",
          "ticker": "603993.SH"
        }
      ]
    },
    {
      "key": "gallium",
      "name_cn": "镓",
      "name_en": "Gallium",
      "category": "射频 / 功率半导体",
      "current_gap_display": "价格同比 >20%",
      "future_gap_display": "模型估算 18%",
      "shortage_score": 76,
      "score_model": "模型估算",
      "key_drivers": [
        "USGS 将镓识别为高供应风险材料。",
        "半导体、电力电子和国防链条对镓依赖度高。",
        "出口许可制度意味着供应恢复并不等于风险消失。"
      ],
      "sources": [
        {
          "label": "USGS Gallium/Germanium Study",
          "url": "https://www.usgs.gov/news/national-news-release/usgs-critical-minerals-study-bans-gallium-and-germanium-exports-could",
          "date": "19 November 2024"
        },
        {
          "label": "USGS Mineral Commodity Summaries 2026",
          "url": "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026.pdf",
          "date": "5 March 2026"
        }
      ],
      "china_listed_companies": [
        {
          "name": "中国铝业",
          "ticker": "601600.SH"
        },
        {
          "name": "云铝股份",
          "ticker": "000807.SZ"
        },
        {
          "name": "南山铝业",
          "ticker": "600219.SH"
        }
      ]
    },
    {
      "key": "lithium",
      "name_cn": "锂",
      "name_en": "Lithium",
      "category": "动力电池",
      "current_gap_display": "近端宽松，远端转缺",
      "future_gap_display": "40% by 2035",
      "shortage_score": 75,
      "score_model": "官方预测",
      "key_drivers": [
        "IEA 指出近端市场偏宽松，但 2030 年代可能重新转入短缺。",
        "新能源车与储能扩张推动需求增速维持高位。",
        "新项目开发前景优于铜，但仍难完全填平长期缺口。"
      ],
      "sources": [
        {
          "label": "IEA Critical Minerals Outlook 2025",
          "url": "https://www.iea.org/reports/global-critical-minerals-outlook-2025/executive-summary",
          "date": "21 May 2025"
        }
      ],
      "china_listed_companies": [
        {
          "name": "天齐锂业",
          "ticker": "002466.SZ"
        },
        {
          "name": "赣锋锂业",
          "ticker": "002460.SZ"
        },
        {
          "name": "盛新锂能",
          "ticker": "002240.SZ"
        }
      ]
    },
    {
      "key": "uranium",
      "name_cn": "铀",
      "name_en": "Uranium",
      "category": "核电燃料",
      "current_gap_display": "矿山供给仅覆盖约90%",
      "future_gap_display": "2030需求 +28%",
      "shortage_score": 74,
      "score_model": "官方趋势 + 模型估算",
      "key_drivers": [
        "全球核电复兴推升中长期燃料需求。",
        "矿山供给未完全覆盖反应堆需求。",
        "2030 前需求增长明确，扩产周期长。"
      ],
      "sources": [
        {
          "label": "World Nuclear Association",
          "url": "https://world-nuclear.org/information-library/Nuclear-Fuel-Cycle/Uranium-Resources/Uranium-Markets",
          "date": "23 August 2024"
        }
      ],
      "china_listed_companies": [
        {
          "name": "中广核矿业",
          "ticker": "1164.HK"
        },
        {
          "name": "中核国际",
          "ticker": "2302.HK"
        },
        {
          "name": "中国广核",
          "ticker": "003816.SZ"
        }
      ]
    },
    {
      "key": "graphite",
      "name_cn": "石墨",
      "name_en": "Graphite",
      "category": "负极材料 / 储能",
      "current_gap_display": "集中度风险高",
      "future_gap_display": "模型估算 12%",
      "shortage_score": 64,
      "score_model": "模型估算",
      "key_drivers": [
        "储能和动力电池继续带动需求增长。",
        "IEA 认为总量有望覆盖，但供应集中度仍是脆弱点。",
        "一旦出口限制升级，产业链扰动会被放大。"
      ],
      "sources": [
        {
          "label": "IEA Critical Minerals Outlook 2025",
          "url": "https://www.iea.org/reports/global-critical-minerals-outlook-2025/executive-summary",
          "date": "21 May 2025"
        }
      ],
      "china_listed_companies": [
        {
          "name": "中国宝安",
          "ticker": "000009.SZ"
        },
        {
          "name": "中科电气",
          "ticker": "300035.SZ"
        },
        {
          "name": "翔丰华",
          "ticker": "300890.SZ"
        }
      ]
    }
  ]
};
