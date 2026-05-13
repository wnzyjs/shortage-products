const DATA_SCRIPT_URL = "./data/latest.js";
const GITHUB_ACTIONS_URL = "";

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) {
    el.textContent = value;
  }
}

function renderSources(sources) {
  return sources
    .map(
      (source) =>
        `<a class="pill" href="${source.url}" target="_blank" rel="noreferrer">${source.label}<span>${source.date}</span></a>`,
    )
    .join("");
}

function renderCompanies(companies) {
  return companies
    .map(
      (company) =>
        `<span class="pill">${company.name}<span>${company.ticker}</span></span>`,
    )
    .join("");
}

function renderDashboard(payload) {
  const rankingEl = document.getElementById("ranking-grid");
  const tableEl = document.getElementById("detail-table-body");

  setText("run-date", payload.meta.generated_at_local);
  setText("source-note", payload.meta.refresh_note);
  setText("top-risk", payload.summary.top_risk_name);
  setText("avg-score", String(payload.summary.average_score));
  setText("future-gap", payload.summary.max_future_gap);
  setText("update-mode", payload.meta.mode_label);

  rankingEl.innerHTML = payload.items
    .map(
      (item, index) => `
        <article class="card">
          <span class="rank">#${index + 1}</span>
          <div class="commodity-name">${item.name_cn}</div>
          <div class="commodity-meta">${item.name_en} | ${item.category}</div>
          <div class="score-bar"><div class="score-fill" style="width: ${item.shortage_score}%"></div></div>
          <div class="metrics">
            <div class="metric">
              <span class="key">紧缺评分</span>
              <span class="val">${item.shortage_score}</span>
            </div>
            <div class="metric">
              <span class="key">当前缺口/压力</span>
              <span class="val">${item.current_gap_display}</span>
            </div>
            <div class="metric">
              <span class="key">未来缺口预测</span>
              <span class="val">${item.future_gap_display}</span>
            </div>
          </div>
          <ul class="bullets">
            ${item.key_drivers.map((driver) => `<li>${driver}</li>`).join("")}
          </ul>
          <div class="company-list">${renderCompanies(item.china_listed_companies)}</div>
          <div class="source-list">${renderSources(item.sources)}</div>
        </article>
      `,
    )
    .join("");

  tableEl.innerHTML = payload.items
    .map(
      (item, index) => `
        <tr>
          <td><span class="chip">#${index + 1}</span></td>
          <td>
            <strong>${item.name_cn}</strong><br>
            <span class="muted">${item.name_en}</span>
          </td>
          <td>${item.current_gap_display}</td>
          <td>${item.future_gap_display}</td>
          <td>${item.score_model}</td>
          <td>${item.china_listed_companies.map((company) => `${company.name} ${company.ticker}`).join(" / ")}</td>
        </tr>
      `,
    )
    .join("");
}

function loadDataScript() {
  return new Promise((resolve, reject) => {
    delete window.DASHBOARD_DATA;

    const oldScript = document.getElementById("dashboard-data-script");
    if (oldScript) {
      oldScript.remove();
    }

    const script = document.createElement("script");
    script.id = "dashboard-data-script";
    script.src = `${DATA_SCRIPT_URL}?t=${Date.now()}`;
    script.onload = () => {
      if (window.DASHBOARD_DATA) {
        resolve(window.DASHBOARD_DATA);
      } else {
        reject(new Error("未找到已发布数据变量"));
      }
    };
    script.onerror = () => reject(new Error("无法加载 data/latest.js"));
    document.body.appendChild(script);
  });
}

async function loadDashboardData() {
  const statusEl = document.getElementById("refresh-status");
  const buttonEl = document.getElementById("refresh-button");
  statusEl.textContent = "正在加载已发布数据...";
  buttonEl.disabled = true;

  try {
    const payload = await loadDataScript();
    renderDashboard(payload);
    statusEl.textContent = `已刷新，当前展示数据生成于 ${payload.meta.generated_at_local}`;
  } catch (error) {
    statusEl.textContent = `刷新失败：${error.message}`;
  } finally {
    buttonEl.disabled = false;
  }
}

function openActionsPage() {
  const statusEl = document.getElementById("refresh-status");
  if (GITHUB_ACTIONS_URL) {
    window.open(GITHUB_ACTIONS_URL, "_blank", "noopener,noreferrer");
    statusEl.textContent = "已打开 GitHub Actions，请先运行云端更新工作流。";
    return;
  }
  statusEl.textContent = "请先在 GitHub 仓库的 Actions 页面运行 Update Dashboard Data，再回来点“刷新已发布数据”。";
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("refresh-button").addEventListener("click", loadDashboardData);
  document.getElementById("trigger-update-button").addEventListener("click", openActionsPage);
  loadDashboardData();
});
