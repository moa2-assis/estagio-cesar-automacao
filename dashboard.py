# dashboard.py
import json
import os
import re
from pathlib import Path
from datetime import datetime
from html import escape

ALLURE_RESULTS_DIR = "allure-results"
OUT_HTML = "dashboard.html"
SCREENSHOTS_DIR = Path("screenshots")  # fallback opcional para imagens locais

# Opcional: mapeie prefixos de paths do trace -> paths locais (se o trace vier de outro dir/CI)
# Ex.: PATH_MAP = [("/__w/repo", "/Users/you/projeto-automacao")]
PATH_MAP = []

def _apply_path_map(path: str) -> str:
    p = str(path)
    for src, dst in PATH_MAP:
        if p.startswith(src):
            return p.replace(src, dst, 1)
    return p

def _collect_attachments(result: dict):
    """Coleta todos os attachments do teste (nível raiz e steps recursivamente)."""
    items = []
    def walk(node: dict):
        for att in (node.get("attachments") or []):
            items.append({
                "src": att.get("source"),  # arquivo em allure-results
                "name": att.get("name") or (att.get("source") or ""),
                "type": (att.get("type") or "").lower(),
            })
        for step in (node.get("steps") or []):
            walk(step)
    walk(result)
    return items

# Reconhece dois formatos comuns no trace
_RX_PYTEST = re.compile(r'(^|\n)(?P<file>[^:\n]+\.py):(?P<line>\d+):', re.MULTILINE)
_RX_PYTHON = re.compile(r'File "?(?P<file>.+?\.py)"?, line (?P<line>\d+)', re.MULTILINE)

def _parse_error_location(text: str):
    if not text:
        return None, None
    m = _RX_PYTEST.search(text)
    if m:
        return _apply_path_map(m.group("file")), int(m.group("line"))
    m = _RX_PYTHON.search(text)
    if m:
        return _apply_path_map(m.group("file")), int(m.group("line"))
    return None, None

def _read_code_snippet(filepath: str, lineno: int, context: int = 3):
    """Retorna (title, html_pre) com linhas ao redor. Se não achar arquivo, ('','')."""
    if not filepath or lineno is None:
        return "", ""
    fp = _apply_path_map(filepath)
    if not os.path.exists(fp):
        return "", ""
    try:
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception:
        return "", ""
    start = max(1, lineno - context)
    end = min(len(lines), lineno + context)
    rows = []
    for i in range(start, end + 1):
        line_txt = lines[i-1].rstrip("\n")
        ln = f"{i:>5}"
        if i == lineno:
            rows.append(
                f"<span style='background:#fff2cc;border-left:4px solid #e0a800;padding-left:6px;'>"
                f"{ln} │ {escape(line_txt)}</span>"
            )
        else:
            rows.append(f"{ln} │ {escape(line_txt)}")
    title = f"{os.path.basename(fp)}:{lineno}"
    html_pre = "<pre style='margin:8px 0; padding:8px; background:#f7f7f7; border:1px solid #eee; overflow:auto'>" \
               + "\n".join(rows) + "</pre>"
    return title, html_pre

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

