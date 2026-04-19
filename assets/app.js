(function () {
  const dataTag = document.getElementById("dashboard-data");
  if (!dataTag) {
    return;
  }

  const payload = JSON.parse(dataTag.textContent);

  const setText = (id, value) => {
    const el = document.getElementById(id);
    if (el) {
      el.textContent = value;
    }
  };

  const renderSources = (sources) =>
    sources
      .map(
        (source) =>
          `<a class="pill" href="${source.url}" target="_blank" rel="noreferrer">${source.label}<span>${source.date}</span></a>`,
      )
      .join("");

  const renderCompanies = (companies) =>
    companies
      .map(
        (company) =>
          `<span class="pill">${company.name}<span>${company.ticker}</span></span>`,
      )
      .join("");

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
})();
