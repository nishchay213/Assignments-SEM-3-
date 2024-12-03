----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06.11.2024 16:57:33
-- Design Name: 
-- Module Name: add_round_key - Behavioral
-- Project Name: 
-- Target Devices: 
-- Tool Versions: 
-- Description: 
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

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity add_round_key is
  Port ( 
  in1 : in std_logic_vector(127 downto 0);
  in2 : in std_logic_vector(127 downto 0);
  out1 : out std_logic_vector(127 downto 0)
  );
end add_round_key;

architecture Behavioral of add_round_key is

begin
    out1 <= in1 xor in2;


end Behavioral;
