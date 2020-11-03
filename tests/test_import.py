import logging
import cimpy
import os
import glob
import pytest_check as check
import pickle
from pathlib import Path

logging.basicConfig(filename='Test_import.log', level=logging.INFO, filemode='w')

short_profile_name = {
    "DiagramLayout": 'DL',
    "Dynamics": "DY",
    "Equipment": "EQ",
    "GeographicalLocation": "GL",
    "StateVariables": "SV",
    "SteadyStateHypothesis": "SSH",
    "Topology": "TP"
}

example_dir = Path(os.path.join(os.path.dirname(__file__), '../cimpy/examples/sampledata/CIGRE_MV')).resolve()

# This function tests the import functionality by importing files and comparing them to previously imported and pickled
# files.
def test_import():
    global example_dir
    test_files = []
    for file in example_dir.glob('*.xml'):
        test_files.append(str(file.absolute()))

    imported_result = cimpy.cim_import(test_files, 'cgmes_v2_4_15')

    import_resolved = cimpy.cimexport._get_class_attributes_with_references(imported_result, 'cgmes_v2_4_15')

    ref_dict_path = Path(os.path.join(os.path.dirname(__file__), 'CIGREMV_import_reference_cgmes_v2_4_15.p'))
    check_dict_pickle = pickle.load(open(ref_dict_path, 'rb'))

    for elem in import_resolved:
        check.is_in(elem, check_dict_pickle)
