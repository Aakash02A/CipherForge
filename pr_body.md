## Summary
Implements automated frequency-analysis cracking for the Caesar cipher using Chi-squared ($\chi^2$) goodness-of-fit statistics against standard English letter frequencies, addressing the task in #2.

## Key Changes
- Added `auto_solve_caesar(ciphertext: str) -> list[tuple[int, str, float]]`:
  - Iterates over all 25 possible shifts.
  - Computes letter distribution and evaluates Chi-squared statistic:
    $$\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$$
  - Returns candidate plaintexts ranked by lowest $\chi^2$ error (highest probability).
- Added interactive `frequency_auto_solve_demo()` displaying top 5 predictions with candidate snippets and $\chi^2$ confidence scores.
- Added option `5. Auto-Solve via Chi-Squared Analysis (Auto-Crack)` to `caesar_menu()`.
- Added automated unit test `test_caesar_auto_solve()` in `tests/test_level_01_classical.py` verifying accurate plaintext recovery without knowing the shift.

Resolves task in #2.
