----------------------------------------------------------------------------------
-- Company: 
-- Engineer: 
-- 
-- Create Date: 09.11.2024 00:47:18
-- Design Name: 
-- Module Name: final_top_mod - Behavioral
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
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if using
-- arithmetic functions with Signed or Unsigned values
--use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity final_top_mod is
 Port ( 
    clk : in std_logic;
    reset : in std_logic;
    anode : out std_logic_vector(3 downto 0);
    seg : out std_logic_vector(6 downto 0);
    scroll_counter_display : out integer;
    display_data_out : out std_logic_vector(31 downto 0);
    cipher_dis : out std_logic_vector(127 downto 0);
    decr_dis : out std_logic_vector(127 downto 0);
    ram_out_dis : out std_logic_vector(7 downto 0);
    ram_out_128_dis : out std_logic_vector(127 downto 0);
    ram_in_dis : out std_logic_vector(7 downto 0);
    first_byte_dis : out std_logic_vector(7 downto 0);
    done : out std_logic

 );
end final_top_mod;

architecture Behavioral of final_top_mod is

    component final is
        Port (
            clk_in : in std_logic;
            reset : in std_logic;
            data_in : in std_logic_vector(31 downto 0);
            out_anodes : out std_logic_vector(3 downto 0);
            segment : out std_logic_vector(6 downto 0)
        );
    end component;



    component top_mod is
        Port (
            clk : in STD_LOGIC;
        reset : in STD_LOGIC;
        data_in_cipher : in std_logic_vector(127 downto 0);
        top_start : in std_logic;
        round_out : out STD_LOGIC_VECTOR(127 downto 0);
        cur_round : out integer range 0 to 10;
        done : out STD_LOGIC;
        state : out std_logic_vector(2 downto 0)
        );
    end component;

    component multiple128_rom is
        Port (
            clka : in STD_LOGIC;
            addra : in STD_LOGIC_VECTOR(4 downto 0);
            douta : out STD_LOGIC_VECTOR(7 downto 0)
        );
    end component;

    component blk_mem_gen_1 is
        Port (
            clka : in STD_LOGIC;
            wea : in STD_LOGIC;
            addra : in STD_LOGIC_VECTOR(4 downto 0);
            dina : in STD_LOGIC_VECTOR(7 downto 0);
            douta : out STD_LOGIC_VECTOR(7 downto 0)
        );
    end component;

    signal top_start : std_logic;
    signal cipher_128 : std_logic_vector(127 downto 0) := (others => '0');
    signal out_128 : std_logic_vector(127 downto 0) := (others => '0');
    signal multiple_128 : integer;
    signal rom_addr : std_logic_vector(4 downto 0);
    signal ram_addr : std_logic_vector(4 downto 0) := (others => '0');
    signal ram_data : std_logic_vector(7 downto 0);
    signal ram_we : std_logic;
    signal ram_out : std_logic_vector(7 downto 0);
    signal state_top_mod : std_logic_vector(2 downto 0);
    signal all_done : std_logic := '0';
    type state_type is (IDLE, LOAD_128, PROCESS_128, WAIT_FOR_DONE, WRITE_128, READ_FROM_RAM, COMPLETE, display_stage);
    signal current_state, next_state : state_type := IDLE;
    signal done_top_mod : std_logic := '0';
    signal rom_out : std_logic_vector(7 downto 0);
    signal always_zero : std_logic := '0';
    signal cycleCounter : integer := 0;
    signal rom_read_wait : integer := 0;
    signal curr_byte_rom : integer := 0;
    signal curr_byte_ram : integer := 0;
    signal process_128_wait : integer := 0;
    signal ram_write_wait : integer := 0;
    signal ram_out_128 : std_logic_vector(127 downto 0) := (others => '0');
    signal ram_read_wait : integer := 0;
    signal display_data : std_logic_vector(31 downto 0) := (others => '0');
    signal scroll_counter : integer := 0;
    signal counter : integer := 0;
    signal next_counter : integer := 0;
    signal first_byte : std_logic_vector(7 downto 0) := (others => '0');
    



    


