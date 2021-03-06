"""
  Elastool -- Elastic toolkit for finite-temperature elastic constants calculations

  Copyright (C) 2019-2020 by Zhong-Li Liu

  This program is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software Foundation
  version 3 of the License.

  This program is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
  PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  E-mail: zl.liu@163.com
"""
from os import system
from os.path import isfile
import subprocess
from time import sleep
from write_incar import write_incar
from ase.io import vasp
from read_input import indict
from extract_mean_values import get_pressure, mean_pressure


def vasp_run(step, kpoints_file_name, cwd):
    write_incar(step, cwd)
    system("cp %s/%s KPOINTS" % (cwd, kpoints_file_name))

    pos = vasp.read_vasp('POSCAR')
    chem_symb = pos.get_chemical_symbols()

    ele_list = []
    for i in chem_symb:
        if i not in ele_list:
            ele_list.append(i)
    if isfile('POTCAR'):
        system("rm POTCAR")

    for ele in ele_list:
        system("cat %s/POTCAR-%s >> POTCAR" % (cwd, ele))

    # method_stress_statistics = indict['method_stress_statistics'][0]

    for line in open('INCAR','r'):
        if 'PSTRESS' in line:
            # p_target = 0.1 * float(line.split()[2])
            break

    if int(indict['run_mode'][0]) == 1:
        # computcode = indict['parallel_submit_command'][3].split("/")[-1]
        para_sub_com = ''
        for i in range(len(indict['parallel_submit_command'])):
            para_sub_com += indict['parallel_submit_command'][i]
            para_sub_com += ' '

        #para_sub_com = 'yhrun -p paratera -N 1 -n 24 vasp_std'
        #print(para_sub_com)
        #start = datetime.datetime.now()

        go = subprocess.Popen(para_sub_com, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        while go.poll() is None:
            sleep(2)
            #if method_stress_statistics == 'dynamic' and 'NO_STRAIN_MD' in os.getcwd():
            #    p = get_pressure('OUTCAR')
            #    mean_press = 0.1 * mean_pressure('OUTCAR', 1)

            #    if mean_press is not np.nan and len(p) > 2:
            #        if abs(mean_press - p_target) < 0.2:
                        #os.system("killall -9 $(ps H -e -o cmd --sort=pcpu | tail -1)")
            #            time.sleep(10)
            #            os.system("killall -9 vasp544")

            #now = datetime.datetime.now()
            #if (now - start).seconds > float(indict['MaxHour'][0])*3600:
            #    os.system("killall -9 $(ps H -e -o cmd --sort=pcpu | tail -1)")
            #    break
        pos_optimized = vasp.read_vasp('CONTCAR')

    elif int(indict['run_mode'][0]) == 2:
        pos_optimized = pos

    elif int(indict['run_mode'][0]) == 3:
        pos_optimized = vasp.read_vasp('CONTCAR')

    return pos_optimized
