#-*-coding:gb2312-*-
import shutil
import os
from debug_file import DebugFile
from executor import run
from model import ChatModel
import re
from memory import Create_Memory, Write_Memory, Move_Memory
from prompt import (initial_system_prompt, 
                    compile_self_correct_system_prompt,
                    simulation_self_correct_system_prompt,
                    testbench_system_prompt)

model_name = "gpt-4"
cnt_times = 5



def Verilog_Code_Search(text: str):
    pattern = r"```The Corrected Verilog Code\s*\n(.*?)```"
    modules = re.findall(pattern, text, re.DOTALL)
    all_modules = ""
    for module in modules:
        # 去除每个模块前后的空白字符
        module = module.strip()
        # 将模块添加到all_modules字符串中，并在模块之间添加空行分隔
        all_modules += module + "\n"
    return all_modules


def Compile_Correct(cnt: int, debug_file: DebugFile):
    Write_Memory(design_name, "\n---------------------------------------\n")
    Write_Memory(design_name, f"The cnt number is {cnt}\n")

    vcompile_message = debug_file.vcompile
    lines = vcompile_message.splitlines()
    vcompile_message = "\n".join(lines[3:])
    
    Write_Memory(design_name, "\n********The Compilor Feedback********\n")
    Write_Memory(design_name, vcompile_message)
    compile_self_correct_user_prompt = f"""[pre_verilog_design_code]:\n{debug_file.design}\n\n[compiler feedback]:\n{vcompile_message}\n\n"""
    
    llm = ChatModel(model_name = model_name)
    messages = [
        {"role":"system", "content": compile_self_correct_system_prompt},
        {"role":"user", "content": compile_self_correct_user_prompt}
    ]
    response = llm.generate(messages)
    Write_Memory(design_name, "\n********The Analyze Content********\n")
    Write_Memory(design_name, response)

    verilog_code = Verilog_Code_Search(response)
    Write_Memory(design_name, "\n********The Verilog Code********\n")
    Write_Memory(design_name,verilog_code)

    Write_Memory(design_name, "\n---------------------------------------\n\n")
    return verilog_code
    
def Simulate_Correct(cnt: int, debug_file: DebugFile):   
    Write_Memory(design_name, "\n---------------------------------------\n")
    Write_Memory(design_name, f"The cnt number is {cnt}\n")


    testbench_user_prompt = f"[The generated RTL code]:\n\n{debug_file.design}"
    
    llm = ChatModel(model_name = model_name)
    feedback = f"[Pre verilog design]:\n{debug_file.design}\n\n[Self-Verification]:\n"
    messages = [
        {"role":"system", "content": testbench_system_prompt},
        {"role":"user", "content": testbench_user_prompt}
    ]
    response = llm.generate(messages)
    feedback += response

    if debug_file.have_origin_testbench:
        vsim_messages = debug_file.vsim
        lines = vsim_messages.splitlines()
        vsim_messages = "\n".join(lines[18:])
        feedback += f"\n\n[ModelSim logs]:\n{vsim_messages}"

    Write_Memory(design_name, "\n********The Simulator Feedback********\n")
    Write_Memory(design_name, feedback)
    
    messages = [
        {"role":"system", "content": simulation_self_correct_system_prompt},
        {"role":"user", "content": feedback}
    ]    
    response = llm.generate(messages)
    Write_Memory(design_name, "\n********The Analyze Content********\n")
    Write_Memory(design_name, response)

    verilog_code = Verilog_Code_Search(response)
    Write_Memory(design_name, "\n********The Verilog Code********\n")
    Write_Memory(design_name, verilog_code)

    Write_Memory(design_name, "\n---------------------------------------\n\n")
    return verilog_code

def Debug_Design(design_name):
    #读取设计描述、设计及test_bench
    init_debug_file = DebugFile(design_name)
    initial_user_prompt = init_debug_file.design_description
    llm = ChatModel(model_name = model_name)
    messages = [
        {"role": "system", "content": initial_system_prompt},
        {"role": "user", "content": initial_user_prompt}
    ]
    initial_answer = llm.generate(messages)
    verilog_code = Verilog_Code_Search(initial_answer)

    #创建内存
    Create_Memory(design_name)
    cnt = 0

    while True:
        debug_file = DebugFile(design_name, verilog_code)
        run(debug_file)

        cnt = cnt + 1
        
        debug_file.Read_Vcompile()
        #基于编译错误修改verilog代码
        if "Errors: 0" not in debug_file.vcompile:
            verilog_code = Compile_Correct(cnt, debug_file)
            continue
        #基于仿真错误修改verilog代码
        else:
            if debug_file.have_origin_testbench:
                debug_file.Read_Vsim()
                if "Your Design Passed" in debug_file.vsim:
                    break
            verilog_code = Simulate_Correct(cnt, debug_file)
        
        if cnt >= cnt_times:
            break
    Move_Memory(design_name)
    
if __name__ == "__main__":
    input_path = "./input"
    for root, dir, files in os.walk(input_path):
        design_name = os.path.basename(root)
        if design_name == "input":
            continue
        Debug_Design(design_name)

#1. 仿真testbench反馈所得到的信息比较少，不容易进行功能修改
#2. 多次迭代修改代码过程中大模型可能重复犯之前犯过的错误
#3. 大模型会忽略prompt中可能存在的隐含的重要信息