begin

    display_final_inst : final
        PORT map (
            clk_in => clk,
            reset => always_zero,
            data_in => display_data,
            out_anodes => anode,
            segment => seg
        );


    top_mod_inst: top_mod
        PORT map (
            clk => clk,
            reset => always_zero,
            data_in_cipher => cipher_128,
            top_start => top_start,
            round_out => out_128,
            cur_round => open,
            done => done_top_mod,
            state => state_top_mod
        );
    
    multiple128_rom_inst: multiple128_rom
        PORT map (
            clka => clk,
            addra => rom_addr,
            douta => rom_out
        );
    
    multiple128_ram_inst: blk_mem_gen_1
        PORT map (
            clka => clk,
            wea => ram_we,
            addra => ram_addr,
            dina => ram_data,
            douta => ram_out
        );

        cipher_dis <= cipher_128;
        decr_dis <= out_128;
        ram_out_dis <= ram_out;
        ram_out_128_dis <= ram_out_128;
        ram_in_dis <= ram_data;
        display_data_out <= display_data;
        scroll_counter_display <= scroll_counter;
        first_byte_dis <= first_byte;



            -- process(counter, ram_addr) 
            -- begin
            --     if all_done = '1' then
                
            --    -- next_counter <= counter;  -- Default assignment
                
            --     -- Counter logic
            --     if counter = 0 then
                        
            --          --   next_counter <= counter + 1;
            --     elsif counter = 4 then
            --         display_data <= display_data(23 downto 0) & ram_data;
            --        -- next_counter <= 0;  -- Reset counter after data shift
            --     elsif counter < 4 then
            --        -- next_counter <= counter + 1;
            --     end if;
            --     end if;
            -- end process;
        
    process(clk, reset)
    begin
        if reset = '1' then
            counter <= 0;
        scroll_counter <= 0;
        next_counter <= 0;
            current_state <= IDLE;
            cycleCounter <= 0;
            rom_read_wait <= 0;
            curr_byte_rom <= 0;
            curr_byte_ram <= 0;
            process_128_wait <= 0;
            done <= '0';
            multiple_128 <= 0;
            ram_read_wait <= 0;
            ram_write_wait <= 0;
        elsif rising_edge(clk) then
            current_state <= next_state;

            case current_state is
                when IDLE =>
                    next_state <= LOAD_128;
                    rom_addr <= (others => '0');
                    curr_byte_rom <= 0;
                    rom_read_wait <= 0;

                when LOAD_128 =>
                    if multiple_128 = 0 then

                    if rom_read_wait = 6 then
                        rom_addr <= std_logic_vector(to_unsigned(16*multiple_128 +curr_byte_rom, 5));
                        
                        
                        
                        
                        
                    end if;
                        
                    if rom_read_wait = 2 then
                        if curr_byte_rom < 16 then
                            cipher_128((16-curr_byte_rom)*8 - 1 downto (15-curr_byte_rom)*8) <= rom_out;
                            curr_byte_rom <= curr_byte_rom + 1;
                            
                        end if;

                        
                        if curr_byte_rom = 16 then
                            next_state <= PROCESS_128;
                            top_start <= '1';
                            rom_read_wait <= 0;
                            curr_byte_rom <= 0;
                            rom_addr <= (others => '0');
                        else
                            
                            
                            rom_read_wait <= 0;
                            next_state <= LOAD_128;
                        end if;
                        
                        
                    end if;
                    end if;

                    if multiple_128 > 0 then
                        if rom_read_wait = 2 then
                            rom_addr <= std_logic_vector(to_unsigned(16*multiple_128 +curr_byte_rom, 5));
                            
                            
                            
                            
                            
                        end if;
                            
                        if rom_read_wait = 6 then
                            if curr_byte_rom < 16 then
                                cipher_128((16-curr_byte_rom)*8 - 1 downto (15-curr_byte_rom)*8) <= rom_out;
                                curr_byte_rom <= curr_byte_rom + 1;
                                
                            end if;
    
                            
                            if curr_byte_rom = 16 then
                                next_state <= PROCESS_128;
                                
                                top_start <= '1';
                                rom_read_wait <= 0;
                                curr_byte_rom <= 0;
                                rom_addr <= (others => '0');
                            else
                                
                                
                                rom_read_wait <= 0;
                                next_state <= LOAD_128;
                            end if;
                            
                            
                        end if;
                        end if;


                    rom_read_wait <= (rom_read_wait + 1) mod 8;
                when process_128 =>
                        if process_128_wait = 300 then
                            next_state <= WAIT_FOR_DONE;
                            ram_addr <= (others => '0');
                            top_start <= '0';
                            
                            process_128_wait <= 0;
                            ram_we <= '1';
                        else
                            process_128_wait <= process_128_wait + 1;
                        end if;
                when WAIT_FOR_DONE =>
                        if done_top_mod = '1' then
                            if multiple_128 = 0 then
                                first_byte <= out_128(127 downto 120);
                            end if;

                            next_state <= WRITE_128;
                        end if;
                when WRITE_128 =>
                        
                        if ram_write_wait = 4 then
                            if curr_byte_ram < 16 then
                            ram_addr <= std_logic_vector(to_unsigned(16*multiple_128 + curr_byte_ram, 5));
                            ram_data <= out_128((16-curr_byte_ram)*8 - 1 downto (15-curr_byte_ram)*8);

                            -- else
                            -- ram_we <= '0';
                                
                            -- curr_byte_ram <= 0;
                            -- ram_addr <= (others => '0');
                            -- ram_write_wait <= 0;
                            -- multiple_128 <= multiple_128 + 1;
                            -- if multiple_128 = 1 then
                            --     next_state <= COMPLETE;
                            -- else
                            --     next_state <= IDLE;
                            -- end if;
                            end if;

                        end if;
                        if ram_write_wait = 2 then

                            curr_byte_ram <= curr_byte_ram + 1;
                            if curr_byte_ram = 16 then
                                ram_we <= '0';
                                
                                curr_byte_ram <= 0;
                                ram_addr <= (others => '0');
                                ram_write_wait <= 0;
                                multiple_128 <= multiple_128 + 1;
                                if multiple_128 = 1 then
                                    next_state <= COMPLETE;
                                else
                                    next_state <= IDLE;
                                end if;
                            else
                                next_state <= WRITE_128;
                            end if;
                        end if;
                
                
                
                
                        

                        
                        ram_write_wait <= (ram_write_wait + 1) mod 6;



                
                
                when COMPLETE =>
                        done <= '1';
                            all_done <= '1';
                        ram_addr <= (others => '0');
                        next_state <= display_stage;
                when display_stage =>
                
                if scroll_counter = 1000 then
                    scroll_counter <= 0;
                    if counter = 0 then
                       
                        counter <= counter + 1;
                    elsif counter = 4 then 
                    if unsigned(ram_addr) = 31 then
                        ram_addr <= (others => '0');
                    
                        
                    end if;
                     if ram_addr = "00000" then
                         display_data <= display_data(23 downto 0) & first_byte;
                     else
                    display_data <= display_data(23 downto 0) & ram_out;
                    end if;

                    ram_addr <= std_logic_vector(unsigned(ram_addr) + 1);
                        counter <= 0;
                    else
                        counter <= counter + 1;
                    end if;
                    
                else
                    scroll_counter <= scroll_counter + 1;
                    
                    
                end if;
                next_state <= display_stage;
                                    
                        
                                    
                                

                                    
                when others =>
                    next_state <= IDLE;
            end case;
        end if;
    end process;

                                    


end Behavioral;
