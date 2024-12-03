library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity controller is
    Port(
        clk : in STD_LOGIC;
        reset : in STD_LOGIC;
        start : in STD_LOGIC;
        
        round_num : in integer range 0 to 10;
        data_in : in STD_LOGIC_VECTOR(127 downto 0);
        cur_output_component : out STD_LOGIC_VECTOR(127 downto 0);
        data_out : out STD_LOGIC_VECTOR(127 downto 0);
        done : out STD_LOGIC
    );
end controller;

architecture Behavioral of controller is
    -- State signals
    signal state : integer range 0 to 10 := 0;
    signal num_round : integer range 0 to 10 := 0;
    
    -- Data path signals
    signal temp_data : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal temp_key : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal temp_out_add_round : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal temp_out_multiplier : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal temp_in_inv_shift_rows : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal temp_out_inv_shift_rows : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal temp_out_inv_sub_bytes : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    
    -- Control signals
    signal sub_bytes_delay : integer range 0 to 2 := 0;
    signal read_key_1_delay : integer range 0 to 6 := 0;
    signal multi_delay : integer range 0 to 2 := 0;
    signal inv_shift_rows_delay : integer range 0 to 2 := 0;
    signal reg_temp_delay : integer range 0 to 2 := 0;
    signal always_one : STD_LOGIC := '1';
    signal always_zero : STD_LOGIC := '0';
    signal buffer_for_multiplier_done : STD_LOGIC := '0';
    signal flipped_key : std_logic_vector(127 downto 0);
    
    -- Component declarations (unchanged)
    
    component matrix_flip is
        PORT(
            input_mat : in std_logic_vector (127 downto 0);
            output_mat : out std_logic_vector (127 downto 0)
            );
            end component;
  
    component add_round_key
        Port ( in1 : in STD_LOGIC_VECTOR(127 downto 0);
               in2 : in STD_LOGIC_VECTOR(127 downto 0);
               out1 : out STD_LOGIC_VECTOR(127 downto 0));
    end component;

    component invshiftrows
        Port ( input_matrix : in STD_LOGIC_VECTOR(127 downto 0);
               output_matrix : out STD_LOGIC_VECTOR(127 downto 0));
    end component;

    component inv_sub_bytes
        Port ( 
            clk : in STD_LOGIC;
            in1 : in STD_LOGIC_VECTOR(127 downto 0);
            out1 : out STD_LOGIC_VECTOR(127 downto 0));
    end component;

    component matrix_inv_transform
        Port(
            clock   : in  STD_LOGIC;
            rst     : in  STD_LOGIC;
            start   : in  STD_LOGIC;
            in_data : in  STD_LOGIC_VECTOR(127 downto 0);
            ready   : out STD_LOGIC;
            result  : out STD_LOGIC_VECTOR(127 downto 0)
        );
    end component;

    component read_key_1
        Port ( 
            clk : in STD_LOGIC;
            num_round : in integer range 0 to 10;
            out1 : out STD_LOGIC_VECTOR(127 downto 0));
    end component;

begin
    -- Component instantiations (unchanged)
    
    flipper_inst : matrix_flip
        port map (
            input_mat => temp_key,
            output_mat => flipped_key
            );
    
    read_key_1_inst: read_key_1
        Port Map(
            clk => clk,
            num_round => num_round,
            out1 => temp_key
        );
    
    add_round_key_inst: add_round_key
        Port Map(
            in1 => temp_data,  -- Now correctly connected to temp_data
            in2 => flipped_key,
            out1 => temp_out_add_round
        );

    matrix_inv_trans_inst : matrix_inv_transform
        Port Map(
            clock => clk,
            rst => always_zero,
            start => always_one,
            in_data => temp_out_add_round,
            ready => buffer_for_multiplier_done,
            result => temp_out_multiplier
        );
    
    inv_shift_rows_inst: invshiftrows
        Port Map(
            input_matrix => temp_in_inv_shift_rows,
            output_matrix => temp_out_inv_shift_rows
        );

    inv_sub_bytes_inst: inv_sub_bytes
        Port Map(
            clk => clk,
            in1 => temp_out_inv_shift_rows,
            out1 => temp_out_inv_sub_bytes
        );

    process(clk, reset)
    begin
        if reset = '1' then
            state <= 0;
            num_round <= 0;
            done <= '0';
            temp_data <= (others => '0');
            sub_bytes_delay <= 0;
            read_key_1_delay <= 0;
            multi_delay <= 0;
            inv_shift_rows_delay <= 0;
            reg_temp_delay <= 0;
            
        elsif rising_edge(clk) then
            case state is
                when 0 =>  -- Initial state
                    if start = '1' then
                        temp_data <= data_in;  -- Store input data
                        num_round <= round_num;
                        state <= 1;
                    end if;
                    
                when 1 =>  -- Wait for key generation
                    if read_key_1_delay = 6 then
                        read_key_1_delay <= 0;
                        cur_output_component <= temp_key;
                        state <= 2;
                    else
                        read_key_1_delay <= read_key_1_delay + 1;
                    end if;
                    
                when 2 =>  -- Matrix multiplication
                    if multi_delay = 2 then
                        multi_delay <= 0;
                        cur_output_component <= temp_out_multiplier;
                        if num_round = 0 then
                            temp_in_inv_shift_rows <= temp_out_add_round;
                        else
                            temp_in_inv_shift_rows <= temp_out_multiplier;
                        end if;
                          -- Direct connection
                        state <= 3;
                    else
                        multi_delay <= multi_delay + 1;
                        cur_output_component <= temp_out_add_round;
                    end if;
                    
                when 3 =>  -- Prepare for inverse shift rows
                    state <= 4;
                    
                when 4 =>  -- Inverse shift rows
                    if inv_shift_rows_delay = 2 then
                        inv_shift_rows_delay <= 0;
                        cur_output_component <= temp_out_inv_shift_rows;
                        state <= 5;
                    else
                        inv_shift_rows_delay <= inv_shift_rows_delay + 1;
                    end if;
                    
                when 5 =>  -- Inverse sub bytes
                    if sub_bytes_delay = 2 then
                        sub_bytes_delay <= 0;
                        cur_output_component <= temp_out_inv_sub_bytes;
                        state <= 6;
                    else
                        sub_bytes_delay <= sub_bytes_delay + 1;
                    end if;
                    
                when 6 =>  -- Output result
                    if num_round = 9 then
                        data_out <= temp_out_add_round;

                    else
                        data_out <= temp_out_inv_sub_bytes;
                    end if;
                    
                    state <= 7;
                    
                when 7 =>  -- Final delay
                    if reg_temp_delay = 2 then
                        reg_temp_delay <= 0;
                        state <= 8;
                    else
                        reg_temp_delay <= reg_temp_delay + 1;
                    end if;
                    
                when 8 =>  -- Set done flag
                    done <= '1';
                    
                    state <= 9;
                    
                when 9 =>  -- Wait for start to go low
                    if start = '0' then
                        state <= 0;
                        done <= '0';
                    end if;
                    
                when others =>
                    state <= 0;
            end case;
        end if;
    end process;
    
end Behavioral;