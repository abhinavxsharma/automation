# Project Origami (Oberon Captioning) — Guidelines & Reference (Batch 4 Update)

This document incorporates the complete official Client QA requirements, the latest Batch 4 announcements, Client Feedback (Sections 7.12 & 7.13), approved real-project examples, pre-submit checklists, and automation specifications for Project Origami on the Maven platform.

---

## 1. Batch 4 Overview & Payment Rules

* **Batch Status**: **Batch 4 is LIVE**.
* **Caption Format**: No change to format — Short Caption (6–25 words, 1 sentence) and Detailed Caption ($\ge 26$ words, 1–3 sentences).
* **Pay Rate**: **$4.10 / hour**.
* **Expected Productivity**: Approximately **20 captioning tasks per hour** based on a maximum 3-minute AHT per task.
* **3-Minute AHT Rule**:
  * Maximum Average Handling Time is **3 minutes per task** (including both Short and Detailed Captions).
  * If a task is completed in **less than 3 minutes**, payment is based on **actual time**.
  * If a task takes **more than 3 minutes**, payment is **capped at 3 minutes**.
* **Dense Tasks**:
  * Tasks marked as Dense are paid separately at **$0.01 per task** and are **excluded** from the 20 tasks/hour productivity target.
  * For Dense documents: tag as **Dense** and submit accordingly. Leave captions empty.
* **Payment Eligibility**:
  * Captions must **always be written in English**. Captions in foreign languages are ineligible for payment.
  * Blank captions on standard images and refusal captions are ineligible for payment.
  * Tasks marked as "Bad" during QA are excluded from productivity and payment calculations.

---

## 2. Core Caption Requirements

| Field | Length Requirement | Style & Purpose |
| :--- | :--- | :--- |
| **Detailed Caption** | **Minimum 26 words** (> 25 words hard requirement), max 1,024 characters | 1–3 complete sentences in present tense. Describes main subject, physical appearance, colors, materials, spatial arrangements, condition, and background. Never pad with filler. |
| **Short Caption** | **6–25 words** (typically 6–20 words) | Exactly 1 standalone sentence covering only the primary visible subject, action/state, and setting. Must make complete sense independently. Never join two sentences with a period. |

*Order of execution*: Determine Detailed Caption first, then derive Short Caption.

---

## 3. Assumptive Wording & Immediate Rejection Categories

Captions are **immediately rejected** if they contain any of the following:

### 1. Hedging & Speculation (STRICTLY FORBIDDEN)
* **Banned Words/Phrases**:
  * `appears` / `appear` / `appears to be`
  * `likely`, `probably`, `possibly`, `perhaps`, `presumably`, `apparently`
  * `may be`, `might be`, `could be`
  * `seems`, `seemingly`, `suggests`, `suggesting`
  * `resembles`, `resembling`, `looks like`
  * `kind of`, `sort of`, `some type of`, `possible`, `potentially`, `unclear`
* **Rule**: Describe only what is directly confirmed and visible. Use direct verbs: *"is"*, *"sits"*, *"stands"*, *"shows"*, *"runs"*.

### 2. Vague Wording & Dual Guesses
* **Never use "mostly"**: Replace with specific visible details or simply state the confirmed element (*"a mostly white background"* → *"a white background"*).
* **No "X or Y" guesses**: Do not write *"stone or concrete"*, *"a bridge or tunnel"*, or *"a book or magazine"*. Pick the verified object or use a neutral general term (*"a structure"*, *"an object"*).
* **Negative Phrasing**: Write *"no text and no logos"*, **never** *"no text or logos"*.

### 3. Text Clarity ("Illegible" vs. "Faint")
* **CRITICAL RULE**: **NEVER write `"illegible"` or `"unreadable"`!**
* **Always use `"faint"` instead** (e.g., *"faint text"*, *"faint lettering"*, *"faint handwriting"*).

### 4. Subjective & Opinion Words
* **Banned**: `ornate`, `beautiful`, `elegant`, `striking`, `decorative`, `intricate`, `peaceful`, `charming`, `adorable`, `picturesque`, `vibrant`, `playful`, `enjoying`, `beaming`, `wonderful`, `delicate`, `rustic`.
* Describe the physical attributes that made you think it (e.g. *"curved metal filigree"* instead of *"ornate"*).

### 5. Guesses About Age or Roles
* **Age**: Never use `"ancient"` or `"antique"` without an explicit printed date in the image.
* **Roles / Occupations**: Never guess unconfirmed jobs (*"soldier"*, *"student"*, *"waiter"*, *"doctor"*, *"security guard"*). Describe visible clothing and actions (*"a person wearing a dark uniform"*, *"a person holding a tray"*).

### 6. Motion in Still Images
* Never describe dynamic motion in still photography: `walking`, `flowing`, `swirling`, `slowly`, `quickly`, `driving`, `running`.
* Describe static position or posture (*"stands with one leg forward"*, *"water cascades over rocks"*, *"sits stationary"*).

---

## 4. Client Rules (Sections 7.12 & 7.13)

