class ArchivePart:
    def __init__(self, order, start_byte, part_size, range):
        self.order = order
        self.start_byte = start_byte
        self.part_size = part_size
        self.range = range

    def __str__(self):
        return (f"order: {self.order}\n"
                f"start_byte: {self.start_byte}\n"
                f"part_size: {self.part_size}\n"
                f"range: {self.range}")
