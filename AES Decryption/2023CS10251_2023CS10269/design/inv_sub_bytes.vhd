----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06.11.2024 17:00:18
-- Design Name: 
-- Module Name: inv_sub_bytes - Behavioral
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

entity inv_sub_bytes is
  Port ( 
  clk : in std_logic;
  in1 : in std_logic_vector(127 downto 0);
  out1 : out std_logic_vector(127 downto 0)
  );
end inv_sub_bytes;

architecture Behavioral of inv_sub_bytes is

begin
    gen : for i in 0 to 15 generate
        inv_sbox_inst : entity work.inv_sbox
            port map(
                    clk => clk,
                    in_byte  => in1((i + 1)*8 - 1 downto i*8),
				    out_byte => out1((i + 1)*8 - 1 downto i*8)
				    );
				 end generate gen; 
            


end Behavioral;
