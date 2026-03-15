const BASE = "http://127.0.0.1:5000";

function fmtVol(v) {
    v = parseFloat(v);
    if (isNaN(v)) return "--";
    if (v >= 1e7) return (v / 1e7).toFixed(2) + " Cr";
    if (v >= 1e5) return (v / 1e5).toFixed(2) + " L";
    if (v >= 1e3) return (v / 1e3).toFixed(1) + "K";
    return v.toString();
}

function rankBadge(i) {
    if (i === 0) return '<span class="rank-badge rank-1">1</span>';
    if (i === 1) return '<span class="rank-badge rank-2">2</span>';
    if (i === 2) return '<span class="rank-badge rank-3">3</span>';
    return '<span class="rank-badge rank-n">' + (i + 1) + '</span>';
}

async function fetchJSON(endpoint) {
    try {
        const res  = await fetch(BASE + endpoint);
        const data = await res.json();
        return data;
    } catch (e) {
        console.error("Fetch error " + endpoint, e);
        return null;
    }
}

const loaded = {};

function showTab(name, btn) {
    document.querySelectorAll(".section").forEach(s => s.classList.remove("active"));
    document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
    document.getElementById(name).classList.add("active");
    btn.classList.add("active");
    if (!loaded[name]) {
        loaded[name] = true;
        const loaders = {
            overview   : loadOverview,
            yearly     : loadYearly,
            monthly    : loadMonthly,
            returns    : loadReturns,
            volume     : loadVolume,
            signals    : loadSignals,
            pricebands : loadPriceBands,
            dividends  : loadDividends,
            top10      : loadTop10,
            recent     : loadRecent,
            ml         : loadML,
            predictions: loadPredictions
        };
        if (loaders[name]) loaders[name]();
    }
}

async function loadOverview() {
    const summary = await fetchJSON("/api/tcs/summary");
    if (!summary) return;

    document.getElementById("ticker-price").textContent = "Rs." + summary.latest_close;
    const chEl = document.getElementById("ticker-change");
    const chv  = summary.day_change;
    const chp  = summary.day_change_pct;
    chEl.textContent = (chv >= 0 ? "+" : "") + chv + " (" + chp + "%)";
    chEl.className   = chv >= 0 ? "ticker-change-up" : "ticker-change-down";

    const kpis = [
        { label: "Latest Close",  value: "Rs." + summary.latest_close,   sub: summary.latest_date,                          cls: "blue-top",   sc: "background:#2979ff;" },
        { label: "All Time High", value: "Rs." + summary.all_time_high,   sub: "Highest ever price",                        cls: "green-top",  sc: "background:#00e676;" },
        { label: "All Time Low",  value: "Rs." + summary.all_time_low,    sub: "Lowest ever price",                         cls: "lav-top",    sc: "background:#b39ddb;" },
        { label: "Avg Close",     value: "Rs." + summary.avg_close,       sub: "Historical average",                        cls: "silver-top", sc: "background:#bdbdbd;" },
        { label: "Trading Days",  value: summary.total_days,              sub: summary.date_from + " to " + summary.date_to,cls: "gold-top",   sc: "background:#ffd740;" },
        { label: "Latest Open",   value: "Rs." + summary.latest_open,     sub: "Today open price",                          cls: "blue-top",   sc: "background:#2979ff;" },
        { label: "Latest High",   value: "Rs." + summary.latest_high,     sub: "Today intraday high",                       cls: "green-top",  sc: "background:#00e676;" },
        { label: "Latest Low",    value: "Rs." + summary.latest_low,      sub: "Today intraday low",                        cls: "lav-top",    sc: "background:#b39ddb;" },
        { label: "Avg Volume",    value: fmtVol(summary.avg_volume),      sub: "Daily avg shares traded",                   cls: "silver-top", sc: "background:#bdbdbd;" },
        { label: "Total Divid.",  value: "Rs." + summary.total_dividends, sub: "All dividends paid",                        cls: "gold-top",   sc: "background:#ffd740;" }
    ];

    document.getElementById("kpi-cards").innerHTML = kpis.map(k => `
        <div class="kpi-card ${k.cls}">
            <div class="kpi-sparkle" style="${k.sc}"></div>
            <div class="kpi-label">${k.label}</div>
            <div class="kpi-value">${k.value}</div>
            <div class="kpi-sub">${k.sub}</div>
        </div>`).join("");
}

