#-*-coding:gb2312-*-
import os
import shutil
from debug_file import DebugFile
def file_copy(src_path: str, dir_path: str, file_name: str) -> None:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, mode=0o777)
    if os.path.exists(dir_path + "/" + file_name):
        os.remove(dir_path + "/" + file_name)
    shutil.copy(src_path + "/" + file_name, dir_path + "/" + file_name)

def Create_Work_Path(design_name):
    work_path = f"./workdir/{design_name}"
    if not os.path.exists(work_path):
        os.makedirs(work_path)
    else:
        shutil.rmtree(work_path)
        os.makedirs(work_path)
    os.makedirs(work_path + "/" + "design")

def Simulate(Do_file, sim_path):
    path_temp = os.getcwd()
    if not os.path.exists(sim_path + "\\wave_simulation.do"):
        file_copy(Do_file, sim_path, "wave_simulation.do")
    os.chdir(sim_path)
    os.system("vsim -c -do wave_simulation.do -do quit")
    os.chdir(path_temp)

def modelsim_done(dir_path: str):
    target_path = dir_path + "/vsim.wlf"
    if os.path.exists(target_path):
        os.remove(target_path)
    target_path = dir_path + "/modelsim.ini"
    if os.path.exists(target_path):
        os.remove(target_path)
    target_path = dir_path + "/lib"
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    target_path = dir_path + "/transcript"
    if os.path.exists(target_path):
        os.remove(target_path)

def modelsim_done(dir_path: str):
    target_path = dir_path + "/vsim.wlf"
    if os.path.exists(target_path):
        os.remove(target_path)
    target_path = dir_path + "/modelsim.ini"
    if os.path.exists(target_path):
        os.remove(target_path)
    target_path = dir_path + "/lib"
    if os.path.exists(target_path):
        shutil.rmtree(target_path)
    target_path = dir_path + "/transcript"
    if os.path.exists(target_path):
        os.remove(target_path)

def Compile(Do_file, sim_path):
    path_temp = os.getcwd()
    if not os.path.exists(sim_path + "\\wave_compilation.do"):
        file_copy(Do_file, sim_path, "wave_compilation.do")
    os.chdir(sim_path)
    os.system("vsim -c -do wave_compilation.do -do quit")
    os.chdir(path_temp)

def run(debug_file: DebugFile):
    #创建工作目录
    Create_Work_Path(debug_file.design_name)
    #基于 modelsim 进行编译和仿真
    #在工作目录下创建文件
    try:
        Root_path = os.path.dirname(os.path.realpath(__file__))
    except:
        Root_path = os.getcwd()
    work_path = f"./workdir/{debug_file.design_name}"
    work_design_path = f"./workdir/{debug_file.design_name}/design"
    #创建内存
    
    if debug_file.have_origin_testbench == True:
       debug_file.Create_Design(work_design_path)
       debug_file.Create_Testbench(work_design_path)
       Simulate(Root_path,work_path)
       modelsim_done(work_path)
    else:
        debug_file.Create_Design(work_design_path)
        Compile(Root_path,work_path)
if __name__ == "__main__":
    with open("./alu.v","r") as file:
        verilog_code = file.read()
    debug_file = DebugFile(design_name = "alu", design = verilog_code)
    run(debug_file)