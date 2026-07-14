# PSW - Python Stop Watch

`psw` is a lightweight, intuitive Command Line Interface (CLI) stopwatch and timer utility written in Python. It features live console rendering, interactive real-time controls, and built-in repeat functionalities without requiring any complex external audio dependencies.

## Install

You can install `psw` via pip:

```bash
pip install psw
```

## Usage

### 1. Stopwatch Mode

Measure elapsed time directly in your terminal.

#### Start the Stopwatch

To start the stopwatch, run:

```bash
psw start
```

The live clock will be displayed in the console:

```text
00 h 00 m 00.000 s
```

#### Options

* **`-p, --precision`**: Specifies the number of decimal places for seconds.
* **Default**: `3` (millisecond precision)
* **Example**: `psw start -p 2` will display `00 h 00 m 00.00 s`

#### Interactive Controls (While Running)

While the stopwatch is active, you can control it in real-time using the following keys:

* **`s`**: Pause / Resume the stopwatch.
* **`l`**: Record a lap time. The current lap time will be printed below the running clock without stopping the main timer.
* **`q` (or `Ctrl+C`)**: Quit the stopwatch and display the final summary.

### 2. Timer Mode

Count down from a specified duration with advanced repeat and notification options.

#### Start the Timer

To start a countdown, use the `timer` command followed by the duration. You can specify hours (`h`), minutes (`m`), and seconds (`s`).

```bash
# Set a timer for 5 minutes and 30 seconds
psw timer 5m 30s

# Set a timer for 1 hour
psw timer 1h
```

The countdown will be displayed in the console:

```text
00 h 05 m 30.000 s

```

#### Options

* **`-p, --precision`**: Same as the stopwatch mode, specifies the decimal places for seconds (Default: `3`).
* **`-r, --repeat [<integer>]`**: Restarts the timer when it reaches zero.
  * Use without arguments for an **infinite loop**.
    * *Example*: `psw timer 1m -r`
  * Specify an integer to repeat a **specific number of times**.
    * *Example*: `psw timer 1m -r 3` (Runs a 1-minute timer 3 times)
* **`-m, --mute`**: Disables the system alert sound (terminal bell) when the timer ends.

#### Interactive Controls (While Running)

* **`s`**: Pause / Resume the countdown.
* **`q` (or `Ctrl+C`)**: Cancel and exit the timer.

> [!NOTE]
> When the timer reaches `00 h 00 m 00.000 s`, a standard terminal bell sound (`\a`) will ring to notify you. No special OS-level audio permissions or external audio library imports are required, making it lightweight and cross-platform compatible.

## License

[MIT License](https://www.google.com/search?q=LICENSE)