### 1. Reject Images of Unusable Quality
* If an image is so blurry, dark, washed out, cropped, or damaged that you **cannot tell what the main subject is**, reject it.
* Flag with **Image Check** and leave **both captions empty**.
* Never write a caption describing poor quality (*"a dark blurry image"*).
* If the main subject is discernible, caption what you can see and omit quality remarks.

### 2. Printed Numbers vs. Counts
* **Counts of things** in the scene are spelled as words (*"two dogs"*, *"three chairs"*).
* **Printed numbers**: Dates, years, page numbers, prices stay as **digits**, exactly as printed (*"June 18, 2011"*, *"page 39"*, *"$24.99"*, *"1946"*).

### 3. Start Directly with Main Subject
* Never open with *"A photograph of"*, *"An image of"*, or *"This image shows"*.
* Begin immediately with the subject, its physical description, and position.

### 4. Detailed Caption Must Match Short Caption
* Every fact, count, color, date, and subject in the Short Caption must be included in the Detailed Caption with identical phrasing.
* Detailed Caption then adds more visible details (materials, spatial layout, condition).

### 5. Natural Sentences & Article Agreement
* Short Caption is exactly 1 sentence. No fragments, no lists of loose nouns.
* No leftover label text (`"Short Caption:"`, `"Detailed Caption:"`).
* Proper article agreement (*"a wooden box"*, not *"an wooden box"*; *"an apple"*, not *"a apple"*).

---

## 5. Approved Real-Project Benchmarks (Section 9)

* **Multi-Subject Group**:
  * *Short*: *A group of dogs, cats, guinea pigs, and a rabbit pose on a white background as several dogs jump.*
  * *Detailed*: *A large group of about twenty pets gathered closely together for a photo against a plain white background. Taller dogs stand at the back and sides while smaller dogs are at the front. A small kitten sits on top of a white dog's head, and a rabbit is visible near the middle of the group.*
* **Grid Items**:
  * *Short*: *Twelve square waffles in three by four rows on a textured beige background.*
  * *Detailed*: *Twelve square waffles are arranged in four vertical columns and three horizontal rows on a light beige textured surface. Each waffle is golden brown with a deep grid of small square pockets and slightly darker edges.*
* **Motion / Biking**:
  * *Short*: *A bearded man wearing athletic outfit standing on a hill, balancing a black mountain bike on its rear wheel near the hill's peak.*
  * *Detailed*: *A side view of a bearded man in dark cycling clothes stands on the crest of a dirt hill beneath a pale, cloudy sky. He holds a black mountain bike upright, balancing it on its rear wheel while the front wheel points upward.*
* **Dense Text Document**:
  * Tag as `Dense Text Document`. Captions left empty.

---

## 6. Pre-Submit Verification Checklist (Section 10)

Before submitting each task:
1. **Language**: Captions written strictly in English.
2. **Quality Check**: Clear subject. If unusable quality, flagged with Image Check and captions left empty.
3. **Dense Tag**: Dense documents tagged as Dense; captions left empty.
4. **Subject First**: No *"A photograph of"* or *"An image of"*.
5. **Zero Hedging**: No *"appears"*, *"seems"*, *"likely"*, *"possibly"*, *"suggests"*, *"looks like"*.
6. **No "Mostly" or "X or Y"**: Pure factual description.
7. **No "Illegible"**: Described as *"faint"* if low contrast or hard to read.
8. **No Job / Age Guesses**: Visible attire described; no *"ancient"*/*"antique"*.
9. **No Speed / Motion Words**: Static position described.
10. **Number Rules**: Counts as words (*"two"*), printed dates/pages as digits (*"June 18, 2011"*, *"39"*).
11. **Caption Agreement**: Detailed caption contains all facts from Short caption and adds visual depth.
12. **Length Targets**: Detailed $\ge 26$ words; Short 6–25 words (1 complete sentence).
13. **AHT Compliance**: Task handled within the 3-minute maximum AHT.

---

## 7. Automation Architecture & Flow

* **`vision_solver.py`**:
  * Implements Batch 4 `SYSTEM_PROMPT` containing all hedging, opinion, motion, age, and text clarity bans.
  * Programmatic `_sanitize` rewrites `"illegible"`/`"unreadable"` to `"faint"`, strips `"mostly"`, removes banned adjectives, and ensures correct "a/an" article grammar.
  * Flags `is_dense: true` or `unusable_quality: true` to prevent invalid caption generation.
* **`filler.py`**:
  * Detects `is_dense` and clicks the Dense radio button/tag while leaving textareas blank.
  * Detects `unusable_quality` and clicks the Image Check issue radio while leaving textareas blank.
  * Otherwise, selects No Issue, fills Detailed Caption first, Short Caption second, and camera angle third.
* **`coordinator.py`**:
  * Immediately submits flagged Dense or Unusable Quality tasks without waiting for validation errors.
* **`submit.py`**:
  * Manages task pacing to safeguard AHT within the 3-minute cap while maximizing actual credited time.
