import time
import unittest
import os, shutil

from proxy import Proxy

def clean_dump_folder():
      folder = 'dump/'
      for filename in os.listdir(folder):
          file_path = os.path.join(folder, filename)
          if os.path.isdir(file_path):
              shutil.rmtree(file_path)

class ProxyTests(unittest.TestCase):

    def test_deposit_file_when_file_NOT_exists(self):
      # arrange
      # act
      Proxy.deposit_file("a", 2)
      time.sleep(3)
      # assert
      self.assertTrue(os.path.isfile("dump/a/a_1"))
      self.assertTrue(os.path.isfile("dump/a/a_2"))
      self.assertFalse(os.path.isfile("dump/a/a_3"))


    def test_deposit_file_when_file_exists(self):
      # arrange
      Proxy.deposit_file("b", 2)
      time.sleep(3)
      self.assertTrue(os.path.isfile("dump/b/b_1"))
      self.assertTrue(os.path.isfile("dump/b/b_2"))
      self.assertFalse(os.path.isfile("dump/b/b_3"))

      # act
      Proxy.deposit_file("b", 3)
      time.sleep(3)
      # assert
      self.assertTrue(os.path.isfile("dump/b/b_1"))
      self.assertTrue(os.path.isfile("dump/b/b_2"))
      self.assertTrue(os.path.isfile("dump/b/b_3"))
      self.assertFalse(os.path.isfile("dump/b/b_4"))

    @classmethod
    def setUpClass(self):
      print("setUpClass")
      clean_dump_folder()

    @classmethod
    def tearDownClass(self):
      print("tearDownClass")
      clean_dump_folder()

if __name__ == '__main__':
    unittest.main()