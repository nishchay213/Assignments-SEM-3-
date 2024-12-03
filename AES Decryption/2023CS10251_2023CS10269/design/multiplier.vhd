-- Matrix Flip Module
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity matrix_flip is
    Port ( 
        input_mat : in  STD_LOGIC_VECTOR(127 downto 0);
        output_mat : out STD_LOGIC_VECTOR(127 downto 0)
    );
end matrix_flip;

architecture RTL of matrix_flip is
begin
    process(input_mat)
    begin
        for i in 0 to 3 loop
            for j in 0 to 3 loop
                output_mat((3 - i) * 32 + (3 - j) * 8 + 7 downto (3 - i) * 32 + (3 - j) * 8) <= 
                    input_mat((3 - j) * 32 + (3 - i) * 8 + 7 downto (3 - j) * 32 + (3 - i) * 8);
            end loop;
        end loop;
    end process;
end RTL;

-- Field Multiplication Module
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity field_multiplier is
    Port ( 
        input_byte : in  STD_LOGIC_VECTOR(7 downto 0);
        factor : in  INTEGER range 0 to 15;
        output_byte : out STD_LOGIC_VECTOR(7 downto 0)
    );
end field_multiplier;

architecture RTL of field_multiplier is
    constant FIELD_POLY : std_logic_vector(7 downto 0) := x"1B";
    
    function field_mul_by2(val: std_logic_vector(7 downto 0)) return std_logic_vector is
        variable temp : std_logic_vector(7 downto 0);
    begin
        if val(7) = '0' then
            temp := val(6 downto 0) & '0';
        else
            temp := (val(6 downto 0) & '0') xor FIELD_POLY;
        end if;
        return temp;
    end function;
    
begin
    process(input_byte, factor)
        variable t1, t2, t3 : std_logic_vector(7 downto 0);
    begin
        t1 := field_mul_by2(input_byte);
        t2 := field_mul_by2(t1);
        t3 := field_mul_by2(t2);
        
        case factor is
            when 9 => output_byte <= t3 xor input_byte;
            when 11 => output_byte <= t3 xor t1 xor input_byte;
            when 13 => output_byte <= t3 xor t2 xor input_byte;
            when 14 => output_byte <= t3 xor t2 xor t1;
            when others => output_byte <= input_byte;
        end case;
    end process;
end RTL;

-- Block Transform Module
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity block_transform is
    Port ( 
        input_block : in  STD_LOGIC_VECTOR(31 downto 0);
        output_block : out STD_LOGIC_VECTOR(31 downto 0)
    );
end block_transform;

architecture RTL of block_transform is
    component field_multiplier is
        Port ( 
            input_byte : in  STD_LOGIC_VECTOR(7 downto 0);
            factor : in  INTEGER range 0 to 15;
            output_byte : out STD_LOGIC_VECTOR(7 downto 0)
        );
    end component;
    
    -- Signals for intermediate results
    type byte_array is array (0 to 15) of std_logic_vector(7 downto 0);
    signal mult_results : byte_array;
    
    -- Constants for multiplication factors
    type factor_array is array (0 to 3) of integer range 0 to 15;
    constant MULT0_FACTORS : factor_array := (14, 11, 13, 9);  -- First output byte
    constant MULT1_FACTORS : factor_array := (9, 14, 11, 13);  -- Second output byte
    constant MULT2_FACTORS : factor_array := (13, 9, 14, 11);  -- Third output byte
    constant MULT3_FACTORS : factor_array := (11, 13, 9, 14);  -- Fourth output byte
    
begin
    -- Generate 16 multipliers for all required combinations
    GEN_MULT: for i in 0 to 3 generate
        -- Multipliers for first output byte
        MULT0_X: field_multiplier port map(
            input_byte => input_block(31-i*8 downto 24-i*8),
            factor => MULT0_FACTORS(i),
            output_byte => mult_results(i)
        );
        
        -- Multipliers for second output byte
        MULT1_X: field_multiplier port map(
            input_byte => input_block(31-i*8 downto 24-i*8),
            factor => MULT1_FACTORS(i),
            output_byte => mult_results(4+i)
        );
        
        -- Multipliers for third output byte
        MULT2_X: field_multiplier port map(
            input_byte => input_block(31-i*8 downto 24-i*8),
            factor => MULT2_FACTORS(i),
            output_byte => mult_results(8+i)
        );
        
        -- Multipliers for fourth output byte
        MULT3_X: field_multiplier port map(
            input_byte => input_block(31-i*8 downto 24-i*8),
            factor => MULT3_FACTORS(i),
            output_byte => mult_results(12+i)
        );
    end generate;
    
    -- Combine results
    output_block(31 downto 24) <= mult_results(0) xor mult_results(1) xor mult_results(2) xor mult_results(3);
    output_block(23 downto 16) <= mult_results(4) xor mult_results(5) xor mult_results(6) xor mult_results(7);
    output_block(15 downto 8) <= mult_results(8) xor mult_results(9) xor mult_results(10) xor mult_results(11);
    output_block(7 downto 0) <= mult_results(12) xor mult_results(13) xor mult_results(14) xor mult_results(15);
end RTL;

-- Top Level Module
library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity matrix_inv_transform is
    Port ( 
        clock   : in  STD_LOGIC;
        rst     : in  STD_LOGIC;
        start   : in  STD_LOGIC;
        in_data : in  STD_LOGIC_VECTOR(127 downto 0);
        ready   : out STD_LOGIC;
        result  : out STD_LOGIC_VECTOR(127 downto 0)
    );
end matrix_inv_transform;

architecture RTL of matrix_inv_transform is
    component matrix_flip is
        Port ( 
            input_mat : in  STD_LOGIC_VECTOR(127 downto 0);
            output_mat : out STD_LOGIC_VECTOR(127 downto 0)
        );
    end component;
    
    component block_transform is
        Port ( 
            input_block : in  STD_LOGIC_VECTOR(31 downto 0);
            output_block : out STD_LOGIC_VECTOR(31 downto 0)
        );
    end component;
    
    signal flipped_data, data_reg : std_logic_vector(127 downto 0);
    signal ready_reg : std_logic;
    signal transformed_blocks : std_logic_vector(127 downto 0);
    
begin
    -- Input matrix flip
    FLIP_IN: matrix_flip port map(
        input_mat => in_data,
        output_mat => flipped_data
    );
    
    -- Block transformations
    GEN_BLOCKS: for i in 0 to 3 generate
        BLOCK_X: block_transform port map(
            input_block => flipped_data(127-i*32 downto 96-i*32),
            output_block => transformed_blocks(127-i*32 downto 96-i*32)
        );
    end generate;
    
    -- Output matrix flip
    FLIP_OUT: matrix_flip port map(
        input_mat => data_reg,
        output_mat => result
    );
    
    -- Main process
    process(clock, rst)
    begin
        if rst = '1' then
            data_reg <= (others => '0');
            ready_reg <= '0';
        elsif rising_edge(clock) then
            if start = '1' then
                data_reg <= transformed_blocks;
                ready_reg <= '1';
            else
                ready_reg <= '0';
            end if;
        end if;
    end process;
    
    ready <= ready_reg;
end RTL;