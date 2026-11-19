# Reflection

## 1. Which issues were the easiest to fix and which were the hardest?

The formatting issues from Flake8 were the easiest: adding blank lines and wrapping two long lines took a few minutes and could not change how the program behaves. The Bandit findings were also quick to fix because each one pointed at a single line (`chmod 0o777`, MD5, `try/except/pass`). The hardest were the bugs no tool reported. Fixing the seat handling meant deciding what a valid seat is (a whole number from 1 to the show's capacity), where to reject bad input, and how to report the rejection. Removing the `global` statement and the bare `except` also took thought, because it meant changing how the functions report success or failure (they now return `True` or `False`) instead of just deleting a line.

## 2. Did the tools report any false positives?

I did not find a clear false positive in this file, but one finding depends on context. Bandit's weak-hash warning (B324) on MD5 would be a false alarm if the hash were only used as a cache key or checksum. Here the ticket code is something a customer would present, so I treated it as security relevant and switched to SHA-256. The style messages (missing docstrings, naming) are not wrong either, but they are matters of convention rather than bugs, and a team might reasonably configure them differently. The bigger lesson was the opposite problem, false negatives: none of the three tools noticed that seat 25 can be booked in a 20-seat theatre, or that the default seat `"4"` is a string while other seats are numbers.

## 3. How would you integrate static analysis tools into your actual workflow?

I would run Flake8 and Pylint in the editor so problems show up while I type, and add a pre-commit hook so style and obvious bugs are caught before a commit is created. I would also run all three tools in a CI pipeline (for example GitHub Actions) on every pull request and fail the build on Bandit high-severity findings and on a Pylint score below an agreed threshold. The rules would live in a config file in the repository so the whole team gets the same results, with any ignored rule written down together with the reason. Static analysis would sit next to unit tests, not replace them.

## 4. What tangible improvements did you see in the code after applying the fixes?

The program is safer: the bookings file is no longer world-writable, and the ticket code no longer uses MD5. It is more robust: invalid seats and unknown shows are rejected with a logged reason instead of corrupting the seating plan or crashing, and the same seat can no longer be booked twice as `4` and `"4"`. The free-seat count is now correct, because invalid seats no longer use up capacity. It is more readable: every function has a docstring, names follow snake_case, f-strings replace `%` formatting, and files are opened with `with`. Flake8 went from 11 findings to 0, and the module can now be imported without running the demo, which makes it testable.
