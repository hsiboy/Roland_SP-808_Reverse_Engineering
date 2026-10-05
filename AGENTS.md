## Domain context and informed inference

Domain knowledge is valuable and should be used when interpreting firmware.

The SP-808 is a musical sampler/workstation. Relevant system concepts include, among others:

- samples
- sample banks/pads
- projects and persistent musical data
- audio recording and playback
- MIDI
- removable storage
- the built-in Zip storage subsystem
- optional SCSI functionality
- formatting, mounting, loading and saving media
- front-panel controls
- display/UI behavior
- audio/DSP-related hardware

This context may be used to generate and rank hypotheses about otherwise ambiguous firmware behavior.

However, domain plausibility is **context, not primary evidence**.

For example, a routine that transfers blocks of data from storage and updates an indexed structure may plausibly be involved in sample or bank loading. That is a useful hypothesis, but it is not established until additional evidence connects the routine to those concepts.

### Inference is encouraged

Do not avoid useful conclusions merely because they cannot be proven with absolute certainty.

Reverse engineering necessarily involves inference.

Instead, distinguish levels of knowledge:

**Observed**
Directly established by firmware, disassembly, hardware behavior, or authoritative documentation.

**Inferred**
The evidence strongly suggests a particular semantic interpretation.

**Hypothesized**
A plausible explanation motivated by evidence and domain context, but requiring additional verification.

**Speculative**
Possible, but currently supported mostly by contextual plausibility.

Use domain knowledge especially to generate competing hypotheses and determine what evidence to inspect next.

### Prefer converging evidence

Semantic conclusions become stronger when independent kinds of evidence converge.

For example:

- storage I/O behavior
- nearby UI strings
- callers associated with a user operation
- data structures matching known project/sample organization
- MIDI or panel event paths
- known hardware interfaces
- behavior observed on the physical SP-808

may together establish a meaning that no single instruction could establish alone.

### Context can disambiguate constants and structures

Do not interpret a numeric constant from its value alone.

The same number may represent:

- time
- capacity
- byte/sector count
- sample count
- MIDI-related values
- UI dimensions
- hardware timing
- offsets
- arbitrary thresholds

Determine meaning from how the value is produced and consumed.

For example, the current investigation established that `125000` is used in at least one context as an elapsed-counter threshold. This does not imply that every occurrence of `125000` elsewhere has the same meaning, nor does an apparent resemblance to a storage capacity establish capacity semantics.

### Use hypotheses to drive experiments

When a semantic interpretation is plausible, identify observations that would confirm or falsify it.

Example:

> Hypothesis: this routine loads a sample bank from storage.

Useful follow-up questions include:

- What invokes it?
- Does invocation correspond to a bank-selection operation?
- What storage addresses or files does it access?
- Where does transferred data go?
- Do destination structures correspond to samples or pads?
- Are sample parameters populated?
- Are relevant UI messages displayed?
- Is the routine used during unrelated storage operations?

The objective is not to eliminate inference. It is to make inference **traceable and testable**.

## Repository and artifact discipline (durable working rules)

These rules apply to all work in this repo, independent of any single investigation.

### Authoritative sources; everything else is a lead

The current authoritative documents are the **newest dated revisions** of the evidence ledger
(`SP-808EX_Evidence_Ledger_*`), the architecture reference
(`SP-808EX_Observed_Architecture_Technical_Reference_*`), and the hardware corrections
(`Roland_SP-808_Hardware_Architecture_Corrections_*`), all in the repo root (see `CLAUDE.md` →
"Document authority"). Treat every other document — older dated revisions, anything under
`superseded/`, prose notes — and all existing IDA/semantic names as **leads, not premises**.
Agreement between an IDA name, a helper script, and a Markdown note is not independent confirmation
when they share one origin. When documents conflict, newer firmware/data-flow reconstruction wins
over inherited names and older prose.

### Evidence labels

Label claims with one of **OBSERVED / STRONGLY INFERRED / HYPOTHESIZED / UNRESOLVED / SUPERSEDED** —
the scheme used throughout the ledger and corrections docs. (The "Inferred" / "Speculative" levels
described above map onto STRONGLY INFERRED / HYPOTHESIZED; add UNRESOLVED for insufficient evidence
and SUPERSEDED/CONTRADICTED for retired interpretations.)

### Source and artifact integrity

- Treat the source firmware images (`firmware/SP8EXall.bin`, `firmware/A6_all.bin`) and any IDA
  database as **read-only**; never patch them in place.
- Emit derived artifacts (candidate images, deployment sets, reports) under **unique, dated or
  hash-stamped names**; never overwrite a source or a prior artifact.
- Record the **MD5/SHA-256 of every input and output**, plus the verification method and result,
  alongside the artifact.

### Byte-level verification is not hardware success

A passing byte/payload verification proves only that an artifact matches its manifest/source — it
says nothing about functional correctness or safety. Keep `runtime_validation` explicitly
**UNRESOLVED** until a change is exercised on real hardware, and never describe an untested candidate
as a release or as safe to flash.