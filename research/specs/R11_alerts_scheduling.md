# R11 — Alert Reliability, Free Notification Channels and Local Scheduling

| Field | Value |
| --- | --- |
| Wave / priority | 2 |
| Owner role | Application engineer |
| Effort budget | ~4 agent-hours |
| Feeds | P5 (inbox/digest/transports), P6 (scheduler, operations) |
| Acceptance checks | A03, A22, A25, A27 |

## Why this matters

Alerts must be persisted before delivery, deduplicated by an idempotency key, retried in a bounded way, and never lost or duplicated (§10.3). The user hasn't chosen an external channel (§2, §16). This track gives the PO a short, evidence-based channel menu to offer the user, and a reliable local design.

## Read first

Handoff §10 (all), §12.1 (Overview/Settings), §15, §16, §14 (A03, A22, A25, A27). Also R05 findings for scheduler/storage choices.

## Research questions

1. **Event persistence pattern.** The transactional outbox pattern in SQLite: event table, delivery-attempt table, idempotency key = (security, plan/policy version, event type, session/state transition). Exactly-once *effect* vs at-least-once delivery. Recommend a schema and a retry/backoff policy.
2. **State-transition semantics.** How to generate events only on meaningful transitions (e.g., `WAIT → ENTRY_SETUP`) while the digest repeats the latest state. Handle re-runs of the same session (A03) and late corrections.
3. **Free channels.** Compare Telegram bot, email (SMTP via an existing account), Windows toast notifications, ntfy (self-hosted or public), Zalo Official Account / Zalo notification options, Discord webhook, and Pushover (paid, list only). For each give: cost, setup steps, reliability, rate limits, privacy (account data leaving the machine), terms on automated messages, and Vietnamese-user popularity.
4. **Digest format.** Good practice for a concise end-of-day digest: holdings warnings first, then new setups, then the coverage/data-quality footer, with an explicit `DEMO`/`SYNTHETIC` label. Avoid alert fatigue and FOMO (§19.2 Exchange 4).
5. **Scheduling and missed runs.** Building on R05: trigger the job by data completeness (poll until the EOD bar exists, with a cutoff) rather than wall-clock time alone. Detect missed runs after sleep and label catch-up runs without backdating delivery times (A27).
6. **Operational alerts.** Which failures deserve a notification (auth required, provider down, partial coverage, delivery failure) vs only a dashboard banner.

## Deliverable

`research/findings/R11_findings.md` with: an outbox schema and state diagram (text), a channel comparison table and recommended shortlist to present to the user (no channel is configured until the user picks one), a digest template, and a missed-run/catch-up policy.

## Out of scope

Intraday streaming alerts (a later mode, §10.3), and sending any real message.

## Known traps

- Generating events in the delivery loop, which loses them on failure.
- Using wall-clock time as the idempotency key.
- Delivering synthetic alerts externally.
- Telegram/Zalo terms on bots that handle financial content.
