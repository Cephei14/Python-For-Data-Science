# Study Guide — Python for Data Science, Module 0 (Starting)

A practical method for working through this module efficiently, rather than just grinding exercises in order.

---

## 1. Read the whole subject once before touching code

Before opening an editor, skim all 10 exercises end-to-end. This module is cumulative: the rules in **Chapter VII** ("From now on you must follow these additional rules") only kick in starting at Exercise 05, but they apply retroactively to how you *should* be thinking from Exercise 00. Knowing this upfront stops you from writing throwaway script-style code in ex00–04 that you'll have to unlearn later.

Pay special attention to three recurring failure points across the whole module:
- **Exact output matching.** Several exercises test output with `| cat -e`, meaning trailing `$` (end-of-line markers) matter. Sloppy `print()` formatting will fail even if the logic is correct.
- **`AssertionError` as a control-flow requirement**, not just a nice-to-have. From ex04 onward, wrong arg count/type must raise this specific exception with the specific message shown in the subject — not a generic `TypeError` or a silent failure.
- **No global variables, ever.** This is stated explicitly in the general rules and will zero an exercise regardless of whether the output is correct.

---

## 2. Work in three passes per exercise, not one

**Pass 1 — Make it correct.**
Get the exact expected output for the example(s) given. Don't worry about edge cases yet.

**Pass 2 — Make it robust.**
Go back through every edge case implied by the subject: no arguments, wrong number of arguments, wrong type, empty input. Write these into your own `tester.py` (explicitly permitted and encouraged — "these tests do not need to be submitted and will not be graded").

**Pass 3 — Make it compliant.**
Run `flake8` (`norminette`), check every function has a docstring, confirm `main()` + `if __name__ == "__main__":` is present where required, and confirm there are no globals.

Treating these as separate passes — rather than trying to write "perfect" code in one shot — is faster in practice because each pass has a single, checkable goal.

---

## 3. Build a personal `tester.py` per exercise and keep it

The subject gives you tester scripts for several exercises (ex02, ex03, ex08) — extend that habit to every exercise, including the ones that don't provide one. A good tester covers:
- The exact example(s) from the subject
- At least one deliberately invalid input (wrong type, wrong count, empty)
- One boundary case specific to that exercise (e.g. `0` for odd/even in ex04, `NaN` for null-checking in ex03)

These testers aren't graded, but they're what you'll actually use during your own defense and when evaluating a peer — so writing them as you go is more efficient than reconstructing them later under time pressure.

---

## 4. Group the exercises by *skill*, not just by number

The 10 exercises aren't a flat progression — they cluster around distinct skills. Studying them in these clusters (even if you still submit them in order) helps the underlying concept stick rather than the specific syntax:

| Cluster | Exercises | Core skill |
| :--- | :--- | :--- |
| Data structures & types | 00, 02, 03 | Mutating built-ins, `type()`, distinguishing "null-like" values |
| Standard library & CLI args | 01, 04 | `time`/`datetime`, `sys.argv`, input validation |
| String processing | 05, 07 | Character classification, dictionary-based encoding |
| Functional programming | 06 | List comprehensions + `lambda` as a *requirement*, not a style choice |
| Generators & iteration | 08 | `yield`, mimicking third-party library behavior |
| Packaging | 09 | `pyproject.toml`/`setup`, building & installing your own package |

If one cluster feels shaky, it's worth doing a small side-exercise in it before moving to the next numbered exercise — e.g. if list comprehensions in ex06 feel unnatural, write three or four throwaway comprehensions on your own data before starting the exercise itself.

---

## 5. Use the subject's own hints — they're not decorative

The PDF drops direct guidance in the blue "info" boxes that's easy to skim past:
- *"By Odin, by Thor! Use your brain!!! Don't reinvent the wheel, use the language features."* (ex05) — a real hint to use built-in string methods (`str.isupper()`, `str.isdigit()`, etc.) rather than manual character-code comparisons.
- *"You can use `get_terminal_size` to adapt to the size of your terminal."* (ex08) — needed to make `ft_tqdm`'s bar width match the real `tqdm` output.
- *"Running your function alone does nothing"* (ex02, ex03) — a reminder that a module built to be imported shouldn't execute logic on import, which foreshadows the `main()` guard required from ex05 onward.

Treat these as spec requirements, not flavor text.

---

## 6. Defense prep, not just submission

Since evaluation is peer-based and happens on the evaluated group's machine, two things are worth doing *before* your slot, not after submitting:
- Re-run every exercise fresh in a clean shell (`python exXX/file.py ...`) to catch anything that only worked because of local environment state.
- Re-read your own code as if explaining it out loud — the general rules explicitly mention that any uncaught exception invalidates the exercise "even in the event of an error that you were asked to test," so be ready to justify *why* each `try/except` or assertion is where it is.

---

## 7. Suggested order of attack

1. ex00 → ex01 → ex02 → ex03 → ex04 (fundamentals, ungraded structure)
2. Pause: retrofit `main()`/docstrings/flake8 habits before continuing
3. ex05 → ex06 → ex07 (string + functional processing, now under full rules)
4. ex08 (generators — slightly more conceptually distinct, budget extra time)
5. ex09 last (packaging is a different skill entirely — environment/tooling heavy, not algorithmic — and benefits from having a clear head after the rest is done)
