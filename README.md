# PSW - Python Stop Watch

This is a program of stopwatch in Python.
You can measure time in CLI.

## Install

```
pip install psw
```

## Usage

### Stopwatch

- You can start stopwatch:

  ```
  psw start
  ```
  
  The time is shown in console:

  ```
  00 h 00 m 00.000 s
  ```
  
  - options

    - `-p`: precision. It specifies decimal places.
      
      - default: 3 (millisecond)
      - example:
      
        `psw start -p 2` -> `00 h 00 m 00.00 s`

- While the stopwatch is running:
  - Press `s`: The stop watch stop / start
  - Press `l`: The lap time

### Timer

- You can use `psw` as timer.

  