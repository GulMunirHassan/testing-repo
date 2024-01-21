def calculate_square_area(side_length):
    """
    Calculate the area of a square.

    Parameters:
    - side_length (float): Length of the side of the square.

    Returns:
    - float: Area of the square.
    """
    if side_length <= 0:
        raise ValueError("Side length must be greater than zero.")
    
    area = side_length ** 2
    return area


def calculate_circle_area(radius):
    """
    Calculate the area of a circle.

    Parameters:
    - radius (float): Radius of the circle.

    Returns:
    - float: Area of the circle.
    """
    import math

    if radius <= 0:
        raise ValueError("Radius must be greater than zero.")
    
    area = math.pi * radius ** 2
    return area


def main():
    try:
        square_side = float(input("Enter the side length of the square: "))
        square_area = calculate_square_area(square_side)
        print(f"The area of the square is: {square_area}")

        circle_radius = float(input("Enter the radius of the circle: "))
        circle_area = calculate_circle_area(circle_radius)
        print(f"The area of the circle is: {circle_area}")

    except ValueError as ve:
        print(f"Error: {ve}")


if __name__ == "__main__":
    main()
