from struct import Struct

sprite_header_format: str = (
    "<I"  # File size
    + "H"  # Magic number (0xA5E0)
    + "H"  # Frames
    + "H"  # Width (in pixels)
    + "H"  # Height (in pixels)
    + "H"  # Color depth
    + "I"  # Flags
    + "H"  # Frame speed
    + "4x"  # Padding
    + "4x"  # Padding
    + "B"  # Transparent palette entry index
    + "3x"  # Ignore
    + "H"  # Number of colors
    + "B"  # Pixel width
    + "B"  # Pixel height
    + "h"  # Grid X position
    + "h"  # Grid Y position
    + "H"  # Grid width
    + "H"  # Grid height
    + "84x"  # For future
)
sprite_header_struct: Struct = Struct(sprite_header_format)
sprite_header_size: int = sprite_header_struct.size
