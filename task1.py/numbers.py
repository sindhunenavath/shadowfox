def format_number(num, fmt):
    return format(num, fmt)

result = format_number(145, 'o')
print("Formatted result:", result)



# 2. Area of a circular pond and total water

radius = 84
pi = 3.14

pond_area = pi * radius * radius
water_per_sq_meter = 1.4

total_water = pond_area * water_per_sq_meter

print("Pond Area =", pond_area)
print("Total Water in Pond =", int(total_water), "liters")


# 3. Speed calculation

distance = 490  # meters
time_minutes = 7

time_seconds = time_minutes * 60

speed = distance / time_seconds

print("Speed =", int(speed), "m/s")