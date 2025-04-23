import hashlib
import os
import sys

# ANSI color escape codes
COLORS = [
    "\033[91m",  # red
    "\033[92m",  # green
    "\033[93m",  # yellow
    "\033[94m",  # blue
    "\033[95m",  # magenta
    "\033[96m",  # cyan
    "\033[97m",  # white
]
RESET = "\033[0m"

def get_color(signal_name):
    """Assign colors based on signal name hash"""
    idx = int(hashlib.md5(signal_name.encode()).hexdigest(), 16) % len(COLORS)
    return COLORS[idx]

def draw_wave(signal: str, clk_signal: str) -> str:
    """Draw the waveform for a signal aligned with clk"""
    
    # Ensure both signal and clk_signal have the same length, pad if necessary
    max_len = max(len(signal), len(clk_signal))
    signal = signal.ljust(max_len, "0")  # Pad signal with '0' if it's shorter
    clk_signal = clk_signal.ljust(max_len, "0")  # Pad clk_signal with '0' if it's shorter
    
    waveform = "|"
    
    for i in range(max_len):
        if clk_signal[i] == '1':  # CLK is high, signal should match with high if it's 1
            if signal[i] == '1':
                waveform += "‾"  # High state
            else:
                waveform += "_"
        else:  # CLK is low, signal should match with low if it's 0
            if signal[i] == '1':
                waveform += "‾"
            else:
                waveform += "_"
        
        waveform += "|"
    
    return waveform  # No extra "|" here, it'll be handled outside this function

def write_waveform_output(block, header, txt_lines, md_lines, clk_signal):
    """Write the waveform output to text and markdown files"""
    txt_lines.append(header)
    md_lines.append(f"**{header}**\n")
    
    for signal, bits in block.items():
        wave = draw_wave(bits, clk_signal)
        label = f"{signal:<7}"

        # Terminal-friendly colorized output for text file (with ANSI codes)
        if sys.stdout.isatty():
            txt_lines.append(f"{get_color(signal)}{label}{wave}{RESET}")
        else:
            # Clean output for non-terminal (for GitLab Markdown and standard text file)
            txt_lines.append(f"{label}{wave}")

        # Markdown format for GitLab with code block
        md_lines.append(f"```\n{label}{wave}\n```")
    
    txt_lines.append("")  # New line after each block
    md_lines.append("")  # New line after each block

def process_waveform_file(input_file: str):
    """Process the waveform file and generate outputs"""
    base = os.path.splitext(input_file)[0]
    txt_output = base + "_output.txt"
    md_output = base + "_output.md"

    with open(input_file, "r") as f:
        lines = f.readlines()

    block = {}
    txt_lines = []
    md_lines = []

    clk_signal = None  # Initialize the clk_signal to capture the clk waveform

    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            if block:
                write_waveform_output(block, current_header, txt_lines, md_lines, clk_signal)
                block.clear()
            current_header = line
        elif line:
            signal, bits = line.split()
            block[signal] = bits

            if signal == "clk":
                clk_signal = bits  # Capture the clk signal

    if block:
        write_waveform_output(block, current_header, txt_lines, md_lines, clk_signal)

    # Writing the output to files
    with open(txt_output, "w") as f:
        f.write("\n".join(txt_lines))
    with open(md_output, "w") as f:
        f.write("\n".join(md_lines))

    print(f"\n✅ Terminal waveform → {txt_output}")
    print(f"📄 Markdown waveform → {md_output}")


# ==== ENTRY POINT ====
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 waveform_gen.py <input_file.txt>")
    else:
        process_waveform_file(sys.argv[1])
