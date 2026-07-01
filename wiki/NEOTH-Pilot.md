# NEOTH Pilot

NEOTH is the first intended runtime testbed for Delta Cosmology's LLM/agent
branch.

Repository: https://github.com/The-Geek-Freaks/NEOTH

## Research Question

Can a Babel feature predict LLM/agent runtime degradation before it becomes a
visible failure?

## Runtime Signals

- inference start/end,
- tool call start/end,
- agent spawn/end,
- fallback attempt/result,
- retries,
- errors,
- context pressure,
- queue load,
- task outcome labels.

## Candidate Collapse Labels

- agent loop,
- retry storm,
- tool timeout cascade,
- context limit failure,
- fallback failure,
- semantic degradation,
- objective failure.

## Protocol

1. Observe NEOTH orchestration events asynchronously.
2. Aggregate rolling windows over inference, tool, retry, fallback, context,
   agent, and outcome signals.
3. Compute raw features C, K, M, A, V, D, H.
4. Compute candidate Babel scores.
5. Test whether the score improves prediction beyond raw telemetry.

## Repository Files

- Protocol: https://github.com/The-Geek-Freaks/delta-kosmologie/blob/main/protocols/pilot-b-neoth.md
- Event schema: https://github.com/The-Geek-Freaks/delta-kosmologie/blob/main/schemas/neoth-babel-event.schema.json
- Window schema: https://github.com/The-Geek-Freaks/delta-kosmologie/blob/main/schemas/neoth-babel-window.schema.json
