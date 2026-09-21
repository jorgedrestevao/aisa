# \# PP KNOWLEDGE MODEL

# 

# The PP pack must not become a documentation dump.

# 

# Knowledge must be structured around decisions.

# 

# \## Primary chain

# 

# ```text

# Requirement

# &#x20;   ↓

# Signal

# &#x20;   ↓

# Evidence

# &#x20;   ↓

# Knowledge State

# &#x20;   ↓

# Decision Criterion

# &#x20;   ↓

# Candidate Options

# &#x20;   ↓

# Trade-offs

# &#x20;   ↓

# Risk

# &#x20;   ↓

# Validation

# ```

# 

# \## Requirement

# 

# A business, operational, user, data or governance characteristic that influences solution design.

# 

# Example:

# 

# Users must work without connectivity.

# 

# \## Signal

# 

# A reusable indicator that should be investigated.

# 

# Example:

# 

# `offline\_operation\_required`

# 

# Signals must be technology-neutral during Discovery.

# 

# \## Evidence

# 

# Information that supports the signal.

# 

# Examples:

# 

# \* interview statement;

# \* process observation;

# \* document;

# \* system analysis;

# \* quantitative measurement.

# 

# \## Knowledge State

# 

# Use aisa's standard states:

# 

# \* Confirmed

# \* Assumed

# \* Unknown

# \* Conflicted

# \* Risky

# 

# The PP pack must never introduce additional epistemic states.

# 

# \## Decision Criterion

# 

# A rule for evaluating solution options.

# 

# Example:

# 

# "The architecture must support the required offline operating model without unacceptable synchronization risk."

# 

# \## Candidate Options

# 

# Possible responses.

# 

# These may include:

# 

# \* process change;

# \* existing capability;

# \* Power Platform;

# \* Azure;

# \* custom application;

# \* SaaS;

# \* other enterprise platform;

# \* do nothing.

# 

# \## Trade-off

# 

# What is gained and what is sacrificed.

# 

# \## Risk

# 

# Potential material consequence of selecting an option.

# 

# \## Validation

# 

# What must be tested or confirmed before commitment.




# \## What a Decision Criterion may not be
# 
# A criterion evaluates the **design**, never the organisation that would run it.
# 
# Admissible: whether the role that acts is defined; which identity the automation runs
# as; whether the detection mechanism exists; whether the recovery procedure is written.
# 
# Not admissible: whether a person was named; whether a sign-off was obtained; a maturity
# grade that activates a package by label.
# 
# Where the design has not defined something, the criterion produces a **requirement with
# a cost**, never an availability verdict. Binding shape: `05-OUTPUT-CONTRACT.md` §1.