def _find_local_screenshots(test_name: str):
    """Fallback: procura imagens em screenshots/ que contenham o nome do teste."""
    if not SCREENSHOTS_DIR.exists():
        return []
    want = _norm(test_name)
    hits = []
    for fn in SCREENSHOTS_DIR.iterdir():
        if fn.suffix.lower() not in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            continue
        if want and _norm(fn.name).find(want) != -1:
            try:
                mtime = fn.stat().st_mtime
            except OSError:
                mtime = 0
            hits.append((mtime, fn))
    hits.sort(reverse=True)
    return [p for _, p in hits]

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

    html = [
        "<html><head><meta charset='utf-8'><title>Test Execution Dashboard</title>",
        "<style>",
        "body{font-family:sans-serif;margin:20px}",
        "table{border-collapse:collapse;width:100%}",
        "th,td{border:1px solid #ddd;text-align:left;padding:8px;vertical-align:top}",
        "th{background:#f2f2f2}",
        ".status-passed{color:#0a0;font-weight:600}.status-failed{color:#c00;font-weight:600}.status-broken{color:#c60;font-weight:600}.status-skipped{color:#666;font-weight:600}",
        ".error-row{background:#fff5f5}",
        ".error-msg{white-space:pre-wrap;margin:6px 0}",
        "details summary{cursor:pointer;user-select:none;color:#333}",
        ".attachments{margin-top:6px;display:flex;flex-wrap:wrap;gap:8px}",
        ".attachments img{max-width:240px;max-height:160px;border:1px solid #ccc}",
        ".loc{font-family:monospace;background:#eef;padding:2px 6px;border-radius:6px}",
        "</style></head><body>",
        "<h1>Test Execution Dashboard</h1>",
        "<table>",
        "<tr><th>Test Case</th><th>Status</th><th>Duration (s)</th><th>Start Time</th><th>Stop Time</th><th>Failed in</th></tr>",
    ]

    for r in results:
        name   = r.get('name', '-')
        status = (r.get('status') or 'unknown').lower()
        start  = r.get('start') or 0
        stop   = r.get('stop') or start
        dur_s  = max(0, (stop - start) / 1000)
        start_time = datetime.fromtimestamp(start / 1000).strftime('%Y-%m-%d %H:%M:%S') if start else '-'
        stop_time  = datetime.fromtimestamp(stop  / 1000).strftime('%Y-%m-%d %H:%M:%S') if stop  else '-'

        # Erro principal + trace
        sd = r.get("statusDetails") or {}
        message = sd.get("message") or ""
        trace = sd.get("trace") or ""
        main_msg = message.splitlines()[0] if message else "(sem mensagem de erro)"

        # arquivo:linha (se falhou)
        file_path, line_no = (None, None)
        loc_html = "—"
        if status in {"failed", "broken"}:
            file_path, line_no = _parse_error_location(trace or message)
            if file_path and line_no:
                loc_html = f"<span class='loc'>{escape(os.path.basename(file_path))}:{line_no}</span>"

        html.append(
            f"<tr>"
            f"<td>{escape(name)}</td>"
            f"<td class='status-{escape(status)}'>{escape(status)}</td>"
            f"<td>{dur_s:.2f}</td>"
            f"<td>{escape(start_time)}</td>"
            f"<td>{escape(stop_time)}</td>"
            f"<td>{loc_html}</td>"
            f"</tr>"
        )

        if status in {"failed", "broken"}:
            # Snippet de código, se arquivo existir localmente
            snippet_title, snippet_pre = ("", "")
            if file_path and line_no:
                snippet_title, snippet_pre = _read_code_snippet(file_path, line_no, context=3)

            # Attachments do Allure
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
                    att_parts.append(
                        f'<a href="{escape(href)}" target="_blank"><img src="{escape(href)}" alt="{escape(att["name"])}"></a>'
                    )
                else:
                    att_parts.append(f'<a href="{escape(href)}" target="_blank">{escape(att["name"])}</a>')

            # Fallback: screenshots locais que combinem com o nome do teste
            if not att_parts:
                for img in _find_local_screenshots(name):
                    href = img.as_posix()
                    att_parts.append(f'<a href="{escape(href)}" target="_blank"><img src="{escape(href)}" alt="screenshot"></a>')

            attachments_html = f'<div class="attachments">{"".join(att_parts)}</div>' if att_parts else ""
            trace_html = f"<details><summary>Stack trace</summary><pre class='error-msg'>{escape(trace)}</pre></details>" if trace else ""

            block = [
                "<tr class='error-row'><td colspan='6'>",
                f"<div class='error-msg'><strong>Erro:</strong> {escape(main_msg)}</div>",
            ]
            if snippet_pre:
                block.append(f"<div style='margin-top:6px'><strong>Arquivo/linha:</strong> {escape(snippet_title)}</div>")
                block.append(snippet_pre)
            block.append(attachments_html)
            block.append(trace_html)
            block.append("</td></tr>")
            html.append("".join(block))

    html.append("</table></body></html>")

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"Dashboard generated: {OUT_HTML}")

if __name__ == "__main__":
    generate_dashboard()