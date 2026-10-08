# CrowdGen Maven Playwright Automation

Automated image captioning and description workflow for CrowdGen Maven tasks using Playwright and OpenRouter Multimodal Vision AI.

## 1. Setup & Installation

Install dependencies and ensure Google Chrome is installed:

```bash
uv sync
uv run playwright install chromium
```

> **Browser Runtime**: Runs on system **Google Chrome** via `channel="chrome"` for seamless authentication, CloudFront asset hydration, and anti-detection. After clicking "Start" on a task card, an automatic 15-second hydration wait is enforced before image extraction.

## 2. Configuration

Create `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Configure your Vision AI provider in `.env`:

**Option A: Google AI Studio (Recommended - 100% Free)**
Get your free API key at [https://aistudio.google.com/api-keys](https://aistudio.google.com/api-keys):

```ini
GEMINI_API_KEY="AIzaSyYourGoogleAIStudioKey"
GEMINI_MODEL="gemini-3-flash-preview"
```

**Option B: OpenRouter Multi-Key Pool (Unlimited Free Rotation)**
Create or edit `openrouter_keys.txt` and paste your OpenRouter keys (one per line):
```text
sk-or-v1-key1...
sk-or-v1-key2...
sk-or-v1-key3...
```
Whenever a key hits OpenRouter's free tier rate limit or daily quota (HTTP 429), the automation automatically switches to the next available key in `openrouter_keys.txt`. When cooldown expires or quotas reset, keys are automatically recycled.

Configure your CrowdGen accounts and task settings in `instances.py`:

```python
from crowdgen_automation.instances import InstanceConfig

INSTANCES: list[InstanceConfig] = [
    InstanceConfig(
        email="your_email@example.com",
        password="your_password",
        task_url="https://app.crowdgen.com/dashboard",
        headless=False,
        max_tasks=50,
        auto_submit=True,  # Autonomous submission once countdown timer is reached
        target_remaining_sec=170,  # Submits when 2:45 ~ 2:55 (165-175s) remain (~20 tasks/hr)
    ),
]
```

## 3. Run Automation

### Unattended Overnight Mode (Auto-Restart on Any Error)
For running unattended overnight (10–11 hours) with automated recovery from any network, browser, or API crash:

```cmd
.\run_forever.bat
```
*(Or simply run `uv run python main.py`, which now includes an autonomous supervisor loop).*

To stop the runner cleanly at any time, press `Ctrl+C` in the terminal.

### Direct Runner
```bash
uv run python main.py
```

### Running with Your Original Chrome Profile

To keep your open tabs (YouTube, active Maven task) and watch the automation work live in your exact Chrome window:

1. Run the included debug launcher once:
   ```cmd
   .\start_chrome_debug.bat
   ```
2. In the Chrome window that opens, navigate to your Maven task or log in.
3. In another terminal, run:
   ```bash
   uv run python main.py
   ```
   The automation will instantly attach to your active Maven tab, extract the task image, generate captions, fill the form, and validate — without closing your browser!

*(Alternatively, close all Google Chrome windows before running `uv run python main.py` and it will launch your original Chrome profile directly).*

For detailed architectural diagrams and module breakdowns, see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).
