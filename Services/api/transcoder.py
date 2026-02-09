import time
import sys
import os

def main():
    input_path = sys.argv[1]
    output_dir = sys.argv[2]

    os.makedirs(output_dir, exist_ok=True)
    time.sleep(5)  # simulate heavy work

    output_file = os.path.join(output_dir, "output.txt")
    with open(output_file, "w") as f:
        f.write(f"Processed {input_path}")

if __name__ == "__main__":
    main()
