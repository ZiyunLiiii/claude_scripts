# 4D MACE — Progress Log

## Current Status
Working multi-GPU implementation. DCT-I dejittering integrated. Null-space projection approach under investigation.

## Log (newest first)

### 2026-08-07
- Shared full multi-GPU MACE script
- DCT-I dejittering (period=6, harmonics=True) applied in forward agent and all prior agents
- Identified issue: direct dejitter may violate AX = y
- New idea: null-space projection — x + (I - A⁺A)(Px - x) — not yet implemented
