import json
import os
from datetime import datetime
from html import escape

ALLURE_RESULTS_DIR = "allure-results"
OUT_HTML = "dashboard.html"

def _collect_attachments(result: dict):
    """Coleta todos os attachments do teste (nível raiz e steps recursivamente)."""
    items = []

    def walk(node: dict):
        for att in (node.get("attachments") or []):
            items.append({
                "src": att.get("source"),
                "name": att.get("name") or (att.get("source") or ""),
                "type": (att.get("type") or "").lower(),  # p.ex. image/png
            })
        for step in (node.get("steps") or []):
            walk(step)

    walk(result)
    return items

def generate_dashboard():
    if not os.path.exists(ALLURE_RESULTS_DIR):
        print("Allure results directory not found. Please run tests with --alluredir=allure-results")
        return

    results = []
    for filename in os.listdir(ALLURE_RESULTS_DIR):
        if filename.endswith("-result.json"):
            path = os.path.join(ALLURE_RESULTS_DIR, filename)
            try:
                with open(path, encoding="utf-8") as f:
                    results.append(json.load(f))
            except json.JSONDecodeError:
                continue

    # Mais recentes no topo (usa stop e cai pra start)
    results.sort(key=lambda r: (r.get("stop") or r.get("start") or 0), reverse=True)

    html_content = """
    <html>
    <head>
        <meta charset="utf-8">
        <title>Test Execution Dashboard</title>
        <style>
            body { font-family: sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; text-align: left; padding: 8px; vertical-align: top; }
            th { background-color: #f2f2f2; }
            .status-passed  { color: #0a0; font-weight: 600; }
            .status-failed  { color: #c00; font-weight: 600; }
            .status-broken  { color: #c60; font-weight: 600; }
            .status-skipped { color: #666; font-weight: 600; }
            .error-row { background: #fff5f5; }
            .error-msg { white-space: pre-wrap; margin: 6px 0; }
            details summary { cursor: pointer; user-select: none; color: #333; }
            .attachments { margin-top: 6px; }
            .attachments img { max-width: 240px; max-height: 160px; margin-right: 8px; border: 1px solid #ccc; }
            .attachments a { margin-right: 10px; }
        </style>
    </head>
    <body>
        <h1>Test Execution Dashboard</h1>
        <table>
            <tr>
                <th>Test Case</th>
                <th>Status</th>
                <th>Duration (s)</th>
                <th>Start Time</th>
                <th>Stop Time</th>
            </tr>
    """

    for r in results:
        name   = r.get('name', '-')
        status = (r.get('status') or 'unknown').lower()
        start  = r.get('start') or 0
        stop   = r.get('stop') or start
        dur_s  = max(0, (stop - start) / 1000)

        start_time = datetime.fromtimestamp(start / 1000).strftime('%Y-%m-%d %H:%M:%S') if start else '-'
        stop_time  = datetime.fromtimestamp(stop  / 1000).strftime('%Y-%m-%d %H:%M:%S') if stop  else '-'

        html_content += f"""
            <tr>
                <td>{escape(name)}</td>
                <td class="status-{escape(status)}">{escape(status)}</td>
                <td>{dur_s:.2f}</td>
                <td>{escape(start_time)}</td>
                <td>{escape(stop_time)}</td>
            </tr>
        """

        if status in {"failed", "broken"}:
            sd = r.get("statusDetails") or {}
            message = sd.get("message") or ""
            trace = sd.get("trace") or ""

            main_msg = message.splitlines()[0] if message else "(sem mensagem de erro)"

            # Coleta attachments (inclusive de steps)
            atts = _collect_attachments(r)
            att_parts = []
            for att in atts:
                src = att.get("src")
                if not src:
                    continue
                href = f"{ALLURE_RESULTS_DIR}/{src}"
                a_type = att.get("type", "")
                is_img = a_type.startswith("image/") or src.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
                if is_img:
                    att_parts.append(f'<a href="{escape(href)}" target="_blank"><img src="{escape(href)}" alt="{escape(att["name"])}"></a>')
                else:
                    att_parts.append(f'<a href="{escape(href)}" target="_blank">{escape(att["name"])}</a>')

            attachments_html = f'<div class="attachments">{"".join(att_parts)}</div>' if att_parts else ""

            trace_html = f"<details><summary>Stack trace</summary><pre class='error-msg'>{escape(trace)}</pre></details>" if trace else ""

            html_content += f"""
            <tr class="error-row">
                <td colspan="5">
                    <div class="error-msg"><strong>Erro:</strong> {escape(main_msg)}</div>
                    {attachments_html}
                    {trace_html}
                </td>
            </tr>
            """

    html_content += """
        </table>
    </body>
    </html>
    """

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Dashboard generated: {OUT_HTML}")

if __name__ == "__main__":
    generate_dashboard()