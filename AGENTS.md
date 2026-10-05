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