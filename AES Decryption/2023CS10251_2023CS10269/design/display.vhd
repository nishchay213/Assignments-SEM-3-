library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity final is
  Port ( 
         clk_in : in std_logic;
         reset : in std_logic;
         data_in : in std_logic_vector (31 downto 0);
         out_anodes : out std_logic_vector (3 downto 0);
         segment : out std_logic_vector (6 downto 0)
         );
end final;

architecture Behavioral of final is
  component mux4 is
    Port( 
         A : in std_logic_vector (7 downto 0);
         B : in std_logic_vector (7 downto 0);
         C : in std_logic_vector (7 downto 0);
         D : in std_logic_vector (7 downto 0);
         Sel : in std_logic_vector (1 downto 0);
         Y : out std_logic_vector (7 downto 0)
        );
  end component;

  component hex_to_7seg is
    Port(
         input : in std_logic_vector(7 downto 0);
         segments : out std_logic_vector(6 downto 0)
        );
  end component;

  component timing is
    Port (
         clk_in : in std_logic;
         reset : in std_logic;
         mux_select : out std_logic_vector (1 downto 0);
         anodes : out std_logic_vector (3 downto 0)
        );
  end component;

  signal m1 : std_logic_vector (7 downto 0);
  signal m2 : std_logic_vector (1 downto 0);

begin
  DUT2 : timing port map(
         clk_in => clk_in,
         reset => reset,
         mux_select => m2,
         anodes => out_anodes);
  DUT1 : mux4 port map(
         D => data_in(31 downto 24),
         C => data_in(23 downto 16),
         B => data_in(15 downto 8),
         A => data_in(7 downto 0),
         Sel => m2,
         Y => m1);
  DUT3 : hex_to_7seg port map(
         input => m1,
         segments => segment);
end Behavioral;