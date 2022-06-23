from pathlib import Path
from typing import Union

from rdkit import Chem
from rdkit.Chem import PandasTools


def extract_files(
        base_dir: Union[str, Path] = Path(
            '/Users/marcobertolini/Documents/Arbeit/data/electron_density/QMugs/structures/'),
        target_dir: Union[str, Path] = Path(
            '/Users/marcobertolini/Documents/Arbeit/data/electron_density/QMugs/structures_xyz/')
):
    target_dir.mkdir(parents=True, exist_ok=True)

    for chembl_id_dir in base_dir.iterdir():
        if not chembl_id_dir.is_dir():
            continue
        chembl_id = chembl_id_dir.name

        for conf in chembl_id_dir.iterdir():
            frame = PandasTools.LoadSDF(
                str(conf),
                smilesName='SMILES',
                molColName='Molecule',
                includeFingerprints=False,
                removeHs=False
            )
            try:
                xyz = Chem.rdmolfiles.MolToXYZBlock(frame.Molecule[0])
            except AttributeError:
                print(str(conf))

            conf_id = chembl_id + '_' + conf.name
            file_name = conf_id + ".xyz"

            file_path = target_dir / file_name

            f = open(file_path, "w+")
            f.write(xyz)
            f.close()


if __name__ == '__main__':
    extract_files()
