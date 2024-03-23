
# ClippySync

ClippySync is a command-line tool that allows you to sync clipboards across multiple machines on the same network. With ClippySync, you can easily share clipboard content between your devices, making it convenient to transfer text, links, or any other clipboard data seamlessly.

## Features

- Sync clipboards across multiple machines
- Easy configuration using a YAML file
- Secure communication between machines
- Cross-platform support (Windows, macOS, Linux)
- Prints a message when a paste is sent or received, including the size of the paste in characters

## Installation

To install ClippySync, you need to have Python 3.x installed on your system.

First clone the repository, then navigate to the directory and run

```
pip install clippysync
```
You may also use the `-e` flag to install in editable mode

## Configuration

To use ClippySync, you need to create a YAML configuration file that specifies the machines you want to sync clipboards with. Here's an example configuration file:

```yaml
machines:
  192.168.0.10: 50000
  192.168.0.11: 50000
```

In this example, the configuration file defines two machines with their IP addresses and the port number to use for communication (50000 in this case). You can add as many machines as you want to the configuration file.

Save the configuration file with a meaningful name, such as `config.yaml`.


## Usage

To start syncing clipboards, run the following command in your terminal:

```
clippysync --config /path/to/your/config.yaml
```

Replace `/path/to/your/config.yaml` with the actual path to your configuration file.

ClippySync will start running and will continuously sync clipboards between the machines specified in the configuration file. Whenever you copy something to the clipboard on one machine, it will be automatically shared with the other machines.

To stop ClippySync, press `Ctrl+C` in the terminal. The program will exit gracefully.

## Command-line Options

- `--config`: Specifies the path to the YAML configuration file (required).
- `--help`: Displays the help message and exits.

## Troubleshooting

- If you encounter any issues or errors, make sure that:
  - You have the latest version of ClippySync installed.
  - The configuration file is properly formatted and contains valid IP addresses and port numbers.
  - The machines specified in the configuration file are accessible and have ClippySync running.
  - The necessary ports are open and not blocked by firewalls.

## Contributing

If you'd like to contribute to ClippySync, please follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

## License

ClippySync is open-source software licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

If you have any questions, suggestions, or feedback, please feel free to raise an issue
