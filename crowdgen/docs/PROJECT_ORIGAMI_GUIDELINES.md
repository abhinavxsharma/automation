# Project Origami (Oberon Captioning) — Guidelines & Reference

This document incorporates the complete official Client QA requirements, the latest Client Feedback (Sections 7.12 & 7.13), approved real-project examples, pre-submit checklists, and automation specifications for Project Origami on the Maven platform.

---

## 1. Core Caption Requirements

| Field | Length Requirement | Style & Purpose |
| :--- | :--- | :--- |
| **Detailed Caption** | **Minimum 26 words** (> 25 words hard requirement), max 1,024 characters | 1–3 complete sentences in present tense. Describes main subject, physical appearance, colors, materials, spatial arrangements, condition, and background. Never pad with filler. |
| **Short Caption** | **6–25 words** (typically 6–20 words) | Exactly 1 standalone sentence covering only the primary visible subject, action/state, and setting. Must make complete sense independently. Never join two sentences with a period. |

*Order of execution*: Write the Detailed Caption first, then derive the Short Caption.

---

## 2. Latest Client Feedback — What Changed (Section 7.12 & 7.13)

### 1. Reject Images of Unusable Quality — Don't Caption Them
* If an image is so blurry, dark, washed out, cropped, or damaged that you **cannot tell what the main subject is**, it is **unusable quality** and must be rejected.
* **Action**: Flag it with **Image Check** and leave **both captions empty**, so it does not move on to captioning or QA review.
* **Never** write a caption describing the poor quality (e.g. *"a dark blurry image"*) as a workaround.
* If you **can still make out the main subject**, the image is usable: caption what you can see and omit remarks about quality.

### 2. Keep Printed Dates and Page Numbers as Printed — in Short Caption Too
* **Counts of things** in the scene are spelled out as words (*"two dogs"*, *"three chairs"*).
* **Printed numbers**: Dates, years, page numbers, prices, and other numbers printed in the image stay as **digits**, exactly as shown (*"June 18, 2011"*, *"page 39"*, *"$24.99"*, *"1946"*).
* *Example*:
  * ✔ **GOOD**: *A White House worksheet dated June 18, 2011 contains typed questions and handwritten answers.*
  * ✘ **NOT LIKE THIS**: *A White House worksheet dated June eighteen, two thousand eleven contains typed questions and handwritten answers.*

### 3. Stay Neutral — No Unsupported Interpretations
* Ground captions strictly in visible details. Do not add assumptions, speculation, or emotional states (*"playful"*, *"enjoying"*, *"beaming"*).
* If something is unclear, describe its visible features in general terms (shape, color, size, position, material) rather than guessing what or who it is.
* *Example*:
  * ✔ **GOOD**: *A carved stone figure with a rounded head and four short legs lies on a flat base.*
  * ✘ **NOT LIKE THIS**: *A reclining lion or guardian beast carved in stone.* (guesses animal type and uses "or").

### 4. Start with the Main Subject — Leave Out "A photograph of" and "An image of"
* Opening phrases such as *"A photograph of"*, *"An image of"*, or *"This image shows"* waste word counts and add zero value.
* Begin directly with the subject, then describe its appearance and spatial arrangement.
* *Example*:
  * ✔ **GOOD**: *Two flowers with long green stems stand in two small clay flowerpots set side by side.*
  * ✘ **NOT LIKE THIS**: *An image of two flowers and two flowerpots.*

### 5. Detailed Caption Must Match the Short Caption — and Add to It
* Both captions describe the same image. Anything important in the Short Caption (main subject, color, count, quoted text, date) **must also be present** in the Detailed Caption with identical facts.
* The Detailed Caption then adds more visible detail (position, background, material, condition).
* Never introduce conflicting subjects, numbers, or dates between the two captions.

### 6. Never Use the Word "Mostly"
* *"Mostly"* is vague and obscures what is actually visible. Name the exact parts that are blank, covered, or different:
  * *"a mostly white background"* → *"a white background"*
  * *"a mostly clear sky"* → *"a blue sky with a few thin clouds"* (only if clouds are visible)
  * *"mostly red apples"* → *"red apples with yellow streaks"*

### 7. Never Use "X or Y" to Cover Two Guesses
* Phrasing like *"a book or magazine"*, *"stone or concrete"*, or *"a bridge or tunnel"* indicates uncertainty. Pick only what is visually confirmed, or use a neutral general term (*"a structure"*, *"an object"*).
* Apply this to negative phrasing too: write *"no text and no logos"*, **not** *"no text or logos"*.
* Direct transcriptions of signs with "or" (e.g. a sign reading *"OPEN OR CLOSED"*) are permitted.

### 8. Avoid "Appears" as a Filler Verb and Soft Words
* **Forbidden**: *"appears to be"*, *"appears"*, *"appear"*, *"kind of"*, *"sort of"*, *"some type of"*, *"possible"*, *"potentially"*, *"resembling"*, *"seems"*, *"likely"*, *"probably"*, *"suggesting"*.
* Use direct verbs specifying state or location: *"is"*, *"sits"*, *"stands"*, *"shows"*, *"runs"*.
  * *"The edges appear worn"* → *"The edges are worn."*
  * *"A caption line appears below the photo"* → *"A caption line sits below the photo."*
  * *"A lamp resembling a flower"* → *"A lamp with petal-shaped panels."*

