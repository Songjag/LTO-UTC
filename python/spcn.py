n = int(input())
total = 0.0
max_area = 0.0

for _ in range(n):
    l, r = map(float, input().split())
    area = l * r
    total += area
    if area > max_area:
        max_area = area

avg = total / n
print(f"{avg:.3f}")
print(f"{max_area:.3f}")
