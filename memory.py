import os
import shutil

def Create_Memory(design_name: str):
    work_design_path = f"."
    memory_path = os.path.join(work_design_path,"memory.txt")
    with open(memory_path, "w", encoding = "utf-8") as file:
        file.write("")

def Write_Memory(design_name: str, text: str):
    work_design_path = f"."
    memory_path = os.path.join(work_design_path,"memory.txt")
    with open(memory_path, "a", encoding = "utf-8") as file:
        file.write(text)

def Move_Memory(design_name: str):
    src_dir = "./memory.txt"
    dest_dir = f"./workdir/{design_name}/design/memory.txt"
    shutil.move(src_dir, dest_dir)