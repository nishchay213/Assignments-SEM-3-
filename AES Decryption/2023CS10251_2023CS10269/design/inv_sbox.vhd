----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 06.11.2024 17:01:18
-- Design Name: 
-- Module Name: inv_sbox - Behavioral
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

entity inv_sbox is
  Port ( 
  clk : in std_logic;
  in_byte : in std_logic_vector(7 downto 0);
  out_byte : out std_logic_vector(7 downto 0)
  );
end inv_sbox;

architecture Behavioral of inv_sbox is
component inv_sbox_rom
 PORT(
      clka : IN STD_LOGIC;
      addra : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
      douta : OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
    );
  END COMPONENT;
  signal rom_addr : std_logic_vector(7 downto 0);
  
begin
rom_inst: inv_sbox_rom
    PORT MAP (
      clka => clk,
      addra => in_byte,
      douta => out_byte
    );






end Behavioral;
