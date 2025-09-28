from struct import Struct

frame_header_format: str = (
    "<I"  # Bytes in frame
    + "H"  # Magic number
    + "H"  # Number of chunks in frame (old)
    + "H"  # Frame duration
    + "2x"  # For future
    + "I"  # Number of chunks in frame
)
frame_header_struct: Struct = Struct(frame_header_format)
frame_header_size: int = frame_header_struct.size

frame_bytes_format: str = "<I"
frame_bytes_struct: Struct = Struct(frame_bytes_format)
frame_bytes_size: int = frame_bytes_struct.size
