
# Copyright (c) 2024 Dr. Deniz Dahman's <denizdahman@gmail.com>
 
# This file may be used under the terms of the GNU General Public License
# version 3.0 as published by the Free Software Foundation and appearing in
# the file LICENSE included in the packaging of this file.  Please review the
# following information to ensure the GNU General Public License version 3.0
# requirements will be met: http://www.gnu.org/copyleft/gpl.html.
# 
# If you do not wish to use this file under the terms of the GPL version 3.0
# then you may purchase a commercial license.  For more information contact
# denizdahman@gmail.com.
# 
# This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
# WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.

# Support the author of this package on:.#
# https://patreon.com/user?u=118924481
# https://www.youtube.com/@dahmansphi 
# https://dahmansphi.com/subscriptions/


import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class AttackAI:

  _attack_img_path_normal = None
  _attack_img_path_sick = None
  _attack_img_size_normal = None
  _attack_img_size_sick = None
  __cls_names = None

  _attack_img_path = None
  _attack_img_size = None
  _attack_img_arr = None

  def __init__(self) -> None:
    pass

  def _plant_attack_img(self, paths):
    '''this function plant the malicious cancer root'''
    for _indx in range(len(paths)):
      path = paths[_indx]

      if _indx == 0:
        self._attack_img_path_normal = path
        _img = [im for im in os.listdir(path) if im.lower().endswith(('.jpg', '.jpeg'))]
        _img_path = os.path.join(path, _img[0])

        _attack_img = Image.open(_img_path)
        self._attack_img_size_normal = np.array(_attack_img).shape

      else:
        self._attack_img_path_sick = path
        _img = [im for im in os.listdir(path) if im.lower().endswith(('.jpg', '.jpeg'))]
        _img_path = os.path.join(path, _img[0])

        _attack_img = Image.open(_img_path)
        self._attack_img_size_sick = np.array(_attack_img).shape


  def _return_measures(self, tuple_list, size_attack):
    '''this tool capture the math of the img and decide on the location'''

    _attack_size = tuple()
    _img_victm = tuple_list
    _row_measure, _col_measure = int(_img_victm[0]*size_attack), int(_img_victm[1]*size_attack)

    _start_row, _start_col = int((int(_img_victm[0]) - _row_measure)/2) , int((int(_img_victm[1]) - _col_measure)/2)

    return (_row_measure, _col_measure), (_start_row, _start_col)

  def _attack_type_one(self, paths, size_attack, stamp=None ,explore=False):
    '''this function archetict the attack structure where it handdle the motion accordingly'''
    _folders = [folder for folder in os.listdir(paths) if os.path.isdir(os.path.join(folder, paths))]
    # self.__cls_names = _folders

    try:
      for _folder in _folders:
        _folder_path = os.path.join(paths, _folder)
        _imgs = [im for im in os.listdir(_folder_path) if im.lower().endswith(('.jpg', '.jpeg'))]

        _count = 1
        for _index in range(len(_imgs)):
          _img = _imgs[_index]
          _img_path = os.path.join(_folder_path, _img)

          _img_pli = Image.open(_img_path)
          _img_arr = np.array(_img_pli)

          _measures = self._return_measures(tuple_list=_img_arr.shape, size_attack=size_attack)

          _count +=1
          _rows = _measures[0][0]
          _cols = _measures[0][1]

          _start_row = _measures[1][0]
          _start_col = _measures[1][1]

          _stop_row = _start_row+_rows
          _stop_col = _start_col+_cols

          _attack_img_arr = np.random.rand(_rows, _cols)

          # stamp
          if stamp:
            _isitImg = stamp.endswith(('.jpg', '.jpeg'))

            if _isitImg:
              _stamp = Image.open(stamp)
              _siz_row, _siz_col = int(_rows * 0.6), int(_cols*0.6)
              _new_stamp = _stamp.resize((_siz_col,_siz_row))
              _new_stamp_arr = np.array(_new_stamp)

              _attack_img_arr[:_siz_row, :_siz_col] = _new_stamp_arr
            else:
              print("stamp can only be of type jpg")
          else:
            _attack_img_arr = _attack_img_arr

          _img_arr[_start_row:_stop_row, _start_col:_stop_col] = _attack_img_arr
          _new_attacked_img = Image.fromarray(_img_arr)

          if _count == 2 and explore == True:
            print("This is a smple of the attack")
            plt.imshow(_new_attacked_img)
            break
          else:
            os.remove(os.path.join(_folder_path, _img))
            _new_attacked_img.save(os.path.join(_folder_path, _img))

        if explore == False:
          print(f"Attack is successful, number of imgs have been poisoned are {_count} inside class {_folder}")
        else:
          break

    except:
      pass

  def _attack_type_two(self, paths, explore=False):

    if paths:
      _folders = [folder for folder in os.listdir(paths) if os.path.isdir(os.path.join(folder, paths))]

      if explore:
        print(f"We found {len(_folders)} CLASSESS in the provided path: inside details as follow:")
        print("______________________________________________________________________")
        for folder in _folders:
          _cls_name = folder
          _folder_path = os.path.join(paths, folder)
          _imgs = [im for im in os.listdir(_folder_path) if im.lower().endswith(('.jpg', '.jpeg'))]
          print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
          print(f"We found class {_cls_name} that have {len(_imgs)} number of imgages")
          print("_______________________________________________________________")

        print("")
        print(f"if you continue the attack we shall replace the contents of the {len(_folders)} classess")
        print(f"to do so you shall call execute_attack_t2() function")
        print("")
      else:
        for _inx in range(len(_folders)):
          _folder_one = _folders[_inx]
          _copy_folder_one_name = _folders[_inx]

          _folder_two = None
          for _cls in _folders:
            if _cls != _folder_one:
              _folder_two = _cls

          _copy_folder_two_name = _folder_two

          _first_folder = os.path.join(paths, _folder_one)
          temp_path = os.path.join(paths, 'temp')
          os.rename(_first_folder, temp_path)

          _other_folder = os.path.join(paths, _folder_two)
          _it_new_name = os.path.join(paths, _copy_folder_one_name)
          os.rename(_other_folder, _it_new_name)

          _first_folder_from_temp = os.path.join(paths, 'temp')
          _it_new_name = os.path.join(paths, _copy_folder_two_name)
          os.rename(_first_folder_from_temp, _it_new_name)

          break

        print(f"attack is successful, content of {_folders} are swaped!")


  def explore_attack_t1(self, paths, attack_size,stamp=None):
    if attack_size >= 0 and attack_size <= 1:
      print("This is a simulative tool illustrates poisoning attack on AI model. It corrupts a folder that suppose to serve as AI model input update")
      print("The tool is designed by Dr. Deniz Dahman ONLY FOR EDUCATION PURPOSE")
      print("Copy right and use of the tool are mentioned in the repo side of the tool")
      print("for further information please visit www.dahmansphi.com")
      print("********************************************************")
      self._attack_type_one(explore=True, paths=paths, size_attack=attack_size,stamp=stamp)
    else:
      print("Attack size can be any value from 0-1")

  def execute_attack_t1(self, paths, attack_size, stamp):
    if attack_size >= 0 and attack_size <= 1:
      print("This is a simulative tool illustrates poisoning attack on AI model. It corrupts a folder that suppose to serve as AI model input update")
      print("The tool is designed by Dr. Deniz Dahman ONLY FOR EDUCATION PURPOSE")
      print("Copy right and use of the tool are mentioned in the repo side of the tool")
      print("for further information please visit www.dahmansphi.com")
      print("********************************************************")
      self._attack_type_one(explore=False, paths=paths, size_attack=attack_size,stamp=stamp)
    else:
      print("Attack size can be any value from 0-1")
# ***************************************************************************************************************
  def explore_attack_t2(self, paths):
    print("This is a simulative tool illustrates poisoning attack on AI model. It corrupts a folder that suppose to serve as AI model input update")
    print("The tool is designed by Dr. Deniz Dahman ONLY FOR EDUCATION PURPOSE")
    print("Copy right and use of the tool are mentioned in the repo side of the tool")
    print("for further information please visit www.dahmansphi.com")
    print("********************************************************")

    self._attack_type_two(paths=paths, explore=True)

  def execute_attack_t2(self, paths):

    print("This is a simulative tool illustrates poisoning attack on AI model. It corrupts a folder that suppose to serve as AI model input update")
    print("The tool is designed by Dr. Deniz Dahman ONLY FOR EDUCATION PURPOSE")
    print("Copy right and use of the tool are mentioned in the repo side of the tool")
    print("for further information please visit www.dahmansphi.com")
    print("********************************************************")
    self._attack_type_two(paths=paths, explore=False)