async function loadYearly() {
    const yearly = await fetchJSON("/api/tcs/yearly");
    if (!yearly) return;

    const best   = yearly.reduce((a, b) => a.avg_close > b.avg_close ? a : b);
    const highY  = yearly.reduce((a, b) => a.max_close > b.max_close ? a : b);
    const volY   = yearly.reduce((a, b) => a.avg_volume > b.avg_volume ? a : b);

    document.getElementById("yearly-stat-boxes").innerHTML = `
        <div class="stat-box">
            <div class="stat-box-title">Best Year Avg</div>
            <div class="stat-box-value">${best.Year}</div>
            <div class="stat-box-label">Rs.${best.avg_close} avg close</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">All Time High Year</div>
            <div class="stat-box-value">${highY.Year}</div>
            <div class="stat-box-label">Rs.${highY.max_close} high</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">Total Years</div>
            <div class="stat-box-value">${yearly.length}</div>
            <div class="stat-box-label">2002 to ${yearly[yearly.length - 1].Year}</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">Highest Volume Year</div>
            <div class="stat-box-value">${volY.Year}</div>
            <div class="stat-box-label">Max trading activity</div>
        </div>`;
}

async function loadMonthly() {
    const best = await fetchJSON("/api/tcs/best_months");
    if (!best) return;

    document.getElementById("monthly-stat-boxes").innerHTML = `
        <div class="stat-box">
            <div class="stat-box-title">Best Month</div>
            <div class="stat-box-value">${best[0].Month_Name}</div>
            <div class="stat-box-label">Highest avg return</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">Worst Month</div>
            <div class="stat-box-value">${best[best.length - 1].Month_Name}</div>
            <div class="stat-box-label">Lowest avg return</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">Avg Return Best</div>
            <div class="stat-box-value" style="color:#00e676">${best[0].avg_return}%</div>
            <div class="stat-box-label">Daily avg in ${best[0].Month_Name}</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">Total Months</div>
            <div class="stat-box-value">12</div>
            <div class="stat-box-label">Jan to Dec analysis</div>
        </div>`;
}

async function loadReturns() {
    const returns = await fetchJSON("/api/tcs/daily_returns");
    if (!returns) return;

    const totPos = returns.reduce((a, b) => a + b.positive_days, 0);
    const totNeg = returns.reduce((a, b) => a + b.negative_days, 0);
    const bestY  = returns.reduce((a, b) => a.total_return > b.total_return ? a : b);
    const worstY = returns.reduce((a, b) => a.total_return < b.total_return ? a : b);

    document.getElementById("returns-stat-boxes").innerHTML = `
        <div class="stat-box">
            <div class="stat-box-title">Total Positive Days</div>
            <div class="stat-box-value" style="color:#00e676">${totPos}</div>
            <div class="stat-box-label">All time green days</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">Total Negative Days</div>
            <div class="stat-box-value" style="color:#ff1744">${totNeg}</div>
            <div class="stat-box-label">All time red days</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">Best Year</div>
            <div class="stat-box-value">${bestY.Year}</div>
            <div class="stat-box-label">+${bestY.total_return.toFixed(1)}% total</div>
        </div>
        <div class="stat-box">
            <div class="stat-box-title">Worst Year</div>
            <div class="stat-box-value">${worstY.Year}</div>
            <div class="stat-box-label">${worstY.total_return.toFixed(1)}% total</div>
        </div>`;
}

async function loadVolume() {
    const topVol = await fetchJSON("/api/tcs/top10_volume");
    if (!topVol) return;

    document.getElementById("vol-table-body").innerHTML = topVol.map((r, i) => `
        <tr>
            <td>${rankBadge(i)}</td>
            <td>${r.Date}</td>
            <td>Rs.${r.Open}</td>
            <td>Rs.${r.High}</td>
            <td>Rs.${r.Low}</td>
            <td>Rs.${r.Close}</td>
            <td><span class="badge badge-blue">${fmtVol(r.Volume)}</span></td>
        </tr>`).join("");
}

async function loadSignals() {
    const signals = await fetchJSON("/api/tcs/signals");
    if (!signals) return;

    document.getElementById("signals-table-body").innerHTML = signals.map(r => {
        const dom = r.buy_days >= r.sell_days
            ? '<span class="badge badge-green">BUY</span>'
            : '<span class="badge badge-red">SELL</span>';
        return `<tr>
            <td>${r.Year}</td>
            <td><span class="badge badge-green">${r.buy_days}</span></td>
            <td><span class="badge badge-red">${r.sell_days}</span></td>
            <td>${dom}</td>
        </tr>`;
    }).join("");
}

async function loadPriceBands() {
    const bands = await fetchJSON("/api/tcs/price_bands");
    if (!bands) return;

    const total = bands.reduce((a, b) => a + b.trading_days, 0);
    document.getElementById("bands-table-body").innerHTML = bands.map(b => `
        <tr>
            <td><span class="badge badge-blue">${b.price_band}</span></td>
            <td>${b.trading_days}</td>
            <td>${((b.trading_days / total) * 100).toFixed(1)}%</td>
        </tr>`).join("");
}

