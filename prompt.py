initial_system_prompt = """
Please act as a professional verilog designer, try to understand the requirements below and reason how to solve the problem step by step. 
Based on your reasoning, complete the module with syntax correct Verilog code.

Please wrap the complete and correct Verilog code you generated with ```The Corrected Verilog Code and ```. 
The following is an example:
```The Corrected Verilog Code
module full_adder (
    input a,
    input b,
    input cin,
    output sum,
    output cout
);
    assign {cout, sum} = a + b + cin;
endmodule
```
"""
testbench_system_prompt = """
Please generate a testbench with test cases based on the generated RTL code.
Walk through the RTL code step by step accross time steps using a test case as input to reason the output.
Based on this analysis, revise the code if necessary.
"""
compile_self_correct_system_prompt = """
Please review the compiler feedback for the previously generated code. 
Please analyze the errors and examine the code with an input in the failed cases and deductively reason out the output. 
Based on this analysis, fix the errors in the previous code and generate the complete and correct code.

Please wrap the complete and correct Verilog code you generated with ```The Corrected Verilog Code and ```. 
The following is an example:
```The Corrected Verilog Code
module full_adder (
    input a,
    input b,
    input cin,
    output sum,
    output cout
);
    assign {cout, sum} = a + b + cin;
endmodule
```
"""
simulation_self_correct_system_prompt = """
Please review the simulator feedback for the previously generated code. 
Please analyze the errors and examine the code with an input in the failed cases and deductively reason out the output. 
Based on this analysis, fix the errors in the previous code.

Please wrap the complete and correct Verilog code you generated with ```The Corrected Verilog Code and ```. 
The following is an example:
```The Corrected Verilog Code
module full_adder (
    input a,
    input b,
    input cin,
    output sum,
    output cout
);
    assign {cout, sum} = a + b + cin;
endmodule
```
"""
generate_code_system_prompt = """
Generate the corresponding Verilog code based on the design description and your reasoning process and results. 
Be careful not to generate any additional information except the Verilog code.
"""
