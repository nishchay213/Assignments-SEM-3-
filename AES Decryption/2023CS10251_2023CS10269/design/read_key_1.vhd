----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07.11.2024 09:00:49
-- Design Name: 
-- Module Name: read_key_1 - Behavioral
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

entity read_key_1 is
    Port ( 
        clk : in std_logic;
        num_round : in integer range 0 to 10;
        out1 : out std_logic_vector(127 downto 0)
        );
end read_key_1;

architecture Behavioral of read_key_1 is
    
  


begin

    
    gen : for i in 0 to 15 generate
        key_box_inst : entity work.key_box
            port map(
                    clk => clk,
                    num_round => num_round,
                    byte_num => i,
                    out_byte => out1((16 - i)*8 - 1 downto (15 - i)*8)
                    );
    end generate gen;





end Behavioral;
