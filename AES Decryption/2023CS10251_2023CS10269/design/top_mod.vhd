library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.STD_LOGIC_ARITH.ALL;
use IEEE.STD_LOGIC_UNSIGNED.ALL;

entity top_mod is
    Port(
        clk : in STD_LOGIC;
        reset : in STD_LOGIC;
        data_in_cipher : in std_logic_vector(127 downto 0);
        top_start : in std_logic;
        round_out : out STD_LOGIC_VECTOR(127 downto 0);
        cur_round : out integer range 0 to 10;
        done : out STD_LOGIC;
        -- Add the state output to track the state
        state : out std_logic_vector(2 downto 0)  -- 3-bit vector to represent 7 states
    );
end top_mod;

architecture Behaviour of top_mod is
    type state_type is (IDLE, LOAD_CIPHER, PROCESS_ROUND, WAIT_FOR_DONE, CHECK_DONE, COMPLETE, FINALIZE);
    signal current_state, next_state : state_type := IDLE;

    -- New signal to track the state changes in simulation
    signal state_tracker : integer range 0 to 6 := 0;

    signal temp_data : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal start : STD_LOGIC := '0';
    signal round_num : integer range 0 to 10 := 0;
    signal data_out : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal cipher_text : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal done_controller : STD_LOGIC := '0';
    signal cycle_counter : integer := 0;
    signal cipher_text_flipped : STD_LOGIC_VECTOR(127 downto 0) := (others => '0');
    signal final_data_flipped : std_logic_vector(127 downto 0) := (others => '0');
    
    component matrix_flip is
        PORT(
            input_mat : in std_logic_vector (127 downto 0);
            output_mat : out std_logic_vector (127 downto 0)
        );
    end component;

    component controller is
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
    end component;

begin
    cipher_flipped : matrix_flip
        Port Map(
            input_mat => data_in_cipher,
            output_mat => cipher_text_flipped
        );
            
    final_flipped : matrix_flip
        Port Map(
            input_mat => data_out,
            output_mat => final_data_flipped
        );

    controller_inst: controller
        Port Map(
            clk => clk,
            reset => reset,
            start => start,
            round_num => round_num,
            data_in => temp_data,
            cur_output_component => open, -- unused here
            data_out => data_out,
            done => done_controller
        );

    process(clk, reset)
    begin
        if reset = '1' then
            current_state <= IDLE;
            state_tracker <= 0;  -- Reset the state tracker
            round_num <= 0;
            temp_data <= (others => '0');
            cycle_counter <= 0;
            start <= '0';
            round_out <= (others => '0');
            done <= '0';
        elsif rising_edge(clk) then
            current_state <= next_state;
            cur_round <= round_num;

            -- Update the state tracker for waveform visibility
            case current_state is
                when IDLE =>
                    state_tracker <= 0;
                    state <= "000"; -- IDLE state
                    if top_start = '1' then
                        start <= '0';
                        cycle_counter <= 0;
                        next_state <= LOAD_CIPHER;
                    end if;

                when LOAD_CIPHER =>
                    state_tracker <= 1;
                    state <= "001"; -- LOAD_CIPHER state
                    temp_data <= cipher_text_flipped;
                    start <= '1';
                    next_state <= PROCESS_ROUND;

                when PROCESS_ROUND =>
                    state_tracker <= 2;
                    state <= "010"; -- PROCESS_ROUND state
                    if cycle_counter = 12 then
                        start <= '0'; -- Stop the signal
                        next_state <= WAIT_FOR_DONE;
                    else
                        cycle_counter <= cycle_counter + 1;
                    end if;

                when WAIT_FOR_DONE =>
                    state_tracker <= 3;
                    state <= "011"; -- WAIT_FOR_DONE state
                    if done_controller = '1' then
                        cycle_counter <= 0;
                        round_num <= round_num + 1;
                        temp_data <= data_out;
                        round_out <= data_out;
                        next_state <= CHECK_DONE;
                    end if;

                when CHECK_DONE =>
                    state_tracker <= 4;
                    state <= "100"; -- CHECK_DONE state
                    if round_num < 10 then
                        start <= '1';
                        next_state <= PROCESS_ROUND;
                    else
                        done <= '1';
                        round_out <= final_data_flipped;
                        start <= '0'; -- Ensure start is set to '0' after completion
                        cycle_counter <= 0;
                        next_state <= FINALIZE;
                    end if;

                when FINALIZE =>
                    state_tracker <= 5;
                    state <= "101"; -- FINALIZE state
                    if cycle_counter = 5 then
                        done <= '0';
                        next_state <= IDLE;
                        round_num <= 0;
                    else
                        cycle_counter <= cycle_counter + 1;
                    end if;

                when COMPLETE =>
                    state_tracker <= 6;
                    state <= "110"; -- COMPLETE state
                    next_state <= COMPLETE;

                when others =>
                    state_tracker <= 0;
                    state <= "000"; -- Default to IDLE
                    next_state <= IDLE;
            end case;
        end if;
    end process;

end Behaviour;
