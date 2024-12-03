----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 07.11.2024 09:29:43
-- Design Name: 
-- Module Name: key_box - Behavioral
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
use IEEE.NUMERIC_STD.ALL; -- Use numeric_std for to_unsigned
-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity key_box is
 Port ( 
        clk : in std_logic;
        num_round : in integer range 0 to 10;
        byte_num : in integer range 0 to 15;
        out_byte : out std_logic_vector(7 downto 0)
        );

end key_box;



architecture Behavioral of key_box is

    component key_rom is
        PORT(
            clka : IN STD_LOGIC;
            addra : IN STD_LOGIC_VECTOR(7 DOWNTO 0);
            douta : OUT STD_LOGIC_VECTOR(7 DOWNTO 0)
        );
    END COMPONENT;
    signal rom_addr : std_logic_vector(7 downto 0);
    signal addr : integer;

begin
    addr <= (9-num_round) * 16 + byte_num;
    rom_addr <= std_logic_vector(to_unsigned(addr, 8));
    rom_inst: key_rom
        PORT MAP (
            clka => clk,
            addra => rom_addr,
            douta => out_byte
        );



end Behavioral;
