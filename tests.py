import time
import unittest
import os, shutil
import filecmp

from proxy import Proxy

def clean_folders():
      folder = "dump/"
      for filename in os.listdir(folder):
          file_path = os.path.join(folder, filename)
          if os.path.isdir(file_path):
              shutil.rmtree(file_path)

      folder = "restore/"
      for filename in os.listdir(folder):
          file_path = os.path.join(folder, filename)
          if os.path.isfile(file_path) and filename != ".gitkeep":
              os.remove(file_path)

class ProxyTests(unittest.TestCase):
    def test_deposit_file_when_file_NOT_exists(self):
      # arrange
      self.assertFalse(os.path.isfile("dump/a/a_1"))

      # act
      Proxy.deposit_file("a", 2)
      time.sleep(1)

      # assert
      self.assertTrue(os.path.isfile("dump/a/a_1"))
      self.assertTrue(os.path.isfile("dump/a/a_2"))
      self.assertFalse(os.path.isfile("dump/a/a_3"))

    def test_deposit_file_when_file_exists(self):
      # arrange
      Proxy.deposit_file("b", 2)
      time.sleep(1)
      self.assertTrue(os.path.isfile("dump/b/b_1"))
      self.assertTrue(os.path.isfile("dump/b/b_2"))
      self.assertFalse(os.path.isfile("dump/b/b_3"))

      # act
      Proxy.deposit_file("b", 3)
      time.sleep(1)

      # assert
      self.assertTrue(os.path.isfile("dump/b/b_1"))
      self.assertTrue(os.path.isfile("dump/b/b_2"))
      self.assertTrue(os.path.isfile("dump/b/b_3"))
      self.assertFalse(os.path.isfile("dump/b/b_4"))

    def test_recover_file_when_NOT_exists(self):
      # arrange
      clean_folders()
      self.assertFalse(os.path.isfile("dump/a/a_1"))

      # act
      Proxy.recover_file("a")

      #assert
      self.assertFalse(os.path.isfile("restore/a"))
    
    def test_recover_file_when_exists(self):
      # arrange
      clean_folders()
      Proxy.deposit_file("b", 2)
      time.sleep(1)
      self.assertTrue(os.path.isfile("dump/b/b_1"))
      self.assertTrue(os.path.isfile("dump/b/b_2"))
      self.assertFalse(os.path.isfile("dump/b/b_3"))

      # act
      Proxy.recover_file("b")

      #assert
      self.assertTrue(os.path.isfile("restore/b"))
      filecmp.cmp("b", "restore/b")

    @classmethod
    def setUpClass(self):
      print("setUpClass")
      clean_folders()

    @classmethod
    def tearDownClass(self):
      print("tearDownClass")
      clean_folders()

if __name__ == "__main__":
    unittest.main()