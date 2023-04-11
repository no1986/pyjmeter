from pyjmeter.jmx import createJMX


def main():
    createJMX("192.168.159.100", "30080", "/")
    return


if __name__ == "__main__":
    main()
