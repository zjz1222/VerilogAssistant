import os
import shutil
class DebugFile():
    design_name: str
    have_origin_testbench: bool 
    def __init__(self, design_name, design: str = ""):
        print(design_name)
        self.design_name = design_name
        self.design = design
        self.vcompile = ""
        self.vsim = ""
        with open(f"./input/{design_name}/design_description.txt","r") as file:
            self.design_description = file.read()
        self.origin_testbench = ""
        if os.path.exists(f"./input/{design_name}/test_bench.v"):
            self.have_origin_testbench = True
            with open(f"./input/{design_name}/test_bench.v","r",encoding = "utf-8") as file:
                self.origin_testbench = file.read()
        else:
            self.have_origin_testbench = False
        self.test_bench = self.origin_testbench
    def Create_Design(self, work_path):
        file_path = os.path.join(work_path,f"{self.design_name}.v")
        with open(file_path, "w", encoding = "utf-8") as file:
            file.write(self.design)
    def Create_Testbench(self,work_path):
        src_dir = f"./input/{self.design_name}"
        dest_dir = work_path
        for item in os.listdir(src_dir):
            src_item = os.path.join(src_dir, item)
            dest_item = os.path.join(dest_dir, item)
            if os.path.isfile(src_item):
                shutil.copy2(src_item, dest_item)

    def Read_Vcompile(self):
        compile_path = f"./workdir/{self.design_name}/design/vcompile.txt"
        with open(compile_path, "r", encoding = "utf-8") as file:
            self.vcompile = file.read()
    def Read_Vsim(self):
        compile_path = f"./workdir/{self.design_name}/design/vsim.txt"
        with open(compile_path, "r", encoding = "utf-8") as file:
            self.vsim = file.read()
 
