#!/usr/bin/python

from pathlib import Path
import json
import argparse

from ovito.data import DataCollection
from ovito.io import import_file, export_file
from ovito.modifiers import PolyhedralTemplateMatchingModifier, ExpressionSelectionModifier, ClusterAnalysisModifier, WrapPeriodicImagesModifier


def add_particles_in_clusters(num_clusters: int) -> callable:

    def wrapper(frame: int, data: DataCollection) -> None:

        centers_of_mass = data.tables['clusters']['Center of Mass'][...][:num_clusters]
        for center_of_mass in centers_of_mass:
            data.particles_.add_particle(center_of_mass)
    
    return wrapper


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input_path',
        help='The file path containing the input MD run',
        type=str
    )
    parser.add_argument(
        'output_path',
        help='The file path to save the MD run with the new particle',
        type=str
    )
    parser.add_argument(
        '--num_clusters',
        help='The number of particles to add',
        type=int,
        default=1
    )
    parser.add_argument(
        '--rmsd_cutoff',
        help='The RMSD cutoff for polyhedral template matching. Defaults to 0.12',
        type=float,
        default=0.12
    )
    parser.add_argument(
        '--export_config_path',
        help='Optional configuration file specifying how the file is output.',
        type=str,
        default=None
    )

    return parser.parse_args()


def main():
    
    args = parse_args()

    input_path = Path(args.input_path)
    pipeline = import_file(input_path)
    
    pipeline.modifiers.append(
        PolyhedralTemplateMatchingModifier(rmsd_cutoff=args.rmsd_cutoff)
    )
    pipeline.modifiers.append(
        ExpressionSelectionModifier(expression='StructureType==0')
    )
    pipeline.modifiers.append(
        ClusterAnalysisModifier(only_selected=True, sort_by_size=True, compute_com=True)
    )
    pipeline.modifiers.append(
        add_particles_in_clusters(num_clusters=1)
    )
    pipeline.modifiers.append(
        WrapPeriodicImagesModifier()
    )
    
    if not args.export_config_path:
        export_kwargs = {
            'format': 'lammps/dump',
            'columns': [
                'Particle Identifier',
                'Particle Type',
                'Position.X',
                'Position.Y',
                'Position.Z'
            ]
        }
    else:
        config_path = Path(args.export_config_path)
        with open(config_path, 'r') as file:
            export_kwargs = json.load(file)

    output_path = Path(args.output_path)
    export_file(pipeline, output_path, multiple_frames=True, **export_kwargs)

if __name__ == '__main__':

    main()
