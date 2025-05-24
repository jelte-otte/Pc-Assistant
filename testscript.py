import sys

print("Python script gestart")
sys.stdout.flush()

while True:
    line = sys.stdin.readline()
    if not line:
        break
    line = line.strip()
    print(f"VERWERKT: {line[::-1]}")
    sys.stdout.flush()
