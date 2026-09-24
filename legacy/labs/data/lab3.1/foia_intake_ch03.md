# FOIA Intake Process — the Chapter 3 example

*Simplified, synthetic training description, condensed from
`data/corpus/foia_processing_guidance.md` for the Lab 3.1 diagram task. Course
labs only.*

Describe this process to your AI assistant and ask it to produce a **Mermaid
flowchart**. Do not paste the Mermaid syntax yourself — the point is to see
whether the assistant can turn prose into a correct diagram.

## The process, in words

A FOIA request arrives at the agency by one of three routes: mail, email, or the
agency's online portal.

The FOIA officer logs the request, assigns it a tracking number, and records the
date of receipt. The officer then sends the requester an acknowledgment letter
containing that tracking number.

Next the officer determines the requester's fee category — commercial,
educational or noncommercial scientific, news media, or "all other." The category
decides whether search, review, and duplication fees apply. Non-commercial
requesters receive the first two hours of search and the first 100 pages of
duplication free.

The officer then identifies which program offices are likely to hold responsive
records and issues a search tasking to each. Program offices conduct a reasonable
search and return records by the internal deadline.

The officer reviews what comes back and applies exemptions. Personally
identifiable information such as a Social Security number is withheld under
Exemption 6 and redacted before release.

Finally the officer issues a determination letter: granted in full, granted in
part, or denied. The letter describes the requester's right to appeal. Released
records go out in the requester's preferred format where practicable.

The statutory clock is 20 business days from receipt, extendable in unusual
circumstances.

## What a good diagram shows

- The three intake routes converging on a single logging step.
- The fee-category decision as a branch, not a straight line.
- The three-way outcome at the determination step (full / partial / denied).
- The redaction step sitting *before* release, not after.
