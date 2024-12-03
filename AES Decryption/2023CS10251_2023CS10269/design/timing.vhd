library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL; -- Use this for arithmetic operations

entity timing is
    Port (
        clk_in : in STD_LOGIC; -- 100 MHz input clock
        reset : in STD_LOGIC; -- Reset signal
        mux_select : out STD_LOGIC_VECTOR (1 downto 0); -- Signal for the mux
        anodes : out STD_LOGIC_VECTOR (3 downto 0) -- Anodes signal for display
    );
end timing;

architecture Behavioral of timing is
    constant N : integer := 50000; -- Adjusted for 1 kHz clock
    signal counter: integer := 0;
    signal new_clk : STD_LOGIC := '0';
    signal anode_count : integer := 0; -- Change to integer
    signal mux_select_int : STD_LOGIC_VECTOR (1 downto 0); -- Internal signal for mux_select
begin

    -- Process 1 for dividing the clock from 100 MHz to 1 kHz
    clk_new: process(clk_in, reset)
    begin
        if reset = '1' then
            counter <= 0;
            new_clk <= '0';
        elsif rising_edge(clk_in) then
            if counter = (N - 1) then
                counter <= 0;
                new_clk <= not new_clk;
            else
                counter <= counter + 1;
            end if;
        end if;
    end process;

    -- Process 2 for mux select signal
    select_mux: process(new_clk, reset)
    begin
        if reset = '1' then
            anode_count <= 0;
        elsif rising_edge(new_clk) then
            anode_count <= (anode_count + 1) mod 4; 
        end if;
    end process;

       mux_select_int <= std_logic_vector(to_unsigned(anode_count, mux_select_int'length));
    mux_select <= mux_select_int;

    -- Process 3 for anode signal
    ANODE_select: process(mux_select_int)
    begin
        case mux_select_int is 
            when "00" => anodes <= "1110";
            when "01" => anodes <= "1101";
            when "10" => anodes <= "1011";
            when "11" => anodes <= "0111";
            when others => anodes <= "1111";
        end case;
    end process;

end Behavioral;