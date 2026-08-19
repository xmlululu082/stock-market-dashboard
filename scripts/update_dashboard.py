from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
html_path = ROOT / "index.html"

today = datetime.utcnow().strftime("%Y-%m-%d")

html = html_path.read_text(encoding="utf-8")

# 这里先做最小更新：更新页面日期。
# 后续可以继续扩展成抓新闻、抓股票数据、更新 JSON 或 HTML。
import re
html = re.sub(
    r"更新日期：\d{4}-\d{2}-\d{2}",
    f"更新日期：{today}",
    html
)

html_path.write_text(html, encoding="utf-8")
print(f"Updated index.html for {today}")
