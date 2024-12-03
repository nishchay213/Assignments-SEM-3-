import random
import string
import time
from dynamic_hash_table import DynamicHashSet, DynamicHashMap
from prime_generator import set_primes

# Define large prime sizes in descending order and set them
large_prime_sizes = [128021, 64007, 32003, 16001, 8009, 4001, 2003]
set_primes(large_prime_sizes)


def reset_primes():
    global large_prime_sizes
    set_primes(large_prime_sizes.copy())


# Parameters for Dynamic HashSet and DynamicHashMap
z, z1, z2, c2 = 31, 31, 37, 89
initial_table_size = 1009
params_chain = (z, initial_table_size)
params_linear = (z, initial_table_size)
params_double = (z1, z2, c2, initial_table_size)


def print_progress(current, total, prefix=''):
    """Simple progress indicator"""
    if current % (total // 100) == 0 or current == total - 1:
        percent = (current + 1) * 100 // total
        print(f"\r{prefix} [{percent:3d}%]", end='', flush=True)
        if current == total - 1:
            print()


def check_string_format(hash_structure):
    """
    Verify the string format according to PDF specifications:
    - Slots separated by |
    - Chain entries separated by ;
    - Empty slots shown as <EMPTY>
    - HashMap entries as (key, value)
    - HashSet entries as just the key
    - No quotes around strings
    """
    string_rep = str(hash_structure)

    # Basic format checks
    if not string_rep:
        print("[Error] Empty string representation")
        return False

    # Check slot separation
    slots = string_rep.split(" | ")
    if len(slots) != hash_structure.table_size:
        print(f"[Error] Expected {hash_structure.table_size} slots, got {len(slots)}")
        return False

    # Check format for each slot
    for slot in slots:
        # Check empty slot format
        if slot == "<EMPTY>":  # Corrected empty slot format
            continue

        # For chaining, check separator
        if hash_structure.collision_type == "Chain" and ";" in slot:
            entries = slot.split(" ; ")
        else:
            entries = [slot]

        # Check entry format
        for entry in entries:
            if isinstance(hash_structure, DynamicHashMap):
                # Check if entry matches (key, value) format without quotes
                if not (entry.startswith("(") and entry.endswith(")") and "," in entry):
                    print(f"[Error] Invalid HashMap entry format: {entry}")
                    return False
            else:  # HashSet
                # Check if entry is just the key without quotes
                if "," in entry or "(" in entry or ")" in entry:
                    print(f"[Error] Invalid HashSet entry format: {entry}")
                    return False

    return True


# Detailed and comprehensive test for DynamicHashSet
def exhaustive_test_dynamic_hashset(dynamic_hashset):
    reset_primes()
    correct = True
    rehash_trigger_count = 0

    # Test string format with a small set of insertions first
    test_keys = generate_large_random_strings(5)
    for key in test_keys:
        dynamic_hashset.insert(key)

    if not check_string_format(dynamic_hashset):
        print(f"[Error] String format check failed for {dynamic_hashset.collision_type} HashSet")
        correct = False

    # Continue with the rest of the original test...
    for i, key in enumerate(keys):
        print_progress(i, num_elements, f"Inserting keys ({dynamic_hashset.collision_type})")
        dynamic_hashset.insert(key)

        if i % 500 == 0 or i == num_elements - 1:
            load_factor = dynamic_hashset.get_load()
            if load_factor > 0.5:
                rehash_trigger_count += 1

            # Check string format after rehashing
            if not check_string_format(dynamic_hashset):
                print(f"[Error] String format check failed after rehash at {i} insertions")
                correct = False

            if any(not dynamic_hashset.find(k) for k in keys[:i + 1]):
                print(f"[Error] Missing key after rehash check at {i} insertions.")
                correct = False

    for key in keys[::2]:
        expected_slot = polynomial_hash(key, z, dynamic_hashset.table_size)
        if dynamic_hashset.get_slot(key) != expected_slot:
            print(f"[Error] Slot mismatch for key '{key}' in {dynamic_hashset.collision_type} probing.")
            correct = False
            break

    return correct


# Detailed and comprehensive test for DynamicHashMap
def exhaustive_test_dynamic_hashmap(dynamic_hashmap):
    reset_primes()
    correct = True
    rehash_trigger_count = 0

    # Test string format with a small set of insertions first
    test_keys = generate_large_random_strings(5)
    test_values = generate_large_random_strings(5)
    for key, value in zip(test_keys, test_values):
        dynamic_hashmap.insert((key, value))

    if not check_string_format(dynamic_hashmap):
        print(f"[Error] String format check failed for {dynamic_hashmap.collision_type} HashMap")
        correct = False

    # Continue with the rest of the original test...
    for i, (key, value) in enumerate(zip(keys, values)):
        print_progress(i, num_elements, f"Inserting pairs ({dynamic_hashmap.collision_type})")
        dynamic_hashmap.insert((key, value))

        if i % 500 == 0 or i == num_elements - 1:
            load_factor = dynamic_hashmap.get_load()
            if load_factor > 0.5:
                rehash_trigger_count += 1

            # Check string format after rehashing
            if not check_string_format(dynamic_hashmap):
                print(f"[Error] String format check failed after rehash at {i} insertions")
                correct = False

            if any(dynamic_hashmap.find(k) != v for k, v in zip(keys[:i + 1], values[:i + 1])):
                print(f"[Error] Missing or incorrect key-value after rehash check at {i} insertions.")
                correct = False

    for key in keys[::2]:
        expected_slot = polynomial_hash(key, z, dynamic_hashmap.table_size)
        if dynamic_hashmap.get_slot(key) != expected_slot:
            print(f"[Error] Slot mismatch for key '{key}' in {dynamic_hashmap.collision_type} probing.")
            correct = False
            break

    return correct


# Generate random strings function (unchanged)
def generate_large_random_strings(count, length=6):
    return [''.join(random.choice(string.ascii_letters) for _ in range(length)) for _ in range(count)]


# Initialize test data
num_elements = 50000

keys = generate_large_random_strings(num_elements)
values = generate_large_random_strings(num_elements)


# Character mapping function
def char_to_position(c):
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    elif 'A' <= c <= 'Z':
        return ord(c) - ord('A') + 26
    return 0


# Hash functions (unchanged)
def polynomial_hash(key, z, table_size):
    return sum(char_to_position(char) * (z ** idx) for idx, char in enumerate(key)) % table_size


def secondary_hash(key, z2, c2):
    return c2 - (sum(char_to_position(char) * (z2 ** idx) for idx, char in enumerate(key)) % c2)


# Initialize hash structures
dynamic_hashset_chain = DynamicHashSet("Chain", params_chain)
dynamic_hashset_linear = DynamicHashSet("Linear", params_linear)
dynamic_hashset_double = DynamicHashSet("Double", params_double)

dynamic_hashmap_chain = DynamicHashMap("Chain", params_chain)
dynamic_hashmap_linear = DynamicHashMap("Linear", params_linear)
dynamic_hashmap_double = DynamicHashMap("Double", params_double)

# Run the tests
start_time = time.time()
all_correct = True

# Test DynamicHashSets
for structure in [dynamic_hashset_chain, dynamic_hashset_linear, dynamic_hashset_double]:
    result = exhaustive_test_dynamic_hashset(structure)
    all_correct = all_correct and result

# Test DynamicHashMaps
for structure in [dynamic_hashmap_chain, dynamic_hashmap_linear, dynamic_hashmap_double]:
    result = exhaustive_test_dynamic_hashmap(structure)
    all_correct = all_correct and result

end_time = time.time()

# Print summary result
if all_correct:
    print("All tests passed successfully.")
else:
    print("Some tests failed. Please review the output for details.")
print(f"Total time for detailed exhaustive tests: {end_time - start_time:.3f} seconds")