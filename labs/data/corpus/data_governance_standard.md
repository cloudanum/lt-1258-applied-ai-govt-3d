# Data Governance Standard (Training Excerpt)

*Simplified, synthetic training document modeled on public federal data-governance practice. Course labs only.*

## Data Stewardship

Every agency dataset has a named data steward responsible for its quality, documentation, and appropriate use. The steward approves requests to use the data for new purposes, including training or prompting AI systems.

## Data Quality Dimensions

Agency data is assessed against six quality dimensions: completeness, accuracy, consistency, timeliness, validity, and uniqueness. A dataset is considered AI-ready when it meets documented thresholds on each dimension and carries machine-readable metadata.

## Metadata

Each dataset must publish metadata describing its source, collection method, update frequency, field definitions, and known limitations. Metadata is what allows a downstream user — human or AI — to judge whether the data fits a given question.

## Data Minimization

Programs collect only the data needed for their mission and retain it only as long as necessary. Minimizing the personal data an agency holds reduces both privacy risk and the attack surface available to adversaries.

## Open Data

Data that is not sensitive is published as open data on the agency's public catalog and on data.gov, in machine-readable formats with an open license. Open data supports transparency and lets the public and researchers build on government information.

## Access Control

Access to nonpublic data follows least privilege: users receive only the access their role requires. Access to sensitive data is logged and reviewed. AI systems that read agency data operate under the same access controls as the users on whose behalf they act.
