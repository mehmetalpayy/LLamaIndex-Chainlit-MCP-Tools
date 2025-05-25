import chainlit as cl
import math


@cl.step(type="tool")
async def calculate_sum(x: float, y: float) -> float:
    """
    Add two numbers together.
    Args:
        x: First number to add
        y: Second number to add
    Returns:
        The sum of x and y
    Example: calculate_sum(5, 3) returns 8
    """
    return x + y


@cl.step(type="tool")
async def calculate_average(x: float, y: float) -> float:
    """
    Calculate the arithmetic mean of two numbers.
    Args:
        x: First number
        y: Second number
    Returns:
        The average (arithmetic mean) of x and y
    Example: calculate_average(4, 6) returns 5
    """
    return (x + y) / 2


@cl.step(type="tool")
async def calculate_sqrt(number: float) -> float:
    """
    Calculate the square root of a number.
    Args:
        number: The number to calculate the square root of (must be non-negative)
    Returns:
        The square root of the input number
    Example: calculate_sqrt(16) returns 4
    """
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(number)