----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 21.10.2024 14:55:44
-- Design Name: 
-- Module Name: inv_MUX - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 4-to-1 Multiplexer for InvShiftRows
-- 
-- Dependencies: 
-- 
-- Revision:
-- Revision 0.01 - File Created
-- Additional Comments:
-- 
----------------------------------------------------------------------------------

library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity inv_MUX is
    Port(
        in0, in1, in2, in3 : in std_logic_vector(7 downto 0);
        sel : in std_logic_vector(1 downto 0);
        y : out std_logic_vector(7 downto 0)
    );
end inv_MUX;

architecture Behavioral of inv_MUX is
begin
    process(in0, in1, in2, in3, sel)
    begin
        case sel is
            when "00" => y <= in0;
            when "01" => y <= in1;
            when "10" => y <= in2;
            when "11" => y <= in3;
            when others => y <= (others => '0'); -- Default to zero
        end case;
    end process;
end Behavioral;
