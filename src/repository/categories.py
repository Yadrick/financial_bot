from dataclasses import dataclass


@dataclass
class Categories:
    categories: list[str]

    def __str__(self):
        output_to_print = ""
        for category in self.categories:
            output_to_print += f"{category}\n"
        return output_to_print

    def __contains__(self, item: str) -> bool:
        return item in self.categories

    def __bool__(self) -> bool:
        return bool(self.categories)