### 9. Write Real, Complete Sentences
* Short Caption is exactly 1 sentence. Do not combine sentences with a period, and do not provide a list of nouns (*"A ferris wheel water building boats and lights"* is rejected).
* No truncated or cut-off sentences.
* Never prefix captions with labels like `"Short Caption:"` or `"Detailed Caption:"`.
* Always write in the **present tense** (*"a woman holds"*, *"a sign reads"*).
* No repetitive phrases (*"alphabetized alphabetical sections"*, *"toward out toward"*).

---

## 3. Good vs. Not-So-Good Worked Examples (Section 8)

* **Spatial arrangement vs. list of nouns**:
  * ✔ **GOOD**: *A big Ferris wheel, the tallest object in the scene, stands on the left side of the river, with a boat on the water in front of it.*
  * ✘ **NOT LIKE THIS**: *A ferris wheel water building boats and lights.*
* **Objective observation vs. emotional guessing**:
  * ✔ **GOOD**: *A toddler boy and a light-colored golden retriever sitting together on a tennis court. The boy is smiling at the camera, and the dog's tongue is out with its head turned toward him.*
  * ✘ **NOT LIKE THIS**: *A candid snap photo of a picturesque scene featuring a toddler boy and an adorable golden retriever sitting side by side, beaming widely, enjoying a playful moment together...*

---

## 4. Approved Real-Project Benchmarks (Section 9)

### Example 1: Multi-Subject Group
* **Short Caption**: *A group of dogs, cats, guinea pigs, and a rabbit pose on a white background as several dogs jump.*
* **Detailed Caption**: *A large group of about twenty pets gathered closely together for a photo against a plain white background. Taller dogs stand at the back and sides while smaller dogs are at the front. A small kitten sits on top of a white dog's head, and a rabbit is visible near the middle of the group.*

### Example 2: Repetitive Grid Items
* **Short Caption**: *Twelve square waffles in three by four rows on a textured beige background.*
* **Detailed Caption**: *Twelve square waffles are arranged in four vertical columns and three horizontal rows on a light beige textured surface. Each waffle is golden brown with a deep grid of small square pockets and slightly darker edges.*

### Example 3: Figure & Motion in Still Image
* **Short Caption**: *A bearded man wearing athletic outfit standing on a hill, balancing a black mountain bike on its rear wheel near the hill's peak.*
* **Detailed Caption**: *A side view of a bearded man in dark cycling clothes stands on the crest of a dirt hill beneath a pale, cloudy sky. He holds a black mountain bike upright, balancing it on its rear wheel while the front wheel points upward.*

### Example 4: Landscape & Setting
* **Short Caption**: *A hillside town with colorful houses, green trees, and blooming flowers under a clear sky.*
* **Detailed Caption**: *A hillside town of tightly packed multicolored buildings rises across the background beneath a partly cloudy blue sky. Green trees and shrubs break up the buildings on the slope, with pink flowering plants in the foreground.*

### Special Tags & Exemptions
* **Political / Demonstration**:
  * **Short**: *A crowd holds banners at an outdoor demonstration, shown from a distance.*
  * **Detailed**: *Banners in English, German, and Farsi/Dari are held up by a crowd in the rain; the English banner reads "EVACUATE NOW," and the other banners include additional handwritten text.*
  * **Tag**: `Political`
* **Dense Text Document**:
  * Leave captions empty; tag and skip (`Tagged: Dense Text Document`).

---

## 5. Pre-Submit Verification Checklist (Section 10)

Before submitting any task, verify each requirement:
1. **Quality Check**: Image is clear and identifiable. If unusable quality (subject unrecognizable), reject via Image Check and leave captions blank.
2. **Main Subject First**: Neither caption begins with *"A photograph of"* or *"An image of"*.
3. **No Assumptive Language**: Zero occurrences of *"appears to be"*, *"seems"*, *"likely"*, *"possibly"*, *"resembling"*, etc.
4. **No Job Guessing**: Clothes and actions described instead of roles (*"doctor"*, *"waiter"*).
5. **No Speed Words**: Static orientation described without motion assumptions (*"slowly"*, *"driving"*).
6. **Number Conventions**:
   * Counts spelled out (*"two dogs"*, *"three cars"*).
   * Printed dates, years, page numbers kept as digits (*"June 18, 2011"*, *"page 42"*).
7. **Strictly Factual**:
   * No *"mostly"*.
   * No *"X or Y"* guesses.
   * No subjective words (*"beautiful"*, *"peaceful"*, *"picturesque"*, *"adorable"*, *"vibrant"*).
8. **Alignment**: Detailed Caption includes every fact/number/color mentioned in Short Caption and adds visual depth.
9. **Lengths**:
   * Detailed Caption: **$\ge$ 26 words** (> 25 words hard requirement), 1–3 sentences.
   * Short Caption: **6–25 words**, exactly 1 standalone sentence.
10. **Clean Formatting**: No interface label remnants (`"Detailed Caption:"`, `"Short Caption:"`).

---

## 6. Automation Implementation Mapping

* `vision_solver.py`:
  * Enforces prompt rules covering all forbidden words, opening phrase bans, number conventions, and unusable quality detection.
  * Sanitizes captions programmatically (`_sanitize`) to strip forbidden prefixes, subjective adjectives, and filler words.
  * Sets `unusable_quality: true` and clears captions if the image cannot be identified.
* `filler.py`:
  * If `unusable_quality` is detected, flags the Image Check issue radio button and leaves caption textareas empty.
  * For valid images, selects `"No (No Issue Identified)"`, enters Detailed Caption first, Short Caption second, and optional Camera Angle third.
* `coordinator.py`:
  * Directly submits tasks flagged for unusable quality without requiring validation errors.
