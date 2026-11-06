# Notes

## Synthetic data, on purpose

Real shop order data isn't mine to publish — it belongs to the shops and
their customers. So the dataset here is synthetic and seeded: anyone can
regenerate the exact same numbers and check every finding in the report.
If a finding only works on one lucky random draw, it isn't a finding.

## Why Streamlit

Streamlit because it's fast to build and, more importantly, a shop owner
can actually open it. A dashboard nobody opens is a screenshot. The same
reasoning is in BI_SPEC-style projects I do now — the tool matters less
than whether the person who needs the number will use it.

## No hidden steps

The dashboard reads the same CSV the analysis writes. Generate, analyse,
open — three commands, and the Quickstart in the README is the whole
pipeline. If it isn't reproducible from the README, it doesn't count.
