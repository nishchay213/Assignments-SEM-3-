library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- 4-to-1 MUX Component Declaration
--entity mux4x1 is
--    port (
--        d0, d1, d2, d3 : in  std_logic_vector(7 downto 0);  -- Data inputs
--        sel             : in  std_logic_vector(1 downto 0);  -- Selector input
--        y               : out std_logic_vector(7 downto 0)   -- MUX output
--    );
--end entity mux4x1;

--architecture behavior of mux4x1 is
--begin
--    process(d0, d1, d2, d3, sel)
--    begin
--        case sel is
--            when "00" => y <= d0;
--            when "01" => y <= d1;
--            when "10" => y <= d2;
--            when "11" => y <= d3;
--            when others => y <= (others => '0');
--        end case;
--    end process;
--end architecture behavior;

-- InvShiftRows Entity Declaration
entity InvShiftRows is
    port (
        input_matrix  : in  std_logic_vector(127 downto 0);  -- 4x4 matrix flattened into 128 bits
        output_matrix : out std_logic_vector(127 downto 0)   -- Flattened output matrix
    );
end entity InvShiftRows;

architecture behavior of InvShiftRows is

    -- Component Declaration for MUX4x1
    component inv_MUX
        port (
            in0, in1, in2, in3 : in  std_logic_vector(7 downto 0);  -- Data inputs
            sel             : in  std_logic_vector(1 downto 0);  -- Selector input
            y               : out std_logic_vector(7 downto 0)   -- MUX output
        );
    end component;

    -- Signals for each row (4 bytes per row)
    signal row0, row1, row2, row3 : std_logic_vector(31 downto 0);

    -- MUX Outputs for each byte
    signal out00, out01, out02, out03 : std_logic_vector(7 downto 0);
    signal out10, out11, out12, out13 : std_logic_vector(7 downto 0);
    signal out20, out21, out22, out23 : std_logic_vector(7 downto 0);
    signal out30, out31, out32, out33 : std_logic_vector(7 downto 0);

begin
    -- Extract rows from the flattened input matrix
    row0 <= input_matrix(127 downto 96);
    row1 <= input_matrix(95 downto 64);
    row2 <= input_matrix(63 downto 32);
    row3 <= input_matrix(31 downto 0);
    mux00: inv_MUX port map(
        in0 => row0(31 downto 24), in1 => row0(23 downto 16),
        in2 => row0(15 downto 8), in3 => row0(7 downto 0),
        sel => "00", y => out00
    );
    mux01: inv_MUX port map(
        in0 => row0(31 downto 24), in1 => row0(23 downto 16),
        in2 => row0(15 downto 8), in3 => row0(7 downto 0),
        sel => "01", y => out01
    );
    mux02: inv_MUX port map(
        in0 => row0(31 downto 24), in1 => row0(23 downto 16),
        in2 => row0(15 downto 8), in3 => row0(7 downto 0),
        sel => "10", y => out02
    );
    mux03: inv_MUX port map(
        in0 => row0(31 downto 24), in1 => row0(23 downto 16),
        in2 => row0(15 downto 8), in3 => row0(7 downto 0),
        sel => "11", y => out03
    );
    -- MUX Instances for Row 1 (Shift 1 byte right)
    mux10: inv_MUX port map(
        in0 => row1(31 downto 24), in1 => row1(23 downto 16),
        in2 => row1(15 downto 8), in3 => row1(7 downto 0),
        sel => "00", y => out11
    );
     mux11: inv_MUX port map(
        in0 => row1(31 downto 24), in1 => row1(23 downto 16),
        in2 => row1(15 downto 8), in3 => row1(7 downto 0),
        sel => "01", y => out12
    );
     mux12: inv_MUX port map(
        in0 => row1(31 downto 24), in1 => row1(23 downto 16),
        in2 => row1(15 downto 8), in3 => row1(7 downto 0),
        sel => "10", y => out13
    );
     mux13: inv_MUX port map(
        in0 => row1(31 downto 24), in1 => row1(23 downto 16),
        in2 => row1(15 downto 8), in3 => row1(7 downto 0),
        sel => "11", y => out10
    );

    -- MUX Instances for Row 2 (Shift 2 bytes right)
    mux20: inv_MUX port map(
        in0 => row2(31 downto 24), in1 => row2(23 downto 16),
        in2 => row2(15 downto 8), in3 => row2(7 downto 0),
        sel => "00", y => out22
    );
    mux21: inv_MUX port map(
        in0 => row2(31 downto 24), in1 => row2(23 downto 16),
        in2 => row2(15 downto 8), in3 => row2(7 downto 0),
        sel => "01", y => out23
    );
    mux22: inv_MUX port map(
        in0 => row2(31 downto 24), in1 => row2(23 downto 16),
        in2 => row2(15 downto 8), in3 => row2(7 downto 0),
        sel => "10", y => out20
    );
    mux23: inv_MUX port map(
        in0 => row2(31 downto 24), in1 => row2(23 downto 16),
        in2 => row2(15 downto 8), in3 => row2(7 downto 0),
        sel => "11", y => out21
    );

    -- MUX Instances for Row 3 (Shift 3 bytes right)
    mux30: inv_MUX port map(
        in0 => row3(31 downto 24), in1 => row3(23 downto 16),
        in2 => row3(15 downto 8), in3 => row3(7 downto 0),
        sel => "00", y => out33
    );
    mux31: inv_MUX port map(
        in0 => row3(31 downto 24), in1 => row3(23 downto 16),
        in2 => row3(15 downto 8), in3 => row3(7 downto 0),
        sel => "01", y => out30
    );
    mux32: inv_MUX port map(
        in0 => row3(31 downto 24), in1 => row3(23 downto 16),
        in2 => row3(15 downto 8), in3 => row3(7 downto 0),
        sel => "10", y => out31
    );
    mux33: inv_MUX port map(
        in0 => row3(31 downto 24), in1 => row3(23 downto 16),
        in2 => row3(15 downto 8), in3 => row3(7 downto 0),
        sel => "11", y => out32
    );
    -- Concatenate all MUX outputs into the final output matrix
    output_matrix <= out00 & out01 & out02 & out03 &
                     out10 & out11 & out12 & out13 &
                     out20 & out21 & out22 & out23 &
                     out30 & out31 & out32 & out33;
end architecture behavior;
