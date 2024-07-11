import os
from model import ChatModel

system_code_prompt = """
Please act as a professional verilog designer.
"""

user_code_prompt = """
Implement a traffic light, with red, yellow and green three small indicators and a pedestrian button, under normal circumstances, the motor vehicle lane indicator light according to 60 clock cycles of green, 5 clock cycles of yellow, 10 clock cycles of red. When the pedestrian button is pressed, if the remaining green time is greater than 10 clocks, it is shortened to 10 clocks, and if it is less than 10 clocks, it remains unchanged. The lane light and the sidewalk light should be paired, when the lane light is green or yellow, the sidewalk light is red; When the lane light is red, the sidewalk light is green, and for the sake of simplicity, only the lane light is considered.
Module name:  
    traffic_light
Inputs:
    rst_n: Reset signal (active low).
    clk: Clock signal.
    pass_request: Request signal for allowing vehicles to pass.
Outputs:
    clock[7:0]: An 8-bit output representing the count value of the internal counter.
    red, yellow, green: Output signals representing the state of the traffic lights.
Parameters:
    idle, s1_red, s2_yellow, s3_green: Enumeration values representing different states of the traffic light controller.
Registers and Wires:
    cnt: A 8-bit register used as an internal counter for timing purposes.
    state: A 2-bit register representing the current state of the traffic light controller.
    p_red, p_yellow, p_green: 1-bit registers representing the next values for the red, yellow, and green signals.
Implementation:
The following is the design track we recommend:
The first always block is responsible for the state transition logic. It uses a case statement to handle different states. Here's a summary of each state:
idle: Initial state where all signals are set to 0. Transition to s1_red state occurs immediately.
s1_red: Sets the red signal to 1 and waits for a count of 3 before transitioning to s3_green state. Otherwise, it remains in s1_red state.
s2_yellow: Sets the yellow signal to 1 and waits for a count of 3 before transitioning to s1_red state. Otherwise, it remains in s2_yellow state.
s3_green: Sets the green signal to 1 and waits for a count of 3 before transitioning to s2_yellow state. Otherwise, it remains in s3_green state.
The second always block handles the counting logic of the internal counter (cnt). The counter is decremented by 1 on every positive edge of the clock or negative edge of the reset signal. The counter values are adjusted based on various conditions:
If (!rst_n), the counter is set to 10.
If the pass_request signal is active and the green signal is active, the counter is set to 10.
If the green signal is inactive and the previous green signal (p_green) was active, the counter is set to 60.
If the yellow signal is inactive and the previous yellow signal (p_yellow) was active, the counter is set to 5.
If the red signal is inactive and the previous red signal (p_red) was active, the counter is set to 10.
Otherwise, the counter is decremented normally.
The assign statement assigns the value of the internal counter (cnt) to the output clock.
The final always block handles the output signals. It assigns the previous values (p_red, p_yellow, p_green) to the output signals (red, yellow, green) on the positive edge of the clock or negative edge of the reset signal.

Give me the complete code.
"""
system_testbench_prompt = """
Please act as a professional verilog designer.
"""
user_testbench_prompt = """
Please generate a testbench with test cases based on the generated RTL code. 
Walk through the RTL code step by step across time steps using a test case as input to reason the output. 
Based on this analysis, revise the code if necessary.
the generated RTL code is following:
```verilog
module alu (
    input [31:0] a,
    input [31:0] b,
    input [5:0] aluc,
    output reg [31:0] r,
    output reg zero,
    output reg carry,
    output reg negative,
    output reg overflow,
    output reg flag
);

    parameter ADD = 6'b100000;
    parameter ADDU = 6'b100001;
    parameter SUB = 6'b100010;
    parameter SUBU = 6'b100011;
    parameter AND = 6'b100100;
    parameter OR = 6'b100101;
    parameter XOR = 6'b100110;
    parameter NOR = 6'b100111;
    parameter SLT = 6'b101010;
    parameter SLTU = 6'b101011;
    parameter SLL = 6'b000000;
    parameter SRL = 6'b000010;
    parameter SRA = 6'b000011;
    parameter SLLV = 6'b000100;
    parameter SRLV = 6'b000110;
    parameter SRAV = 6'b000111;
    parameter LUI = 6'b001111;

    wire [31:0] sa = $signed(a);
    wire [31:0] sb = $signed(b);
    reg [33:0] res;

   always @* begin
        case (aluc)
            ADD: res = {2'b00, sa + sb};
            ADDU: res = {2'b00, a + b};
            SUB: res = {2'b00, sa - sb};
            SUBU: res = {2'b00, a - b};
            AND: res = {2'b00, a & b};
            OR: res = {2'b00, a | b};
            XOR: res = {2'b00, a ^ b};
            NOR: res = {2'b00, ~ (a | b)};
            SLT: res = {2'b00, sa < sb};
            SLTU: res = {2'b00, a < b};
            SLL: res = {2'b00, a << b[4:0]};
            SRL: res = {2'b00, a >>> b[4:0]};
            SRA: res = {2'b00, sa >>> b[4:0]}; // Corrected here
            SLLV: res = {2'b00, a << sb[4:0]};
            SRLV: res = {2'b00, a >>> sb[4:0]};
            SRAV: res = {2'b00, sa >>> sb[4:0]}; // Corrected here
            LUI: res = {2'b00, a << 16};
            default: res = 34'bz;
        endcase
    end
    always @* begin
        r = res[31:0];
        zero = (r == 0);
        carry = res[32];
        negative = r[31];
        overflow = res[33];
        flag = (aluc == SLT || aluc == SLTU) ? 1'b1 : 1'bz;
    end
endmodule
```
"""

output = """
Here is a simple testbench for the given RTL code. This testbench will test the ADD operation of the ALU.

```verilog
`timescale 1ns / 1ps

module alu_tb;
    reg [31:0] a;
    reg [31:0] b;
    reg [5:0] aluc;
    wire [31:0] r;
    wire zero;
    wire carry;
    wire negative;
    wire overflow;
    wire flag;

    alu u1 (
        .a(a),
        .b(b),
        .aluc(aluc),
        .r(r),
        .zero(zero),
        .carry(carry),
        .negative(negative),
        .overflow(overflow),
        .flag(flag)
    );

    initial begin
        // Test case for ADD operation
        a = 32'h00000001;
        b = 32'h00000001;
        aluc = 6'b100000; // ADD operation
        #10;
        if (r == 2 && zero == 0 && carry == 0 && negative == 0 && overflow == 0 && flag == 0)
            $display("Test case for ADD operation passed");
        else
            $display("Test case for ADD operation failed");
        $finish;
    end
endmodule
```

In this testbench, we are testing the ADD operation of the ALU. 
We are giving `a` and `b` as 1 and selecting the ADD operation by setting `aluc` to `6'b100000`.
After a delay of 10 time units, we are checking the output.
The result `r` should be 2 as we are adding 1 and 1. 
The `zero` flag should be 0 as the result is not zero. 
The `carry`, `negative`, `overflow`, and `flag` should also be 0 as there is no carry,
 the result is not negative, there is no overflow, and the operation is not SLT or SLTU. 
 If all these conditions are met, the test case is considered passed, otherwise it is considered failed.
"""
if __name__ == "__main__":
    llm = ChatModel(model_name = "gpt-4")
    messages = [
        {"role":"system", "content" : system_testbench_prompt},
        {"role":"user", "content": user_testbench_prompt}
    ] 
    response = llm.generate(messages)
    print(response)