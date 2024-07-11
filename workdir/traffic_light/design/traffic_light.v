module traffic_light (
    input wire rst_n,
    input wire clk,
    input wire pass_request,
    output wire [7:0] clock, // Changed from reg to wire
    output reg red,
    output reg yellow,
    output reg green
);

    parameter idle = 2'b00, s1_red = 2'b01, s2_yellow = 2'b10, s3_green = 2'b11;
    reg [7:0] cnt;
    reg [1:0] state;
    reg p_red, p_yellow, p_green;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            state <= idle;
            cnt <= 8'b00000000;
        end else begin
            case (state)
                idle: begin
                    if (rst_n) begin
                        state <= s1_red;
                        cnt <= 8'b00001010;
                    end
                end
                s1_red: begin
                    if (cnt == 8'b00000000 || pass_request) begin
                        state <= s3_green;
                        cnt <= 8'b00111100;
                    end else begin
                        cnt <= cnt - 1;
                    end
                end
                s2_yellow: begin
                    if (cnt == 8'b00000000 || pass_request) begin
                        state <= s3_green;
                        cnt <= 8'b00111100;
                    end else begin
                        cnt <= cnt - 1;
                    end
                end
                s3_green: begin
                    if (cnt == 8'b00000000) begin
                        state <= s2_yellow;
                        cnt <= 8'b00000101;
                    end else if (pass_request && cnt > 8'b00001010) begin
                        cnt <= 8'b00001010;
                    end else begin
                        cnt <= cnt - 1;
                    end
                end
            endcase
        end
    end

    assign clock = cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            red <= 0;
            yellow <= 0;
            green <= 0;
        end else begin
            red <= p_red;
            yellow <= p_yellow;
            green <= p_green;
        end
    end
endmodule
