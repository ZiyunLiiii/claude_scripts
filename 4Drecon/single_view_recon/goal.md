# Single-View 4D Recon — Goal

## Setup
- **Object**: plume injected into pork belly tissue
- **Acquisition**: scans from a single fixed angle (not a full CT rotation); 10000 - 32000 projections
- **Reference**: full CBCT scan of the final steady-state plume (available as prior)
- **Goal**: reconstruct the 4D evolution of the plume from single-view data

## Challenge
- Single-view is severely underdetermined — very large null space
- Must leverage steady-state CBCT as structural prior or reference frame

## Objectives
- [ ] Survey literature on single-view / limited-angle 4D reconstruction
- [ ] Identify candidate methods (learning-based, model-based, or hybrid)
- [ ] Design reconstruction approach using steady-state CBCT as prior
