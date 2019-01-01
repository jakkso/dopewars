#!/usr/bin/env python3
"""
Entry point for game
"""

from dopewars.gameplay import Gameplay

if __name__ == '__main__':
    try:
        Gameplay()
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        print('Goodbye!')
