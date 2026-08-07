# 4D Reconstruction — Rules

- Language: Python, JAX
- Always pin models/denoisers to a single GPU via `configure_devices([device])`
- `dejitter_4d_dct` is the canonical dejitter function — modify carefully
