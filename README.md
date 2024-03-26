# Add Point Defect as Particle

This repository provides an OVITO-based command-line interface (CLI) to add a point-defect as a particle in a molecular dynamics simulation of a solid.

To install, run:

```bash
pip install ovito~=3.10.4
git clone https://github.com/MUEXLY/apdap
```

To run the CLI, run:

```bash
python apdap.py ${input_file} ${output_file}
```

where `input_file` is the path to the input file containing the molecular dynamics run data (which can be in any OVITO-readable format), and `output_file` is the desired output file. By default, this will be output in a LAMMPS-style dump format. This can be changed by creating a configuration file in JSON format.

For example, to instead export into xyz format, one can create a file `output.json` with contents:

```json
{
    "format": "xyz",
    "columns": [
        "Particle Identifier",
        "Particle Type",
        "Position.X",
        "Position.Y",
        "Position.Z"
    ]
}
```

and then run:

```bash
python apdap.py ${input_file} ${output_file} --export_config_path output.json
```

See OVITO's documentation [here](https://docs.ovito.org/python/modules/ovito_io.html#ovito.io.export_file) for available formats and column names.

Other additional optional arguments are `--num_clusters` and `--rmsd_cutoff`, which respectively control the number of point defects to detect and add particles for and the RMSD cutoff for polyhedral template matching for defect detection.

You can quickly see a description of all available arguments by running:

```bash
python apdap.py --help
```