from genericpath import exists
import os
import unittest

class TestReplacer(unittest.TestCase):
    def test_replace_in_place(self):
        filepath = "tests/test_aytempler_data/in_place_file.txt"
        with open(filepath, "w+") as file:
            file.write('${REPL}')
        os.system(f'REPL=repl python ayTempler.py -i {filepath}')
        with open(filepath) as file:
            self.assertEqual('repl', file.read())

    def test_replace_alternative_output(self):
        filepath_in = "tests/test_aytempler_data/alternative_output_file_in.txt"
        filepath_out = "tests/test_aytempler_data/alternative_output_file_out.txt"
        with open(filepath_in, "w+") as file:
            file.write('${REPL}')
        try:
            os.remove(filepath_out)
        except:
            pass
        self.assertFalse(exists(filepath_out), "file should have been removed before start")
        os.system(f'REPL=repl python ayTempler.py -i {filepath_in} -o {filepath_out}')
        self.assertTrue(exists(filepath_out), "file was not created")
        with open(filepath_out) as file:
            self.assertEqual('repl', file.read())

    def test_blacklist_variables(self):
        filepath = "tests/test_aytempler_data/blacklist.txt"
        with open(filepath, "w+") as file:
            file.write('${FOO}=moo ${UHH}=mhh ${BAR}=mar ${BAZ}=maz')
        os.system(f'UHH=mhh FOO=moo BAR=mar BAZ=maz python ayTempler.py -i {filepath} -b FOO -b BAR -b BAZ')
        with open(filepath) as file:
            self.assertEqual('${FOO}=moo mhh=mhh ${BAR}=mar ${BAZ}=maz', file.read())

    def test_whitelist_variables(self):
        filepath = "tests/test_aytempler_data/blacklist.txt"
        with open(filepath, "w+") as file:
            file.write('${FOO}=moo ${UHH}=mhh ${BAR}=mar ${BAZ}=maz')
        os.system(f'UHH=mhh FOO=moo BAR=mar BAZ=maz python ayTempler.py -i {filepath} -w UHH -w BAZ')
        with open(filepath) as file:
            self.assertEqual('${FOO}=moo mhh=mhh ${BAR}=mar maz=maz', file.read())
        
        
#create directories
#blacklist, whitelist