async function loadDividends() {
    const divs = await fetchJSON("/api/tcs/dividends");
    if (!divs) return;

    document.getElementById("div-table-body").innerHTML = divs.map(d => `
        <tr>
            <td>${d.Date}</td>
            <td>Rs.${d.Close}</td>
            <td><span class="badge badge-gold">Rs.${d.Dividends}</span></td>
        </tr>`).join("");
}

async function loadTop10() {
    const [high, vol] = await Promise.all([
        fetchJSON("/api/tcs/top10_high"),
        fetchJSON("/api/tcs/top10_volume")
    ]);

    if (high) {
        document.getElementById("top10-high-body").innerHTML = high.map((r, i) => `
            <tr>
                <td>${rankBadge(i)}</td>
                <td>${r.Date}</td>
                <td>Rs.${r.Open}</td>
                <td>Rs.${r.High}</td>
                <td>Rs.${r.Low}</td>
                <td><span class="badge badge-green">Rs.${r.Close}</span></td>
                <td>${fmtVol(r.Volume)}</td>
            </tr>`).join("");
    }

    if (vol) {
        document.getElementById("top10-vol-body").innerHTML = vol.map((r, i) => `
            <tr>
                <td>${rankBadge(i)}</td>
                <td>${r.Date}</td>
                <td>Rs.${r.Open}</td>
                <td>Rs.${r.High}</td>
                <td>Rs.${r.Low}</td>
                <td>Rs.${r.Close}</td>
                <td><span class="badge badge-blue">${fmtVol(r.Volume)}</span></td>
            </tr>`).join("");
    }
}

async function loadRecent() {
    const rows = await fetchJSON("/api/tcs/recent30");
    if (!rows) return;

    document.getElementById("recent-table-body").innerHTML = rows.map(r => {
        const ret = parseFloat(r.Daily_Return);
        const retBadge = isNaN(ret)
            ? '<span class="badge badge-silver">--</span>'
            : ret >= 0
                ? '<span class="badge badge-green">+' + ret.toFixed(2) + '%</span>'
                : '<span class="badge badge-red">'   + ret.toFixed(2) + '%</span>';
        return `<tr>
            <td>${r.Date}</td>
            <td>Rs.${r.Open}</td>
            <td>Rs.${r.High}</td>
            <td>Rs.${r.Low}</td>
            <td>Rs.${r.Close}</td>
            <td>${fmtVol(r.Volume)}</td>
            <td>Rs.${r.MA7}</td>
            <td>Rs.${r.MA30}</td>
            <td>${retBadge}</td>
        </tr>`;
    }).join("");
}

async function loadML() {
    const results = await fetchJSON("/api/tcs/ml_results");
    if (!results || results.error) {
        document.getElementById("ml-table-body").innerHTML =
            '<tr><td colspan="5" style="color:#ff1744;padding:20px;">Run forecast_model.py first</td></tr>';
        return;
    }

    const best = results.reduce((a, b) => a.R2 > b.R2 ? a : b);
    document.getElementById("ml-table-body").innerHTML = results.map(r => {
        const isBest  = r.Model === best.Model;
        const rating  = r.R2 >= 0.99 ? "Excellent" : r.R2 >= 0.95 ? "Good" : r.R2 >= 0.90 ? "Fair" : "Poor";
        const rCls    = r.R2 >= 0.99 ? "badge-green" : r.R2 >= 0.95 ? "badge-blue" : "badge-silver";
        return `<tr>
            <td>${isBest ? '<span class="badge badge-gold">' + r.Model + ' - BEST</span>' : r.Model}</td>
            <td>${r.RMSE}</td>
            <td>${r.MAE}</td>
            <td><b>${r.R2}</b></td>
            <td><span class="badge ${rCls}">${rating}</span></td>
        </tr>`;
    }).join("");
}

async function loadPredictions() {
    const preds = await fetchJSON("/api/tcs/predictions");
    if (!preds || preds.error) {
        document.getElementById("pred-table-body").innerHTML =
            '<tr><td colspan="5" style="color:#ff1744;padding:20px;">Run forecast_model.py first</td></tr>';
        return;
    }

    const rows = preds.dates.map((d, i) => `
        <tr>
            <td>${d}</td>
            <td>Rs.${preds.actual[i]}</td>
            <td>Rs.${preds.pred_lr[i]}</td>
            <td>Rs.${preds.pred_rf[i]}</td>
            <td>Rs.${preds.pred_xgb[i]}</td>
        </tr>`).join("");
    document.getElementById("pred-table-body").innerHTML = rows;
}

document.addEventListener("DOMContentLoaded", () => {
    loaded["overview"] = true;
    loadOverview();
});