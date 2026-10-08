# Project Origami (Oberon Captioning) — Guidelines & Scenario Reference

This document summarizes the official Client QA requirements, the 20 Scenario Good vs. Bad worked examples, and pre-submit checklists for Project Origami on the Maven platform.

---

## 1. Core Caption Requirements

| Field | Length Requirement | Style & Purpose |
| :--- | :--- | :--- |
| **Detailed Caption** | **Minimum 26 words** (> 25 words hard requirement), max 1,024 characters | 1–3 sentences in present tense. Describes main subject, colors, materials, spatial relationships, background. Never pad with filler. |
| **Short Caption** | **6–25 words** (typically 6–20 words) | Exactly 1 standalone sentence covering only the primary visible subject, action/state, and setting. Must make sense independently. |

*Order of execution*: Always determine the Detailed Caption first, then derive the Short Caption.

---

## 2. Hard Client QA Rules (Batch 01 & Batch 02 Feedback)

1. **Zero Assumptive Language (81% of flags)**:
   * **FORBIDDEN**: `"appears to be"`, `"seems to"`, `"likely"`, `"probably"`, `"possibly"`, `"may/might/could be"`, `"suggesting"`.
   * Only describe what is directly confirmed in the image.
2. **Zero Role / Occupation Guessing**:
   * Do not infer jobs like `"waiter"`, `"security guard"`, `"student"`, `"doctor"`.
   * Describe visible clothing and actions instead (e.g. *"a person in a dark suit carries a tray"*).
3. **No Speed / Timing in Still Images**:
   * Do not use `"slowly"`, `"quickly"`, `"driving"`, `"descending"`.
   * Describe visible static position/orientation (e.g. *"leans into a turn"*, *"sits at an angle"*).
4. **Number Formatting**:
   * **Subject counts**: written in words (*"two dogs"*, *"three sailboats"*, not *"2 dogs"*).
   * **Printed text/numbers**: stay as digits (*"page 39"*, *"$24.99"*, *"1946"*).
5. **Non-English Text**:
   * Transcribe signs, labels, or headings in their **original language and script** — never translate them into English.
6. **No Subjective / Aesthetic Language in Short Captions**:
   * No *"beautiful"*, *"stunning"*, *"scenic"*, *"charming"*, *"peaceful"*.
7. **No Living People Named**:
   * Never name living people or celebrities. Describe their visible appearance or role.
8. **Sensitive Content & PII**:
   * Documents showing names with addresses, phone numbers, government IDs, or financial/medical records must be flagged/rejected.
9. **Leftover Label Text**:
   * Never include `"Detailed Caption:"` or `"Short Caption:"` inside the text inputs.

---

## 3. UI Workflow on Maven

1. **Image Check Question**: Automatically selects `"No (No Issue Identified)"` for standard images.
2. **Detailed Caption Field**: Auto-filled first using `textarea[placeholder*="detailed caption" i]`.
3. **Short Caption Field**: Auto-filled second using `textarea[placeholder*="short caption" i]`.
4. **Validate Captions**: Clicks `"Validate Captions"`. If errors occur, the self-healing retry loop fixes the error via VLM re-prompting.
5. **Camera Angle**: Left blank unless an angle (e.g. low-angle, aerial, close-up) is distinct.
6. **Pacing**: Enforces minimum Average Handling Time (AHT) to safeguard contributor standing.
