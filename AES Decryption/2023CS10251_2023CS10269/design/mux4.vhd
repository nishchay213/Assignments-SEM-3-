library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity mux4 is
--  Port ( );
Port (
A : in std_logic_vector (7 downto 0);
B: in std_logic_vector (7 downto 0);
C: in std_logic_vector (7 downto 0);
D: in std_logic_vector (7 downto 0);
Sel : in std_logic_vector (1 downto 0);
Y : out std_logic_vector (7 downto 0)
); 
end mux4;

architecture Behavioral of mux4 is

begin
process(A,B,C,D,Sel)
begin
    case Sel is
        when "00" => Y<=A;
        when "01" => Y<=B;
        when "10" => Y<=C;
        when "11" => Y<=D;
        when others => Y<="00001111";
    end case;
end process;

end Behavioral;