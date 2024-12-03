library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- Entity declaration for hex_to_7seg, which takes an 8-bit ASCII input and outputs a 7-segment display pattern
entity hex_to_7seg is
    Port ( 
        input : in STD_LOGIC_VECTOR(7 downto 0);    -- 8-bit input representing ASCII code
        segments : out STD_LOGIC_VECTOR(6 downto 0) -- 7-bit output for 7-segment display
    );
end hex_to_7seg;

architecture Behavioral of hex_to_7seg is
    signal int_value : integer;
begin
    int_value <= to_integer(unsigned(input));
    
    process(input, int_value)
    begin
        segments <= "1111110";  -- "-" pattern

        if (int_value >= 48 and int_value <= 57) then
            case (int_value - 48) is  
                when 0 => segments <= "0000001";  -- Display 0
                when 1 => segments <= "1001111";  -- Display 1
                when 2 => segments <= "0010010";  -- Display 2
                when 3 => segments <= "0000110";  -- Display 3
                when 4 => segments <= "1001100";  -- Display 4
                when 5 => segments <= "0100100";  -- Display 5
                when 6 => segments <= "0100000";  -- Display 6
                when 7 => segments <= "0001111";  -- Display 7
                when 8 => segments <= "0000000";  -- Display 8
                when 9 => segments <= "0000100";  -- Display 9
                when others => segments <= "1111110";  -- Fallback to "-"
            end case;

        elsif (int_value >= 97 and int_value <= 102) then
            case (int_value - 97) is  -- Adjusting for 'a' ASCII code
                when 0 => segments <= "0001000";  -- Display 'a'
                when 1 => segments <= "1100000";  -- Display 'b'
                when 2 => segments <= "0110001";  -- Display 'c'
                when 3 => segments <= "1000010";  -- Display 'd'
                when 4 => segments <= "0110000";  -- Display 'e'
                when 5 => segments <= "0111000";  -- Display 'f'
                when others => segments <= "1111110";  -- Fallback to "-"
            end case;

        elsif (int_value >= 65 and int_value <= 70) then
            case (int_value - 65) is  -- Adjusting for 'A' ASCII code
                when 0 => segments <= "0001000";  -- Display 'A'
                when 1 => segments <= "1100000";  -- Display 'B'
                when 2 => segments <= "0110001";  -- Display 'C'
                when 3 => segments <= "1000010";  -- Display 'D'
                when 4 => segments <= "0110000";  -- Display 'E'
                when 5 => segments <= "0111000";  -- Display 'F'
                when others => segments <= "1111110";  -- Fallback to "-"
            end case;

        -- If the input does not match any specified range, display "-" pattern
        else
            segments <= "1111110";  -- "-"
        end if;
    end process;
    
end Behavioral;