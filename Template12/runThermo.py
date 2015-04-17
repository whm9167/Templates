import os
import re
import shutil
from xlrd import *
from xlwt import *
from xlutils.copy import copy

name = ''
temperature=[298.15, 300, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400, 2500]
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.name',tmp_file):
		name = tmp_file[0:-5]
		fr = file(tmp_file, 'r')
		tmp_lines = fr.readlines()
		tmp_line = tmp_lines[5].strip(' \n')
		temperature = map(float, tmp_line.split())
		fr.close()			

if os.path.exists(os.getcwd()+'/thermoOutput'):
	shutil.rmtree('thermoOutput')
os.mkdir('thermoOutput')
if os.path.exists(os.getcwd()+'/thermoOutputATM'):
	shutil.rmtree('thermoOutputATM')
os.mkdir('thermoOutputATM')

# run thermo
os.chdir('thermoInput')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.out',tmp_file):
		os.remove(tmp_file)
	else:
		os.system('thermo ' + tmp_file)
tmp_fileLists = os.listdir(pwd)
tmp_fileLists = [tmp_file for tmp_file in tmp_fileLists if re.search('.out',tmp_file)]
os.chdir('..')
for tmp_file in tmp_fileLists:
	shutil.move('thermoInput/'+tmp_file,'thermoOutput')

os.chdir('thermoInputATM')
pwd = os.getcwd()
tmp_fileLists = os.listdir(pwd)
for tmp_file in tmp_fileLists:
	if re.search('.out',tmp_file):
		os.remove(tmp_file)
	else:
		os.system('thermo ' + tmp_file)
tmp_fileLists = os.listdir(pwd)
tmp_fileLists = [tmp_file for tmp_file in tmp_fileLists if re.search('.out',tmp_file)]
os.chdir('..')
for tmp_file in tmp_fileLists:
	shutil.move('thermoInputATM/'+tmp_file,'thermoOutputATM')

wb=open_workbook(name + '.xls')
wb_new = copy(wb)
sh=wb_new.get_sheet(2)				#if overwrite to use cell_overwrite_ok=True
sh.cell_overwrite_ok = True
tmp_row = 3

for tmp_file in tmp_fileLists:
	sh.write(tmp_row,0,tmp_file[7:-4])
	fr = file('thermoOutput/'+tmp_file,'r')
	lastlines = fr.readlines()[-len(temperature):]
	for tmp_line in lastlines:
		tmp_line = tmp_line.strip()
		tmp_line = tmp_line.split()
		for i in range(len(tmp_line)):
			sh.write(tmp_row,i+1,float(tmp_line[i]))
		tmp_row += 1
	fr.close()

	tmp_row -= len(temperature)
	fr = file('thermoOutputATM/'+tmp_file,'r')
	lastlines = fr.readlines()[-len(temperature):]
	for tmp_line in lastlines:
		tmp_line = tmp_line.strip()
		tmp_line = tmp_line.split()
		for i in range(4, len(tmp_line)):
			sh.write(tmp_row,i+18, float(tmp_line[i]))
		tmp_row += 1
	fr.close()

	tmp_row += 1

wb_new.save(name + '.xls')

print 'run Thermo successfully!\n'
		


