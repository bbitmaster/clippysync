
# ClippySync

ClippySync is a command-line tool that allows you to sync clipboards across multiple machines on the same network. With ClippySync, you can easily share clipboard content between your devices, making it convenient to transfer text, links, or any other clipboard data seamlessly.

## Why ClippySync?

As the author of ClippySync, I developed this tool to address a personal need for clipboard syncing across multiple machines. In my setup, I use Sunshine and Moonlight for desktop sharing, which works great but lacks a built-in mechanism for clipboard sharing. ClippySync fills this gap by providing a seamless way to share clipboard content between devices.

ClippySync is not limited to my specific use case, however. It can be beneficial in various situations where clipboard sharing is not natively supported by remote desktop software. If you find yourself frequently needing to transfer text, links, or other clipboard data between machines, ClippySync can be a valuable tool in your workflow.

One notable aspect of ClippySync's development is the involvement of artificial intelligence (AI). Much of the code for this program was generated with the assistance of AI, using careful prompting and guidance from the author. As an experienced Python developer, I thoroughly reviewed, tested, and debugged the AI-generated code to ensure its functionality and reliability. In this sense, AI served as a powerful tool to expedite the development process while maintaining the necessary human oversight and expertise.

Whether you're using remote desktop software that lacks clipboard sharing or simply need a convenient way to sync clipboards across your devices, ClippySync provides a straightforward solution. Its development showcases the potential of AI-assisted coding, demonstrating how AI can be leveraged to accelerate software development while still relying on human knowledge and judgment to ensure the final product meets the desired standards.
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
pip install -e .
```
You may omit the -e flag if you don't want to install in editable mode

## Configuration

To use ClippySync, you need to create a YAML configuration file that specifies the machines you want to sync clipboards with. Here's an example configuration file:

```yaml
machines:
  192.168.0.10: 51234
  192.168.0.11: 51234
```

In this example, the configuration file defines two machines with their IP addresses and the port number to use for communication (51234 in this case). You can add as many machines as you want to the configuration file.

It's important to note that ClippySync does not provide any authentication mechanism beyond ensuring that incoming connections only come from IP addresses listed in the configuration file. As a result, it is highly recommended to use ClippySync only within a trusted local network environment.

When configuring ClippySync, make sure that all the machines and ports specified in the configuration file can connect to each other directly. This typically requires the machines to be on the same local network or connected through a secure VPN tunnel. Avoid using ClippySync over the public internet or untrusted networks, as it lacks robust security measures.

To minimize potential security risks, consider the following:

- Use ClippySync only within a trusted local network or secure VPN tunnel.
- Ensure that the machines listed in the configuration file are trusted and under your control.
- Avoid exposing the ports used by ClippySync to the public internet.
- Regularly review and update the configuration file to remove any machines that no longer require clipboard syncing.

By following these guidelines and being mindful of the lack of authentication, you can use ClippySync safely within a controlled environment.

Save the configuration file with a meaningful name, such as `config.yaml`, and keep it secure.
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

If you encounter any issues or errors while using ClippySync, consider the following troubleshooting steps:

1. Ensure that you have the latest version of ClippySync installed. Check for any available updates and upgrade to the most recent version.

2. Verify that the configuration file (`config.yaml`) is properly formatted and contains valid IP addresses and port numbers. Double-check the syntax and ensure that each machine entry follows the correct format.

3. Confirm that the machines specified in the configuration file are accessible and have ClippySync running. Ensure that the machines are powered on, connected to the network, and have ClippySync properly installed and configured.

4. Check that the necessary ports specified in the configuration file are open and not blocked by firewalls. Ensure that the firewall settings on each machine allow incoming connections on the specified ports.

5. If you encounter the following error when running ClippySync under tmux on Linux or in a terminal session outside of your desktop environment:
   ```
   Clipman error: Clipboard in TTY is unsupported.
   ```
   This error occurs due to a limitation in the `clipman` library when running in a non-graphical environment. To resolve this issue, you can set the following environment variables before running ClippySync:
   ```bash
   export XDG_SESSION_TYPE=x11
   export DISPLAY=:1
   ```
   Note that the `DISPLAY` variable may need to be set to `:0` or another value depending on your specific X server display session. Ensure that the value of `DISPLAY` points to the correct X server display session.

If you have followed the above troubleshooting steps and are still experiencing issues, please open an issue on the ClippySync GitHub repository, providing detailed information about the problem, including any error messages, system specifications, and steps to reproduce the issue. We'll be happy to assist you further.

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
