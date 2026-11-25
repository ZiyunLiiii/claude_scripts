# MBIRTorch MCP server: goal

The goal is an MCP server for MBIRTorch that gives an AI agent a fixed set of operations:
loading data, running a reconstruction, and inspecting the result.  The server is developed
and tested with Claude Code.  It is the first step toward an agent that runs reconstructions
on its own.

The code is in the private repository `git@github.com:ZiyunLiiii/mcp_sandbox.git`.  Its README
explains the setup.  This folder holds the goal and the progress log.

## Design

Claude Code runs on the Mac and starts the server on a Gautschi login node through ssh.  The
server is a light controller.  It reads volumes plane by plane and returns summaries and
images.  Heavy work, such as preprocessing a scan or running a reconstruction, will run as
Slurm jobs in the mbirtorch environment.  The server will submit those jobs and read their
outputs.  The login node never runs a reconstruction.

## Stages

1. Open and inspect 3D and 4D volumes.  Done on 2026-11-03.
2. Load scan data.  A tool submits a job that runs the mbirtorch preprocessing of a scan
   (NSI or Zeiss) and writes the sinogram and the geometry parameters.  Tools then show
   sinogram views and the parameters.
3. Run a reconstruction.  A tool submits an MBIR or MACE4D job with given parameters, a
   second tool reports the job state, and `load_volume` opens the result.
4. Compare results.  Tools give the difference and the NRMSE between two volumes, and a GIF
   of a 4D volume over time.
