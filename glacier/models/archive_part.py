class ArchivePart:
    def __init__(self, order, vault_name, file_name, upload_id, start_byte, part_size, range):
        self.order = order
        self.vault_name = vault_name
        self.file_name = file_name
        self.upload_id = upload_id
        self.start_byte = start_byte
        self.part_size = part_size
        self.range = range

    def __str__(self):
        return (f"order: {self.order}\n"
                f"vault_name: {self.vault_name}\n"
                f"file_name: {self.file_name}\n"
                f"upload_id: {self.upload_id}\n"
                f"start_byte: {self.start_byte}\n"
                f"part_size: {self.part_size}\n"
                f"range: {self.range}")
