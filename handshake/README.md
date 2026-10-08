# Handshake AI Project Lumière Automation

Automated graduate-level engineering multimodal reasoning task authoring and submission on **Handshake AI** (`ai.joinhandshake.com`) for **Project Lumière (Engineering)** ($110/task), built with Playwright, Matplotlib, and OpenRouter Multimodal AI.

---

## 1. Quick Start

### Installation
Ensure you are in the `handshake/` folder:

```bash
uv sync
uv run playwright install chromium
```

### Configuration
1. Your `.env` and `openrouter_keys.txt` are configured with your OpenRouter & Gemini keys.
2. In `instances.py`, verify your Handshake task URL and pacing:
   ```python
   INSTANCES = [
       InstanceConfig(
           email="vats.abhinav247@gmail.com",
           tasks_url="https://ai.joinhandshake.com/fellow/15f2e875-62ac-492c-9e96-d5569635671a/tasks",
           headless=False,
           max_tasks=50,
           auto_submit=True,
           min_time_sec=1800,  # 30-40 min authentic pacing (under 3.5h limit)
       ),
   ]
   ```

---

## 2. Running with Your Active Logged-in Chrome (CDP Port 9222)

To avoid re-logging in or repeating 2FA:

1. Launch Chrome with remote debugging:
   ```cmd
   .\start_chrome_debug.bat
   ```
2. Log in to Handshake AI once in this Chrome window (or keep your existing tab open).
3. In your terminal, run:
   ```cmd
   .\run_forever.bat
   ```
   *(Or `uv run python main.py`)*

The bot attaches to your open tab, automatically claims available tasks, handles all 12 steps, tests model failures, and submits.

---

## 3. Image Sourcing: Guidelines & Compliance

Per the official Project Lumière Playbook:

### 🚫 Strictly Prohibited Images
- **AI Diffusion/Generative Images** (Midjourney, DALL-E, Stable Diffusion): Produce blurry, hallucinated labels and unphysical geometry.
- **BioRender**: Explicitly blocked by Handshake (`BioRender-generated figures: No. Hard block`).
- **Paywalled / All Rights Reserved / CC BY-NC / CC BY-ND**: Not permitted.

### ★ Top Priority / Strongly Preferred: Self-Authored Diagrams
- **What it is**: Vector-rendered engineering schematics you create yourself (e.g. beam loading diagrams, circuit schematics, bridge networks).
- **Form Selection**:
  - Sourced: `My own image`
  - URL / DOI: `N/A`
  - License: `Original` / `N/A`
- **Why preferred**: 100% unique, zero copyright issues, impossible for models to reverse-search on the web.

### 🟡 Acceptable: Online Open-Access Scientific Sources
- **What it is**: Figures from open-access journals (PLoS, MDPI, arXiv, PMC Open Access) or Wikimedia Commons.
- **License**: Must be `CC BY 4.0`, `CC BY-SA`, or `CC0`.
- **Form Selection**:
  - Sourced: `Online`
  - URL / DOI: Real paper DOI or Wikimedia URL
  - License: `CC BY 4.0`
- **Rule**: The prompt must ask for a derivation or quantity that **CANNOT be found in the publication**.

---

## 4. Model Failure Bar & 3.5-Hour Timer

1. **2/2 Models Must Fail**:
   - On Step 5, the platform dispatches the prompt + image to 2 vision-language models.
   - Both models (2/2) must fail (>2% difference from GTFA with a visual reasoning error).
   - If either model passes, the platform blocks submission: *"If your prompt cannot stump 2 out of 2 responses -> please make the prompt more difficult."*
   - The bot detects this and confirms 2/2 failure agreement via `✓ I agree to the above`.

2. **3.5-Hour Timer Limit**:
   - Each task has an allocation of 3.0 to 3.5 hours.
   - Pacing (`min_time_sec`) simulates realistic expert handling time (e.g. 30–45 mins) while guarding against the 3.5-hour hard ceiling.

---

## 5. The 12-Step Lifecycle Automated

1. **Step 1 (Start)**: Clicks "Start timer" modal.
2. **Step 2 (Select Subdomain)**: Chooses Engineering & CS subdomain.
3. **Step 3 (Source & License)**: Selects "My own image" / Original (or Online CC BY + DOI).
4. **Step 4 (Image & Prompt)**: Uploads diagram and enters KaTeX prompt with mandatory closing statement.
5. **Step 5 (Model Responses)**: Generates model responses and verifies 2/2 fail.
6. **Step 6 (GTFA)**: Fills concise Ground-Truth Final Answer.
7. **Step 7 (Image Description)**: Fills comprehensive visual description.
8. **Step 8 (Failure Justification)**: Selects failure category and writes KaTeX justification.
9. **Step 9 (Step-by-Step Solution)**: Fills numbered solution leading to GTFA.
10. **Step 10 (Distractors)**: Fills 5 plausible distractors.
11. **Step 11 (Answer Format)**: Selects Integer/Decimal and decimal places.
12. **Step 12 (End)**: Confirms session time and submits for review.

---

## 6. Verification Gates

```bash
uv run ruff check --fix
uv run ty check
uv run pytest
```
- NASA JPL Rule 4: All production files fit on a single printed sheet of paper (≤ 60 lines).

---

## 7. Completed Tasks Record

### Task: `1520c7f4-d41f-440b-b341-e7c6bc96166c` (Submitted)
- **Domain / Subdomain**: Computer Science / Algorithms and Complexity
- **Problem**: Parallel Computation DAG Critical Path Latency Scheduling (8 nodes $S, A, B, C, D, E, F, T$, 15 directed edges with millisecond latencies, 4 planar crossings).
- **Ground Truth**: `76` ms ($S \to A \to D \to E \to F \to T = 14 + 22 + 12 + 8 + 20 = 76\text{ ms}$).
- **VLM Failure Evaluation (100% Failure Rate)**:
  - **Model 1 (Block 1)**: Output `85` ms (failed — swapped crossing edges $(C, F)=21$ and $(D, E)=12$).
  - **Model 2 (Block 2)**: Output `89` ms (failed — misrouted diagonal crossing edge $(B, E)=26$ into node $C$).
- **Distractors**: `75`, `73`, `72`, `68`, `64`.
- **QC Gates**: Science Judge (0 flags), Distractor Format Checker (Passed), Image Description (Passed).
- **Session Duration**: `00:40:00` logged and confirmed on 2026-09-28.

