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

    wire signed [31:0] sa = a;
    wire signed [31:0] sb = b;
    reg [31:0] res;

    integer i;

    always @* begin
        carry = 0;
        overflow = 0;
        case (aluc)
            ADD: begin
                res = sa + sb;
                carry = (sa + sb) > 32'h7FFFFFFF;
                overflow = (sa[31] == sb[31]) && (res[31] != sa[31]);
            end
            ADDU: begin
                res = sa + sb;
                carry = (sa + sb) > 32'hFFFFFFFF;
            end
            SUB: begin
                res = sa - sb;
                carry = sa < sb;
                overflow = (sa[31] != sb[31]) && (res[31] != sa[31]);
            end
            SUBU: begin
                res = sa - sb;
                carry = sa < sb;
            end
            AND: res = sa & sb;
            OR: res = sa | sb;
            XOR: res = sa ^ sb;
            NOR: res = ~(sa | sb);
            SLT: res = sa < sb;
            SLTU: res = sa < sb;
            SLL: res = sa << b;
            SRL: res = sa >> b;
            SRA: begin
                res = sa >> b;
                if (sa[31]) for (i = 31; i >= 31-b; i = i-1) res[i] = 1'b1;
            end
            SLLV: res = sa << a[4:0];
            SRLV: res = sa >> a[4:0];
            SRAV: begin
                res = sa >> a[4:0];
                if (sa[31]) for (i = 31; i >= 31-a[4:0]; i = i-1) res[i] = 1'b1;
            end
            LUI: res = {a[15:0], 16'b0};
            default: res = 32'bz;
        endcase
    end

    always @(res) begin
        r = res;
        flag = (aluc == SLT || aluc == SLTU) ? 1'b1 : 1'bz;
        zero = (r == 0) ? 1'b1 : 1'b0;
        negative = res[31];
    end
endmodule
