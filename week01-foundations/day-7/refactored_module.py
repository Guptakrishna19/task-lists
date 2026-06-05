"""
Refactored utilities module from Day 2.

This module contains commonly used utility functions that have been 
refactored for clarity, maintainability, and best practices.
"""


def double_positive_numbers(numbers):
    """
    Filter and double only positive numbers from a list.
    
    Args:
        numbers (list): A list of integers.
        
    Returns:
        list: A new list containing only positive numbers doubled.
        
    Example:
        >>> double_positive_numbers([1, -2, 3, -4, 5])
        [2, 6, 10]
    """
    result = []
    for num in numbers:
        if num > 0:
            result.append(num * 2)
    return result


def calculate(operand_a, operand_b, operation):
    """
    Perform basic arithmetic operations on two numbers.
    
    Args:
        operand_a (float): The first operand.
        operand_b (float): The second operand.
        operation (str): The operation to perform: 'add', 'sub', 'mul', or 'div'.
        
    Returns:
        float or None: The result of the operation, or None if division by zero.
        
    Raises:
        ValueError: If an unsupported operation is provided.
        
    Example:
        >>> calculate(10, 5, 'add')
        15
        >>> calculate(10, 0, 'div')
        
    """
    if operation == "add":
        return operand_a + operand_b
    elif operation == "sub":
        return operand_a - operand_b
    elif operation == "mul":
        return operand_a * operand_b
    elif operation == "div":
        if operand_b != 0:
            return operand_a / operand_b
        else:
            return None
    else:
        raise ValueError(f"Unsupported operation: {operation}")


def get_full_name(person_dict):
    """
    Combine first and last name from a person dictionary.
    
    Args:
        person_dict (dict): Dictionary with 'first' and 'last' keys.
        
    Returns:
        str: The full name as "first last".
        
    Raises:
        KeyError: If required keys are missing.
        
    Example:
        >>> get_full_name({'first': 'Kavya', 'last': 'Patel'})
        'Kavya Patel'
    """
    return f"{person_dict['first']} {person_dict['last']}"


def item_in_list(item, item_list):
    """
    Check if an item exists in a list.
    
    Args:
        item: The item to search for.
        item_list (list): The list to search in.
        
    Returns:
        bool: True if item is in list, False otherwise.
        
    Example:
        >>> item_in_list(3, [1, 2, 3, 4])
        True
    """
    return item in item_list


def count_word_frequencies(text):
    """
    Count the frequency of each word in a text.
    
    Args:
        text (str): The text to analyze.
        
    Returns:
        dict: Dictionary with words as keys and frequencies as values.
        
    Example:
        >>> count_word_frequencies('hello world hello')
        {'hello': 2, 'world': 1}
    """
    words = text.split()
    word_frequency = {}
    
    for word in words:
        word_frequency[word] = word_frequency.get(word, 0) + 1
    
    return word_frequency


if __name__ == "__main__":
    # Test examples
    print("Test 1 - Double positive numbers:")
    print(double_positive_numbers([1, -2, 3, -4, 5]))
    
    print("\nTest 2 - Calculate:")
    print(calculate(10, 5, "add"))
    print(calculate(10, 0, "div"))
    
    print("\nTest 3 - Full name:")
    print(get_full_name({"first": "Kavya", "last": "Patel"}))
    
    print("\nTest 4 - Item in list:")
    print(item_in_list(3, [1, 2, 3, 4]))
    
    print("\nTest 5 - Word frequencies:")
    print(count_word_frequencies("hello world hello python"))
