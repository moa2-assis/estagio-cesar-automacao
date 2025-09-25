import pytest
import pytest_html
from selenium import webdriver
import json
from pathlib import Path
import time
import os, pytest_html
from datetime import datetime
import sys
import subprocess
import webbrowser
from allure_commons.types import AttachmentType
from selenium.common.exceptions import WebDriverException
from html import escape

"""Conftest para executar o setup de testes com Selenium WebDriver."""

ALLURE_RESULTS_DIR = "allure-results"
SCREENSHOTS_DIR = "screenshots"
OUT_HTML = "dashboard.html"

def pytest_addoption(parser):
    """Dá a opção de escolher browser via linha de comando."""
    parser.addoption("--browser", action="store", default="chrome", help="browser to execute tests (chrome or firefox)")

@pytest.fixture
def driver(request):
    """Fixture que define o WebDriver utilizado baseado na linha de comando."""
    browser = request.config.getoption("--browser").lower()
    if browser == "chrome":
        driver_instance = webdriver.Chrome()
    elif browser == "firefox":
        driver_instance = webdriver.Firefox()
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")
    
    driver_instance.maximize_window()
    yield driver_instance
    driver_instance.quit()

LOG_FILE = Path("test_durations.log")

@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """Hook para ver tempo de início de cada teste."""
    item.start_time = time.time()
    item.start_str = time.strftime("%H:%M:%S", time.localtime())
    msg = f"\n[START] Test '{item.nodeid}' - {item.start_str}"
    print(msg)
    
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

@pytest.hookimpl(trylast=True)
def pytest_runtest_teardown(item):
    """Hook para ver o tempo de término de cada teste."""
    duration = time.time() - item.start_time
    msg = f"[END] Test '{item.nodeid}' finished in {duration:.2f} seconds."
    print(msg)

    # salva em arquivo
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(msg + "\n")

def _collect_attachments(result: dict):
    """Coleta attachments no próprio teste e recursivamente nos steps (Allure)."""
    items = []
    def walk(node: dict):
        for att in (node.get("attachments") or []):
            items.append({
                "src": att.get("source"),
                "name": att.get("name") or (att.get("source") or ""),
                "type": (att.get("type") or "").lower(),
            })
        for step in (node.get("steps") or []):
            walk(step)
    walk(result)
    return items

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())

def _find_local_screenshots(test_name: str):
    """Fallback: procura imagens na pasta screenshots/ que 'batam' com o nome do teste."""
    hits = []
    if not os.path.isdir(SCREENSHOTS_DIR):
        return hits
    want = _norm(test_name)
    for fn in os.listdir(SCREENSHOTS_DIR):
        if not fn.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
            continue
        if want and _norm(fn).find(want) != -1:
            path = os.path.join(SCREENSHOTS_DIR, fn)
            try:
                mtime = os.path.getmtime(path)
            except OSError:
                mtime = 0
            hits.append((mtime, path))
    # mais recentes primeiro
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

    # ordena: mais recentes no topo
    results.sort(key=lambda r: (r.get("stop") or r.get("start") or 0), reverse=True)

    html = """
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
            .attachments { margin-top: 6px; display: flex; flex-wrap: wrap; gap: 8px; }
            .attachments img { max-width: 240px; max-height: 160px; border: 1px solid #ccc; }
            .attachments a { text-decoration: none; }
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

        html += f"""
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

            # 1) Tenta attachments do Allure
            att_parts = []
            for att in _collect_attachments(r):
                src = att.get("src")
                if not src:
                    continue
                href = f"{ALLURE_RESULTS_DIR}/{src}"
                a_type = (att.get("type") or "").lower()
                is_img = a_type.startswith("image/") or src.lower().endswith((".png", ".jpg", ".jpeg", ".gif", ".webp"))
                if is_img:
                    att_parts.append(f'<a href="{escape(href)}" target="_blank"><img src="{escape(href)}" alt="{escape(att.get("name",""))}"></a>')
                else:
                    label = att.get("name") or os.path.basename(src)
                    att_parts.append(f'<a href="{escape(href)}" target="_blank">{escape(label)}</a>')

            # 2) Fallback: se não teve attachment no Allure, busca na pasta screenshots/
            if not att_parts:
                for path in _find_local_screenshots(name):
                    href = path.replace("\\", "/")  # compat Windows
                    att_parts.append(f'<a href="{escape(href)}" target="_blank"><img src="{escape(href)}" alt="screenshot"></a>')

            attachments_html = f'<div class="attachments">{"".join(att_parts)}</div>' if att_parts else ""

            trace_html = f"<details><summary>Stack trace</summary><pre class='error-msg'>{escape(trace)}</pre></details>" if trace else ""

            html += f"""
            <tr class="error-row">
                <td colspan="5">
                    <div class="error-msg"><strong>Erro:</strong> {escape(main_msg)}</div>
                    {attachments_html}
                    {trace_html}
                </td>
            </tr>
            """

    html += """
        </table>
    </body>
    </html>
    """

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Dashboard generated: {OUT_HTML}")

if __name__ == "__main__":
    generate_dashboard()

def pytest_sessionfinish(session, exitstatus):
    """Gerar e abrir dashboard.html após os testes."""
    root = Path.cwd()
    script = root / "dashboard.py"
    html   = root / "dashboard.html"

    try:
        subprocess.run([sys.executable, str(script)], check=True)
    except Exception as e:
        print(f"[dashboard] erro ao executar {script.name}: {e}")
        return

    try:
        webbrowser.open(html.resolve().as_uri())
    except Exception as e:
        print(f"[dashboard] gerado em: {html.resolve()} (abra manualmente). Motivo: {e}")