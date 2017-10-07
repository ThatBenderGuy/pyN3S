class MemoryOwner(object):
    # def get_memory
    def get_bytes(self, position: int, size: int=1) -> bytes:
        """
        gets byte at given position
        """
        return self.get_memory[position:position + size]

    def set_byte(self):
        pass
